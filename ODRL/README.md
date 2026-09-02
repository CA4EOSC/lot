# ODRL-powered Legal Interoperability

**This is a Legal Interoperability Framework supported by ODRL policies, implemented as CDIF for access profile.**

This directory contains Ollama `Modelfile` definitions (with `.md` extensions) used to instantiate specialized AI agents for the Semantic Croissant ecosystem. These models have custom system prompts, context parameters, and temperature settings baked in.

## Available Models

- `llama3.2-croissant.md`: Llama 3.2 specialized in metadata engineering and generating MLCommons Croissant JSON-LD.
- `llama3.2-odrl.md`: Llama 3.2 specialized in ODRL policy and data rights generation.
- `gemma4-croissant.md` / `gemma-odrl.md`: Equivalent specialized models using Gemma.
- `bipm_expert.md`: Expert agent tailored for BIPM standard processing.
- `mcp_agent.md`: Agent specialized in interacting via the Model Context Protocol (MCP).

## How to Create and Run These Models

To use these customized models locally, you need to use the `ollama create` command. This reads the model configurations (e.g., system prompt, base model, temperature) from the provided file and registers it in your local Ollama registry.

### 1. Ensure Ollama is installed and running
Make sure you have [Ollama](https://ollama.com/) installed and the background service is running on your machine.

### 2. Create the Models
Run the following commands from this `prompts/` directory to create the specialized models:

```bash
# Create the Croissant Metadata agent
ollama create llama3.2-croissant -f llama3.2-croissant.md

# Create the ODRL Policy agent
ollama create llama3.2-odrl -f llama3.2-odrl.md

# (Optional) Create the Gemma alternatives
ollama create gemma-croissant -f gemma4-croissant.md
ollama create gemma-odrl -f gemma-odrl.md

# Create the MCP and BIPM agents
ollama create mcp-agent -f mcp_agent.md
ollama create bipm-expert -f bipm_expert.md
```

### 3. Verify Creation
Check that the models now appear in your local list:
```bash
ollama list
```

### 4. Run the Models
You can now run any of these custom models directly from the CLI or invoke them via the Ollama API (e.g., at `http://localhost:11434/api/generate`):

```bash
ollama run llama3.2-croissant
```

## Note on File Extensions
Although these files have `.md` (Markdown) extensions to allow for easy reading and syntax highlighting of the embedded prompts on GitHub, they are fully valid Ollama Modelfiles containing the required `FROM`, `PARAMETER`, and `SYSTEM` directives.

## Natural Language Policy Conversion

In addition to automated SPDX license conversion, the framework provides a tool to convert arbitrary natural language policy descriptions into valid ODRL.

The script `convert_description_to_odrl.py` accepts text descriptions and generates SHACL-compliant JSON-LD (using a generalized SHACL shape).

**Example Usage (Copernicus Data Space):**
```bash
python convert_description_to_odrl.py copernicus --text "On Copernicus website there is a different kind of policy and user should create account first and after... if he wants to use some data with API, this user should open page with specific dataset and manually click to consent with conditions of usage. So there is manual interaction inside."
```

This will automatically extract the duties (e.g., `cdif:createAccount`, `cdif:consent`), structure them into an ODRL policy, run the self-healing SHACL loop, and save the result to `custom-policies/copernicus.jsonld`.

## Web URL Policy Conversion

The framework also provides a tool to fetch policy text directly from external websites, extract the readable text (ignoring HTML, navigation, and scripts), and convert it into a CDIF-compliant ODRL policy.

The script `convert_url_to_odrl.py` accomplishes this using `beautifulsoup4` and automatically handles truncation for extremely long web pages to prevent LLM hallucination.

**Example Usage (Copernicus Web License):**
```bash
python convert_url_to_odrl.py copernicus_web --url https://www.copernicus.eu/en/access-data/copyright-and-licences
```

The resulting validated policy will be saved to `custom-policies/copernicus_web.jsonld`.


## SPDX to ODRL Conversion Pipeline

This directory also contains the infrastructure for converting raw software licenses into machine-readable [ODRL (Open Digital Rights Language)](https://www.w3.org/TR/odrl-model/) policies compliant with the CDIF specification.

### 1. The Expert Model (`generate_expert_models.py`)
Because generating valid, deeply nested JSON-LD graphs is difficult for standard LLMs, we first generate a highly specialized `odrl-expert` model. 
This script builds a custom Ollama Modelfile that uses `gemma4:31b` as its foundation. It bakes in a massive system prompt containing the entire W3C ODRL Information Model specification, strict JSON-LD `@context` rules, and exact structural requirements (like pluralized properties and required `odrl:duty` blocks).

### 2. The Conversion Script (`batch_convert_spdx_to_odrl.py`)
This script automates the mass conversion of all 727 software licenses in the [SPDX index](https://spdx.org/licenses/).
- **Fetching:** It downloads the raw legal text for each license from the SPDX API.
- **Generation:** It sends the license text to the `odrl-expert` model running on a remote Ollama server.
- **Self-Healing Loop:** The script implements a powerful retry mechanism. It validates the LLM's output in-memory using `pyshacl` and a strict SHACL shape file (`cdif-odrl-shacl.ttl`).
- **Feedback & Correction:** If the LLM hallucinates an invalid target, forgets a duty, or uses a singular property instead of a plural one, the SHACL validator instantly rejects it. The script catches this error and feeds the *exact* SHACL violation string back into the LLM as a subsequent prompt, while slightly bumping the temperature. This allows the model to self-correct its JSON structure.
- **Storage:** Once the policy passes the SHACL validation perfectly, it is saved into the `spdx-to-odrl/` directory as a valid `.jsonld` file.

### 3. SHACL Validation (`cdif-odrl-shacl.ttl`)
The validator ensures that every output policy perfectly adheres to our CDIF profile requirements:
- The target MUST be a valid expanded IRI (e.g., `https://spdx.org/licenses/...`).
- Every `odrl:permission` MUST include an `odrl:action` and at least one `odrl:duty`.
- Constraints MUST use `odrl:eq` and map to valid right-operands like `cdif:copiesOrSubstantialPortions`.

