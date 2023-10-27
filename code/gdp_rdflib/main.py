from rdflib import Graph, Namespace, BNode, Literal
from rdflib import FOAF, DC 
import gzip
import csv
import os


if __name__ == "__main__":


    input_file_path = "./vertiefungsbeispiel-gdp.csv.gz"

    # Check if expected input file was provided...
    if not os.path.isfile(input_file_path):
       print(f"Expected to find file {input_file_path} but it was not found") 
       exit()
    
    # Create a graph object which can be queried against
    g = Graph()

    # Note that we need to read this file in 'text mode' therefore 'rt'
    with gzip.open(input_file_path, "rt") as f:
        csv_reader = csv.reader(f)

        # Advance the iterator once so we skip the first row which contains the headers
        next(csv_reader)

        # Define namespaces.
        default = Namespace("http://www.fhgr.ch/ke-e/gdp/2023")
        dpo = Namespace("https://dbpedia.org/")

        g.bind("default", default)
        g.bind("dpo", dpo)

        QUERY = '''
            SELECT ?name ?rank
            WHERE {
                ?s default:rank ?rank .
                ?s foaf:name ?name .
            }
            ORDER BY ASC (?rank)
        '''
        # Note that the order must be the same as the headers in the csv file...
        for rank, country, imf_gdp, un_gdp, gdp_per_capita, pop in csv_reader:
            # Convert e.g "United States" into "United_States"
            country_name = country.strip().replace(' ', '_').replace('-', '_')
            country_node = BNode()
            country_name = Literal(country_name)
            rank = Literal(int(rank))
            gdp_per_capita = Literal(gdp_per_capita)
            imf_gdp = Literal(imf_gdp)
            un_gdp = Literal(un_gdp)
            population_total = Literal(pop)

            g.add((country_node, default.rank, rank))
            g.add((country_node, FOAF.name, country_name))
            g.add((country_node, default.gdpPerCapita, gdp_per_capita))
            g.add((country_node, default.imfGDP, imf_gdp))
            g.add((country_node, default.unGDP, un_gdp))
            g.add((country_node, dpo.populationTotal, population_total))

        #for _, _, name in g.triples((None, FOAF.name, None)):
            #print(name)

        for name, rank in g.query(QUERY):
            print(f"Name: {name} Rank: {rank}")


