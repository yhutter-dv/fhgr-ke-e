# Knowledge Engineering and Extraction
Personal notes and excersises for the module Knowledge Engineering and Extraction @ FHGR Chur. Using the awesome [markdown-slides library](https://github.com/dadoomer/markdown-slides) to turn Markdown into a RevealJs Presentation.

## Setup Protégé on Arch Linux
```bash
sudo pacman -S protege
sudo pacman -S jre8-openjdk
sudo archlinux-java set java-8-openjdk/jre
```
## Setup with Docker 
First of all make sure that Docker is actually installed and the Service is running:
```bash
sudo pacman -S docker
sudo systemctl start docker.service
```

### One Time Setup
```bash
sudo docker pull stain/jena-fuseki
```
### Running the Docker Container
```bash
sudo docker run -p 3030:3030 -e ADMIN_PASSWORD=admin stain/jena-fuseki
```

## Setup Presentation (optional)
```bash
python -m venv ./venv
source ./venv/bin/activate.sh
pip install -r requirements.txt
mdslides main.md --include media
```

## Python Code
The code examples can be found under the `code` directory.

## SPARQL Code

### FOAF Dataset

#### Default Query
```sql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
  ?sub ?pred ?obj .
} LIMIT 10
```

> Wie lauten die E-Mail Adresse, Name und Alter der Person, welche <http://example.org/bobsBlog> publiziert? Das Alter ist dabei optional.

```sql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name ?age ?mbox
WHERE {
   <http://example.org/bobsBlog> dc:publisher ?person .
  ?person foaf:name ?name .
  ?person foaf:mbox ?mbox .
  OPTIONAL {?person foaf:age ?age.} 
}
```
> Geben Sie folgende Personen und E-Mail Adressen aus: Die Person ist älter als 20 Jahre und bei der E-Mail Adresse handelt es sich um eine URI (und keinen String).

```sql
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?person ?name ?mbox ?age
WHERE {
  ?person foaf:name ?name .
  ?person foaf:mbox ?mbox .
  ?person foaf:age ?age .
  FILTER (?age > 20)
}
```

### Solar System Dataset

#### Default Query
```sql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
  ?sub ?pred ?obj .
} LIMIT 10
```

> Objekte, die um die Sonne oder um einen Satelliten der Sonne kreisen

```sql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
  ?sub ?pred ?obj .
} LIMIT 10
```
