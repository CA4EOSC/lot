import json
from pyshacl import validate
import rdflib

# Let's extract the actual output from Ollama by sending a quick request with temperature=0
# since the model is deterministic at temp 0.
