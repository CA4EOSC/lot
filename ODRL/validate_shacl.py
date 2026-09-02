import sys
from pyshacl import validate
from rdflib import Graph

def validate_odrl(data_file, shacl_file):
    print(f"Validating {data_file} against {shacl_file}...\n")
    
    # Load the data graph
    data_graph = Graph()
    try:
        data_graph.parse(data_file, format='json-ld')
    except Exception as e:
        print(f"Error parsing JSON-LD data file: {e}")
        return False
        
    # Load the shacl graph
    shacl_graph = Graph()
    try:
        shacl_graph.parse(shacl_file, format='turtle')
    except Exception as e:
        print(f"Error parsing SHACL file: {e}")
        return False
        
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shacl_graph,
        data_graph_format='json-ld',
        shacl_graph_format='turtle',
        inference='rdfs',
        debug=False,
        serialize_report_graph=True
    )
    
    print(f"Conforms: {conforms}\n")
    if not conforms:
        print("Validation Results:")
        print(results_text)
    
    return conforms

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_shacl.py <data.jsonld> <shacl.ttl>")
        sys.exit(1)
        
    data_file = sys.argv[1]
    shacl_file = sys.argv[2]
    
    validate_odrl(data_file, shacl_file)
