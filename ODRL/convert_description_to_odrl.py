import os
import sys
import argparse
import requests
import time
from pyshacl import validate
from rdflib import Graph

OLLAMA_API = "http://10.147.18.82:11435/api/generate"
MODEL_NAME = "odrl-expert"
SHACL_FILE = "cdif-odrl-shacl-general.ttl"
MAX_RETRIES = 3

def generate_odrl(policy_name, description_text, error_feedback="", temperature=0.0):
    prompt = f"""You are tasked with converting a natural language description of a data/software policy into an ODRL (Open Digital Rights Language) Policy in JSON-LD format.

The policy should accurately reflect the permissions, prohibitions, and duties described in the text.
IMPORTANT: Your output MUST be a valid JSON-LD document representing the ODRL Policy. Return ONLY the raw JSON-LD code block and no other markdown or conversational text.

CRITICAL INSTRUCTION: DO NOT truncate the output. Output the FULL comprehensive JSON-LD.
CRITICAL INSTRUCTION: Ensure that ALL permissions explicitly granted or implied (e.g., use, access, copy) are individually listed as actions in the ODRL permission array.
CRITICAL INSTRUCTION: If the description requires users to create an account, register, or consent to terms, ensure these are represented as duties (e.g., "odrl:action": "cdif:consent" or "cdif:register" or "cdif:agreeToTerms").
CRITICAL INSTRUCTION: Use the 'https://cdif.org' domain for the ODRL profile instead of example.com (e.g., set "profile": "https://cdif.org/odrl:profile:{policy_name}").
CRITICAL INSTRUCTION: Set "target": "https://cdif.org/dataset/{policy_name}".
CRITICAL INSTRUCTION: You MUST use proper namespaces for actions and constraints, such as "odrl:use", "cdif:consent". Include "odrl": "http://www.w3.org/ns/odrl/2/" and "cdif": "https://cdif.org/odrl/" in your @context.
CRITICAL INSTRUCTION: Example of a duty structure: "duty": [{{"action": "cdif:consent", "target": "cdif:usageConditionsNotice"}}]

"""
    if error_feedback:
        prompt += f"""
CRITICAL INSTRUCTION: Your previous output failed SHACL validation! You MUST fix the following errors in your regenerated output:
{error_feedback}
"""

    prompt += f"""
Here is the policy description:
\"\"\"
{description_text}
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

def main():
    parser = argparse.ArgumentParser(description="Convert natural language policy descriptions to ODRL JSON-LD.")
    parser.add_argument("name", help="A short, unique name for the policy (e.g., 'copernicus').")
    parser.add_argument("--text", help="The natural language description of the policy.")
    parser.add_argument("--file", help="A file containing the natural language description.")
    parser.add_argument("--outdir", default="custom-policies", help="Directory to save the resulting JSON-LD.")
    
    args = parser.parse_args()
    
    if args.file:
        with open(args.file, "r") as f:
            description_text = f.read()
    elif args.text:
        description_text = args.text
    else:
        # Read from stdin if no text or file provided
        print("Reading description from standard input (Press Ctrl+D when finished):")
        description_text = sys.stdin.read()
        
    if not description_text.strip():
        print("Error: No description provided.")
        sys.exit(1)
        
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
        
    policy_name = args.name
    output_file = os.path.join(args.outdir, f"{policy_name}.jsonld")
    
    print(f"Generating ODRL for policy '{policy_name}'...")
    error_feedback = ""
    temperature = 0.0
    success = False
    
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"  Attempt {attempt}/{MAX_RETRIES} (temp: {temperature})...")
        try:
            odrl_json = generate_odrl(policy_name, description_text, error_feedback, temperature)
            conforms, error_text = validate_jsonld(odrl_json)
            
            if conforms:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(odrl_json)
                print(f"  Success! Passed SHACL validation and saved to {output_file}")
                success = True
                break
            else:
                print(f"  Validation failed on attempt {attempt}:")
                print("  " + error_text[:2000].replace("\n", "\n  ") + "...")
                error_feedback = error_text
                temperature += 0.2
        except Exception as e:
            print(f"  Error on attempt {attempt}: {e}")
            temperature += 0.2
            error_feedback = f"System Error: {e}"
            
    if not success:
        print(f"Failed to generate a valid ODRL policy for '{policy_name}' after {MAX_RETRIES} attempts.")
        sys.exit(1)

if __name__ == "__main__":
    main()
