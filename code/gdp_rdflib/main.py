from rdflib import Graph, Namespace, BNode, Literal
from rdflib import FOAF
import pickle
import gzip
import csv
import os


def generate_graph_file(graph_file_path, gdp_file_path):
    # Note that we need to read this file in 'text mode' therefore 'rt'
    with gzip.open(gdp_file_path, "rt") as f:
        csv_reader = csv.reader(f)

        # Advance the iterator once so we skip the first row which contains the headers
        next(csv_reader)

        # Create a graph object which can be queried against
        g = Graph()

        # Define namespaces.
        # List of RDF Namespaces can be found here: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Predicates
        namespaces = {
                "default": Namespace("http://www.fhgr.ch/ke-e/gdp/2023"),
                "wd": Namespace("http://www.wikidata.org/entity/"),
                "wdt": Namespace("http://www.wikidata.org/prop/direct/"),
                "dpo": Namespace("https://dbpedia.org/")
        }

        # Bind all namespaces so that they do not need to be defined via PREFIX in queries...
        for name, ns in namespaces.items():
            g.bind(name, ns)

        # Queries for getting oecd and eu countries
        OECD_COUNTRY_QUERY = '''
            SELECT DISTINCT ?country ?label WHERE {
                SERVICE <https://query.wikidata.org/sparql> {
                    # Subject must be instance of OECD_Country
                    ?country wdt:P31 wd:Q113489728 ;
                             rdfs:label ?label .
                    # Only keep english labels
                    FILTER(LANG(?label) = "en")
                }
            }
            LIMIT 100
        '''

        EU_COUNTRY_QUERY = '''
            SELECT DISTINCT ?country ?label WHERE {
                SERVICE <https://query.wikidata.org/sparql> {
                    # subject must be part of European Union
                    ?country wdt:P361 wd:Q458 ;
                             rdfs:label ?label .
                    # Only keep english labels
                    FILTER(LANG(?label) = "en")
                }
            }
            LIMIT 100
        '''

        # Note that we actually get back a Literal instance therefore we need to convert to string
        oecd_countries = [str(country) for _, country in g.query(OECD_COUNTRY_QUERY)]
        eu_countries = [str(country) for _, country in g.query(EU_COUNTRY_QUERY)]

        # Note that the order must be the same as the headers in the csv file...
        for rank, country, imf_gdp, un_gdp, gdp_per_capita, pop in csv_reader:
            if country not in oecd_countries and country not in eu_countries:
                continue
            is_oecd = country in oecd_countries 

            # Convert e.g "United States" into "United_States"
            country_name = country.strip().replace(' ', '_').replace('-', '_')
            country_node = BNode()
            country_name = Literal(country_name)
            rank = Literal(int(rank))
            oecd = Literal(is_oecd)
            gdp_per_capita = Literal(gdp_per_capita)
            imf_gdp = Literal(imf_gdp)
            un_gdp = Literal(un_gdp)
            population_total = Literal(pop)

            default = namespaces["default"]
            dpo = namespaces["dpo"]

            g.add((country_node, default.rank, rank))
            g.add((country_node, default.oecd, oecd))
            g.add((country_node, FOAF.name, country_name))
            g.add((country_node, default.gdpPerCapita, gdp_per_capita))
            g.add((country_node, default.imfGDP, imf_gdp))
            g.add((country_node, default.unGDP, un_gdp))
            g.add((country_node, dpo.populationTotal, population_total))

        # Save graph object
        with open(graph_file_path, "wb") as f:
            pickle.dump(g, f)
            print(f"Created graph file: {graph_file_path}")


def write_oecd_csv(file_path, graph):
    OECD_COUNTRY_QUERY = '''
        SELECT DISTINCT ?country_name ?population_total ?gdp WHERE {
            ?s  foaf:name ?country_name;
                dpo:populationTotal ?population_total;
                default:gdpPerCapita ?gdp;
                default:oecd ?oecd .
            FILTER(?oecd)
        }
    '''
    # Implemented with reference: https://docs.python.org/3/library/csv.html
    with open(file_path, "w", newline='') as f:
        field_names = ["country_name", "population_total", "gdp"]
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for result in graph.query(OECD_COUNTRY_QUERY):
            writer.writerow({
                "country_name": result["country_name"],
                "population_total": result["population_total"],
                "gdp": result["gdp"]
            })
        print(f"Created file {file_path}")


def write_eu_csv(file_path, graph):
    EU_COUNTRY_QUERY = '''
        SELECT DISTINCT ?country_name ?population_total ?gdp WHERE {
            ?s  foaf:name ?country_name;
                dpo:populationTotal ?population_total;
                default:gdpPerCapita ?gdp;
                default:oecd ?oecd .
            FILTER(!?oecd)
        }
    '''
    # Implemented with reference: https://docs.python.org/3/library/csv.html
    with open(file_path, "w", newline='') as f:
        field_names = ["country_name", "population_total", "gdp"]
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for result in graph.query(EU_COUNTRY_QUERY):
            writer.writerow({
                "country_name": result["country_name"],
                "population_total": result["population_total"],
                "gdp": result["gdp"]
            })
        print(f"Created file {file_path}")


if __name__ == "__main__":
    gdp_file_path = "./vertiefungsbeispiel-gdp.csv.gz"
    graph_file_path = "./graph.bin"
    oecd_file_path = "./oecd.csv"
    eu_file_path = "./eu.csv"

    # Check if expected input file was provided...
    if not os.path.isfile(gdp_file_path):
        print(f"Expected to find file {gdp_file_path} but it was not found")
        exit()

    if not os.path.isfile(graph_file_path):
        print(f"Graph file {graph_file_path} not found and will be created...")
        generate_graph_file(graph_file_path, gdp_file_path)

    with open(graph_file_path, "rb") as f:
        graph = pickle.load(f)
        print(f"Loaded graph file: {graph_file_path}")
        write_oecd_csv(oecd_file_path, graph)
        write_eu_csv(eu_file_path, graph)
