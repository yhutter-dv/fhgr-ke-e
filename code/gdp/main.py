import os.path
import gzip
import csv

"""
Reads a csv gz compressed file about Country rankings in regards to their gdp values and writes out
a Turtle conform file which can be imported into SPAQRQL Triplestore.
Implemented with reference to:
    - https://docs.python.org/3/library/gzip.html#gzip.GzipFile
    - https://docs.python.org/3/library/csv.html#csv.reader
"""


def add_namespaces(content):
    content.append("@base <http://text.org/>.")
    content.append("@prefix default: <http://text.org/uebung#>.")
    content.append("@prefix dpo: <https://dbpedia.org/>.")
    content.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.")
    content.append("@prefix dc: <http://purl.org/dc/elements/1.1/#/>.")

    return content

if __name__ == "__main__":
    input_file_path = "./vertiefungsbeispiel-gdp.csv.gz"
    output_file_path = "./output.ttl"

    # Check if expected input file was provided...
    if not os.path.isfile(input_file_path):
       print(f"Expected to find file {input_file_path} but it was not found") 
       exit()
    
    # Note that we need to read this file in 'text mode' therefore 'rt'
    with gzip.open(input_file_path, "rt") as f:
        csv_reader = csv.reader(f)

        # Add required namespaces...
        output_content = []
        output_content = add_namespaces(output_content)

        # Advance the iterator once so we skip the first row which contains the headers
        next(csv_reader)

        # Note that the order must be the same as the headers in the csv file...
        for rank, country, imf_gdp, un_gdp, gdp_per_capita, pop in csv_reader:
            # Convert e.g "United States" into "United_States"
            row_subject = country.strip().replace(' ', '_').replace('-', '_')

            # Add necessary statements...
            rank_statement = f'<{row_subject}> default:rank "{rank}"^^xsd:nonNegativeInteger.' 
            name_statement = f'<{row_subject}> dc:name "{country}".'
            gdp_per_capita_statement = f'<{row_subject}> default:gdpPerCapita "{gdp_per_capita}"^^xsd:double.' 
            imf_gdp_statement = f'<{row_subject}> default:imfGDP "{imf_gdp}"^^xsd:double.' 
            un_gdp_statement = f'<{row_subject}> default:unGDP "{un_gdp}"^^xsd:double.' 
            population_statement = f'<{row_subject}> dpo:populationTotal "{pop}"^^xsd:nonNegativeInteger.' 

            output_content += [rank_statement, name_statement, gdp_per_capita_statement, imf_gdp_statement, un_gdp_statement, population_statement]

        with open(output_file_path, "w") as f:
            for line in output_content:
                f.write(f"{line}\n")

        print(f"Finished converting {input_file_path} to {output_file_path}")
