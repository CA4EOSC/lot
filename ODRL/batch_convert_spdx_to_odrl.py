import os
import requests
import json
import time
from pyshacl import validate
from rdflib import Graph

OLLAMA_API = "http://10.147.18.82:11435/api/generate"
MODEL_NAME = "odrl-expert"
SPDX_INDEX_URL = "https://spdx.org/licenses/licenses.json"
OUTPUT_DIR = "spdx-to-odrl"
SHACL_FILE = "cdif-odrl-shacl.ttl"
MAX_RETRIES = 3

def fetch_spdx_index():
    print(f"Fetching SPDX license index from {SPDX_INDEX_URL}...")
    response = requests.get(SPDX_INDEX_URL)
    response.raise_for_status()
    return response.json().get("licenses", [])

def fetch_license_details(license_id):
    url = f"https://spdx.org/licenses/{license_id}.json"
    print(f"  Fetching details for {license_id} from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_odrl(license_id, license_text, error_feedback="", temperature=0.0):
    prompt = f"""You are tasked with converting a legal software license into an ODRL (Open Digital Rights Language) Policy in JSON-LD format.

The policy should accurately reflect the permissions, prohibitions, and duties specified in the license text.
IMPORTANT: Your output MUST be a valid JSON-LD document representing the ODRL Policy. Return ONLY the raw JSON-LD code block and no other markdown or conversational text.

CRITICAL INSTRUCTION: DO NOT truncate the output. Output the FULL comprehensive JSON-LD.
CRITICAL INSTRUCTION: Ensure that ALL permissions explicitly granted by the license text (e.g., use, copy, modify, merge, publish, distribute, sublicense, sell) are individually listed as actions in the ODRL permission array.
CRITICAL INSTRUCTION: Use the 'https://cdif.org' domain for the ODRL profile instead of example.com (e.g., set "profile": "https://cdif.org/odrl:profile:{license_id}").
CRITICAL INSTRUCTION: Define the "spdx" namespace in the "@context" (mapping to "https://spdx.org/licenses/") and use this prefix for the target property (e.g., set "target": "spdx:{license_id}.html").
CRITICAL INSTRUCTION: You MUST use proper namespaces for actions and constraints, such as "odrl:use", "odrl:copy", "cdif:merge", "cdif:includeNotice". Include "odrl": "http://www.w3.org/ns/odrl/2/" and "cdif": "https://cdif.org/odrl/" in your @context.
CRITICAL INSTRUCTION: Structure duties and constraints strictly like this example: "duty": [{{"action": "cdif:includeNotice", "constraint": [{{"leftOperand": "cdif:scope", "operator": "odrl:eq", "rightOperand": "cdif:copiesOrSubstantialPortions"}}], "target": ["cdif:copyrightNotice", "cdif:permissionNotice"]}}]

"""
    if error_feedback:
        prompt += f"""
CRITICAL INSTRUCTION: Your previous output failed SHACL validation! You MUST fix the following errors in your regenerated output:
{error_feedback}
"""

    prompt += f"""
Here is the {license_id} license text:
\"\"\"
{license_text}
\"\"\"
"""
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 4096
        }
    }
    
    response = requests.post(OLLAMA_API, json=payload, timeout=600) 
    response.raise_for_status()
    result = response.json()
    
    output_text = result.get("response", "")
    
    # Clean up output
    if output_text.startswith("```json"):
        output_text = output_text.split("```json", 1)[1]
    elif output_text.startswith("```jsonld"):
        output_text = output_text.split("```jsonld", 1)[1]
    elif output_text.startswith("```"):
        output_text = output_text.split("```", 1)[1]
    
    if output_text.endswith("```"):
        output_text = output_text.rsplit("```", 1)[0]
        
    return output_text.strip()

def validate_jsonld(json_str):
    try:
        data_graph = Graph()
        data_graph.parse(data=json_str, format='json-ld')
        shacl_graph = Graph()
        shacl_graph.parse(SHACL_FILE, format='turtle')
        
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shacl_graph,
            data_graph_format='json-ld',
            shacl_graph_format='turtle',
            inference='rdfs',
            debug=False,
            serialize_report_graph=False
        )
        return conforms, results_text
    except Exception as e:
        return False, str(e)

def run_batch():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    licenses = fetch_spdx_index()
    print(f"Found {len(licenses)} licenses in SPDX index.")
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for i, lic in enumerate(licenses):
        license_id = lic.get("licenseId")
        if not license_id:
            continue
            
        output_file = os.path.join(OUTPUT_DIR, f"{license_id}.jsonld")
        print(f"[{i+1}/{len(licenses)}] Processing {license_id}...")
        
        if os.path.exists(output_file):
            print(f"  Skipping {license_id}, file already exists.")
            skipped_count += 1
            continue
            
        try:
            details = fetch_license_details(license_id)
            license_text = details.get("licenseText")
            
            if not license_text:
                print(f"  Warning: No license text found for {license_id}. Skipping.")
                error_count += 1
                continue
                
            error_feedback = ""
            temperature = 0.0
            success = False
            
            for attempt in range(1, MAX_RETRIES + 1):
                print(f"  Attempt {attempt}/{MAX_RETRIES} for {license_id} (temp: {temperature})...")
                odrl_json = generate_odrl(license_id, license_text, error_feedback, temperature)
                
                conforms, error_text = validate_jsonld(odrl_json)
                if conforms:
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(odrl_json)
                    print(f"  Success! Passed SHACL validation and saved to {output_file}")
                    success_count += 1
                    success = True
                    break
                else:
                    print(f"  Validation failed on attempt {attempt}:")
                    # print first 2000 chars of error to avoid huge terminal spam
                    print("  " + error_text[:2000].replace("\n", "\n  ") + "...")
                    error_feedback = error_text
                    temperature += 0.2 # Bump temp for next try to get variations
                    
            if not success:
                print(f"  Failed to generate valid ODRL for {license_id} after {MAX_RETRIES} attempts.")
                error_count += 1
            
        except Exception as e:
            print(f"  Error processing {license_id}: {e}")
            error_count += 1
            
        time.sleep(1)
        
    print("\n--- Batch Run Complete ---")
    print(f"Successfully processed: {success_count}")
    print(f"Skipped (already existed): {skipped_count}")
    print(f"Errors: {error_count}")

if __name__ == "__main__":
    run_batch()
