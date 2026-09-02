import json
import urllib.request
import requests
import sys

SPDX_INDEX_URL = "https://spdx.org/licenses/licenses.json"
OLLAMA_API = "http://10.147.18.82:11435/api/generate"
MODEL_NAME = "odrl-expert"
TARGET_LICENSE = "MIT"

def run_test():
    print(f"Fetching SPDX license index from {SPDX_INDEX_URL}...")
    try:
        req = urllib.request.urlopen(SPDX_INDEX_URL)
        index_data = json.loads(req.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching SPDX index: {e}")
        sys.exit(1)

    # Find the target license in the index
    license_info = next((lic for lic in index_data.get("licenses", []) if lic.get("licenseId") == TARGET_LICENSE), None)
    if not license_info:
        print(f"Could not find license '{TARGET_LICENSE}' in the SPDX index.")
        sys.exit(1)
        
    details_url = license_info.get("detailsUrl")
    print(f"Found {TARGET_LICENSE} license. Fetching details from {details_url}...")
    
    try:
        req = urllib.request.urlopen(details_url)
        license_details = json.loads(req.read().decode('utf-8'))
        license_text = license_details.get("licenseText", "")
        print(f"Successfully fetched {len(license_text)} characters of license text.")
    except Exception as e:
        print(f"Error fetching license details: {e}")
        sys.exit(1)

    prompt = f"""Please analyze the following legal license text and convert it into a valid ODRL Policy (in JSON-LD format).
The policy should accurately reflect the permissions, prohibitions, and duties specified in the license text.
IMPORTANT: Your output MUST be a valid JSON-LD document representing the ODRL Policy. Return ONLY the raw JSON-LD code block and no other markdown or conversational text.
CRITICAL INSTRUCTION: DO NOT truncate the output. Output the FULL comprehensive JSON-LD.
CRITICAL INSTRUCTION: Ensure that ALL permissions explicitly granted by the license text (e.g., use, copy, modify, merge, publish, distribute, sublicense, sell) are individually listed as actions in the ODRL permission array.
CRITICAL INSTRUCTION: Use the 'https://cdif.org' domain for the ODRL profile instead of example.com (e.g., set "profile": "https://cdif.org/odrl:profile:mit").
CRITICAL INSTRUCTION: Define the "spdx" namespace in the "@context" (mapping to "https://spdx.org/licenses/") and use this prefix for the target property (e.g., set "target": "spdx:{TARGET_LICENSE}.html").
CRITICAL INSTRUCTION: You MUST use proper namespaces for actions and constraints, such as "odrl:use", "odrl:copy", "cdif:merge", "cdif:includeNotice". Include "odrl": "http://www.w3.org/ns/odrl/2/" and "cdif": "https://cdif.org/odrl/" in your @context.
CRITICAL INSTRUCTION: Structure duties and constraints strictly like this example: "duty": [{{"action": "cdif:includeNotice", "constraint": [{{"leftOperand": "cdif:scope", "operator": "odrl:eq", "rightOperand": "cdif:copiesOrSubstantialPortions"}}]}}]

Here is the {TARGET_LICENSE} license text:
\"\"\"
{license_text}
\"\"\"
"""

    for i in range(1, 4):
        print(f"\\n--- Run {i} ---")
        print(f"Sending request to Ollama model '{MODEL_NAME}'...")
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0 # Force maximum determinism
            }
        }

        try:
            response = requests.post(OLLAMA_API, json=payload, timeout=600)
            response.raise_for_status()
            result = response.json()
            
            output_text = result.get("response", "")
            
            # Strip markdown code blocks if the model wrapped it
            if output_text.startswith("```json"):
                output_text = output_text.split("```json", 1)[1]
            elif output_text.startswith("```jsonld"):
                output_text = output_text.split("```jsonld", 1)[1]
            elif output_text.startswith("```"):
                output_text = output_text.split("```", 1)[1]
            
            if output_text.endswith("```"):
                output_text = output_text.rsplit("```", 1)[0]
                
            output_text = output_text.strip()
            
            output_file = f"odrl_output_{i}.jsonld"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_text)
                
            print(f"Success! ODRL policy generated and saved to {output_file}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API on run {i}: {e}")

if __name__ == "__main__":
    run_test()
