import json
import urllib.request
import requests
import sys

URL = "https://mcp.dev.codata.org/vault/0Ai0aUfF8e8aka72QszE5g.jsonld"
OLLAMA_API = "http://10.147.18.82:11435/api/generate"
MODEL_NAME = "cdif-expert"

def run_test():
    print(f"Fetching input data from {URL}...")
    try:
        req = urllib.request.urlopen(URL)
        input_data = req.read().decode('utf-8')
        print(f"Successfully fetched {len(input_data)} bytes of JSON-LD data.")
    except Exception as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    prompt = f"""Please analyze the following JSON-LD dataset and generate a CDIF-compliant metadata representation for it.
Structure your response according to the Cross-Domain Interoperability Framework (CDIF) profiles (e.g., Core Profile, Discovery Profile, Data Description Profile).
IMPORTANT: Your output MUST be a valid JSON-LD document. Return ONLY the raw JSON-LD code block and no other markdown or conversational text.
CRITICAL INSTRUCTION: DO NOT truncate the output. You must generate every single observation and element from the input dataset. DO NOT use ellipsis like '...' or comments to skip content. Output the FULL comprehensive JSON-LD.

Here is the input JSON-LD:
```json
{input_data}
```
"""

    print(f"\\nSending request to Ollama model '{MODEL_NAME}'...")
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1
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
        if output_text.startswith("```jsonld"):
            output_text = output_text.split("```jsonld", 1)[1]
        if output_text.startswith("```"):
            output_text = output_text.split("```", 1)[1]
        if output_text.endswith("```"):
            output_text = output_text.rsplit("```", 1)[0]
        output_text = output_text.strip()
        
        output_file = "cdif_output.jsonld"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_text)
            
        print(f"\nSuccess! CDIF response generated and saved to {output_file}")
        print("Preview of the generated content:\n")
        print(output_text[:500] + "...\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama API: {e}")
        print("Please ensure Ollama is running and the 'cdif-expert' model has been created.")

if __name__ == "__main__":
    run_test()
