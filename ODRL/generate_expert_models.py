import os
import glob
import tempfile
import urllib.request
import zipfile
import argparse
from bs4 import BeautifulSoup
import markdownify

def generate_cdif():
    REPO_ZIP_URL = "https://github.com/cross-domain-interoperability-framework/cdifbook/archive/refs/heads/main.zip"
    OUTPUT_MODELFILE = "cdif_expert.md"
    
    print(f"Downloading CDIF book source from GitHub...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "cdifbook.zip")
        urllib.request.urlretrieve(REPO_ZIP_URL, zip_path)
        
        print("Extracting archive...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
            
        extracted_dir = os.path.join(temp_dir, "cdifbook-main")
        
        # Gather all markdown files
        md_files = glob.glob(os.path.join(extracted_dir, "**", "*.md"), recursive=True)
        
        # Filter out irrelevant files (like GitHub templates or standard repo readmes)
        irrelevant = ["README.md", "CLAUDE.md", "GEMINI.md", "AGENTS.md", "setup-review.md", "content-review.md"]
        md_files = [f for f in md_files if os.path.basename(f) not in irrelevant and ".github" not in f]
        
        # Sort files to have some deterministic order
        md_files.sort()
        
        print(f"Found {len(md_files)} markdown pages. Compiling...")
        
        all_markdown_content = []
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    filename = os.path.relpath(file_path, extracted_dir)
                    all_markdown_content.append(f"### Source Document: {filename}\n\n{content}\n")
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                
        compiled_text = "\n---\n".join(all_markdown_content)
        
        modelfile_content = f"""FROM gemma4:e4b

PARAMETER temperature 0.1
PARAMETER num_ctx 32768

SYSTEM \"\"\"You are an expert on the Cross-Domain Interoperability Framework (CDIF).
Your task is to answer any questions regarding CDIF, structure, architecture, and implementations.
Use the following official CDIF documentation to ground your answers:

{compiled_text}
\"\"\"
"""
        with open(OUTPUT_MODELFILE, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
            
        print(f"Successfully generated '{OUTPUT_MODELFILE}' ({len(modelfile_content)} bytes).")
        print(f"You can now run: ollama create cdif-expert -f {OUTPUT_MODELFILE}")

def generate_odrl():
    OUTPUT_MODELFILE = "odrl_expert.md"
    url = "https://www.w3.org/TR/odrl-model/"
    print(f"Downloading ODRL Information Model from {url}...")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    
    print("Parsing HTML and converting to Markdown...")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove scripts and styles for cleaner markdown
    for element in soup(["script", "style", "nav", "footer"]):
        element.extract()
        
    # Get the main content body
    body = soup.body
    
    # Convert HTML to Markdown
    md_content = markdownify.markdownify(str(body), heading_style="ATX")
    
    modelfile_content = f"""FROM gemma4:e4b

PARAMETER temperature 0.1
PARAMETER num_ctx 32768

SYSTEM \"\"\"You are an expert on the Open Digital Rights Language (ODRL).
Your task is to answer any questions regarding ODRL policies, profiles, rules, and rights expressions.

CRITICAL INSTRUCTIONS FOR LICENSE CONVERSION:
When asked to convert a legal license to ODRL JSON-LD, you MUST adhere strictly to the following schema:
1. ALWAYS define these namespaces in your @context: 
   "odrl": "http://www.w3.org/ns/odrl/2/"
   "spdx": "https://spdx.org/licenses/"
   "cdif": "https://cdif.org/odrl/"
   "@vocab": "http://www.w3.org/ns/odrl/2/"
   "action": {{"@type": "@id"}}
   "target": {{"@type": "@id"}}
   "profile": {{"@type": "@id"}}
2. ALWAYS use the cdif.org domain for profiles, e.g., "profile": "https://cdif.org/odrl/profile/mit".
3. ALWAYS specify ALL permissions explicitly granted by the license text. CRITICAL: You MUST create a separate JSON object in the "permission" array for EACH individual action (e.g., odrl:use, odrl:reproduce, odrl:modify, cdif:merge, cdif:publish, odrl:distribute, odrl:sublicense, odrl:sell). Do NOT group them into a single action array. Note: use odrl:reproduce instead of copy.
4. When generating duties (like copyright notices), you MUST use this exact structure:
   "duty": [{{
     "action": "cdif:includeNotice",
     "constraint": [{{
       "leftOperand": "cdif:scope",
       "operator": "odrl:eq",
       "rightOperand": "cdif:copyOrSubstantialPortion"
     }}],
     "target": [
       "cdif:copyrightNotice",
       "cdif:permissionNotice"
     ]
   }}]

Use the following official ODRL documentation to ground your answers:

### Source Document: ODRL Information Model 2.2
{url}

{md_content}
\"\"\"
"""
    with open(OUTPUT_MODELFILE, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
        
    print(f"Successfully generated '{OUTPUT_MODELFILE}' ({len(modelfile_content)} bytes).")
    print(f"You can now run: ollama create odrl-expert -f {OUTPUT_MODELFILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Ollama Modelfiles for domain expert agents.")
    parser.add_argument('target', choices=['cdif', 'odrl', 'all'], help="Which expert model to generate (cdif, odrl, or all).")
    
    args = parser.parse_args()
    
    if args.target in ['cdif', 'all']:
        generate_cdif()
        print()
    if args.target in ['odrl', 'all']:
        generate_odrl()
