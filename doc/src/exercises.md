# Übungsbeispiele und Lösungen

## SPARQL

> *Selektiere den Publisher, Author und Buchtitel derjenigen Elemente, welche "Semantic Web" im Titel haben*

```sql
PREFIX dc:<http://purl.org/dc/elements/1.1
SELECT ?publisher ?author ?title WHERE {
  ?book dc:publisher ?publisher .
  ?book dc:title ?title .
  ?book dc:author ?author .
  FILTER(REGEX(?title, "Semantic Web"))
}

```

> *Selektiere den Publisher, Author und Buchtitel derjenigen Elemente, welche nach dem Jahr 2012 veröffentlicht wurden*

```sql
PREFIX dc:<http://purl.org/dc/elements/1.1
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#> 

SELECT ?publisher ?author ?title WHERE {
  ?book dc:publisher ?publisher .
  ?book dc:title ?title .
  ?book dc:author ?author .
  ?book dc:date ?date .
  FILTER(?date >= '2013-01-01'^^xsd:date)
}

```


> *Selektiere alle Personen welche bei IBM arbeiten, jedoch nicht die FHGR besucht haben*

```sql
PREFIX foat:<http://xmlns.com/foaf/0.1

SELECT ?person ?name WHERE {
  ?person foaf:name ?name .
  ?person foaf:workplaceHomepage ?work .
  OPTIONAL {
    ?person foaf:schoolHomepage ?atFHGR .
    FILTER(?atFHGR = "http://www.fhgr.ch")
  }
  FILTER(?work = "http://ibm.com" && !bound(?atFHGR)) } 
```

## Aufgabenblatt 01

### Metadaten
![Aufgabenblatt 01 Metadaten Aufgabenstellung ](./images/homework_01_metadata.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Metadaten Lösung](./images/homework_01_metadata_solution.png)
</details>

### Anonyme Ressource
![Aufgabenblatt 01 anonyme Ressourcen Aufgabenstellung ](./images/homework_01_anonym_ressource.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Anonyme Ressourcen Lösung](./images/homework_01_anonym_ressource_solution.png)
</details>

### Annotationen
![Aufgabenblatt 01 Annotationen Aufgabenstellung ](./images/homework_01_annotations.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Annotationen Lösung](./images/homework_01_annotations_solution.png)
</details>


### Reification
![Aufgabenblatt 01 Reification Aufgabenstellung](./images/homework_01_reification.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Reification Lösung](./images/homework_01_reification_solution.png)
</details>

### Serialisierungsformate
![Aufgabenblatt 01 Serialisierungsformate Aufgabenstellung](./images/homework_01_serialization_formats.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Serialisierungsformate Lösung](./images/homework_01_serialization_formats_solution.png)
</details>

![Aufgabenblatt 01 Serialisierungsformate RDF Aufgabenstellung](./images/homework_01_serialization_formats_rdf.png)

<details>
  <summary><b>Lösung</b></summary>

  ![Aufgabenblatt 01 Serialisierungsformate RDF Lösung](./images/homework_01_serialization_formats_rdf_solution.png)
</details>

## Aufgabenblatt 02

### FOAF
![Aufgabenblatt 02 FOAF Aufgabenstellung](./images/homework_02_foaf.png)

<details>
  <summary><b>Lösung</b></summary>

  > Wie lauten die E-Mail Adressen, Name und Alter der Person, welche `bobsBlog` publizierten? Das Alter ist dabei `optional`
  ```sql
  PREFIX dc: <http://purl.org/dc/elements/1.1/>
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>

  SELECT ?mbox ?name ?age {
    <http://example.org/bobsBlog> dc:publisher ?bob.
    ?bob foaf:name ?name.
    OPTIONAL {
    ?bob foaf:age ?age
    }
  }
  ```

  > Wie viele unterschiedliche E-Mail Adressen gibt es in der Datenbank?
  ```sql
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>

  SELECT (count(?mbox) as ?anzahl) {
    ?s foaf:mbox ?mbox
  }
  ```
  > Geben sie alle Personen aus, welche älter als 20 Jahre sind und bei denen die E-Mail Adresse eine URI ist
  ```sql
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>

  SELECT ?person ?mbox {
    ?person foaf:age ?age;
    foaf:mbox ?mbox.
    FILTER(?age > 20 && isURI(?mbox))
  }
  ```

  > Sortieren Sie das Ergebnis alphabetisch nach der Person (aufsteigend)

  ```sql
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>

  SELECT ?person ?mbox {
    ?person foaf:age ?age;
    foaf:mbox ?mbox.
    FILTER(?age > 20 && isURI(?mbox))
  }
  ORDER BY ?person
  ```
  
</details>


### Sonne, Mond und Sterne
![Aufgabenblatt 02 Sonne, Mond und Sterne Aufgabenstellung](./images/homework_02_planets.png)

<details>
  <summary><b>Lösung</b></summary>

  > Objekte die um die Sonne oder um einen Satelliten der Sonne kreisen

  ```sql
  PREFIX ex: <http://example.org/>

  SELECT ?obj ?sat {
    ex:Sonne ex:satellit ?sat.
    OPTIONAL {
      ?sat ex:satellit ?obj.
    }
  }
  ```

  > Alle Objekte welche ein Volumen von mehr als 2 x 10^10 Kubikkilometer besitzen und falls vorhanden der dazugehörige Satellit

  ```sql
  PREFIX ex: <http://example.org/>

  SELECT ?obj ?sat {
    ?sat ex:radius ?radius.
    OPTIONAL {
      ?obj ex:satellit ?sat.
    }
    FILTER (4/3*3.14*?radius*?radius*?radius > 2E10)
  }
  ```

  > Objekte mit einem Satelliten, für den ein englischsprachiger Name gegeben ist, die ausser- dem Satellit eines Objektes von über 3000 (km) Durchmesser sind

  ```sql
  PREFIX ex: <http://example.org/>

  SELECT ?stern ?obj ?sat {
    ?obj ex:satellit ?sat.
    ?sat ex:name ?name.
    ?stern ex:satellit ?obj.
    FILTER (lang(?name) = "en")
  }
  ```

  > Objekte mit zwei oder mehr Satelliten (nehmen Sie an, dass unterschiedliche URIs hier unterschiedliche Objekte bezeichnen)

  ```sql
  PREFIX ex: <http://example.org/>

  SELECT ?obj ?sat1 ?sat2 {
    ?obj ex:satellit ?sat1, ?sat2 .
    FILTER(?sat1 != ?sat2)
  }
  ```
</details>

### Cafe

![Aufgabenblatt 02 Cafe Aufgabenstellung](./images/homework_02_cafe.png)

<details>
  <summary><b>Lösung</b></summary>

  > Geben Sie alle Statements des Café Datensatzes aus, um dessen Struktur und Vokabular zu ermitteln.

  ```sql
  SELECT ?s ?p ?o
  WHERE {
    ?s ?p ?o.
  }
  ```

  > Ermitteln sie die Namen aller Cafés und deren Rating.

  ```sql
  PREFIX dc: <http://purl.org/dc/elements/1.1/>
  PREFIX ex: <http://inf.ed.ac.uk/examples#>

  SELECT ?cafe ?name ?rating
  WHERE {
    ?cafe dc:title ?name.
    ?cafe ex:rating ?rating.
  } 
  ```

  > Geben Sie aus, welche Personen Café's lieben, die im "eastEnd" beheimatet sind.

  ```sql
  PREFIX dc: <http://purl.org/dc/elements/1.1/>
  PREFIX dbp: <http://dbpedia.org/property/>
  PREFIX ex: <http://inf.ed.ac.uk/examples#>

  SELECT ?cafe ?name ?person
  WHERE {
    ?cafe dbp:locatedIn ex:eastEnd.
    ?cafe dc:title ?name.
    ?cafe ex:lovedBy ?person.
  }
  ```

  > Geben Sie bei der vorhergehenden Aufgabe zusätzlich aus, welche Personen die ermittelten Café Liebhaber kennen.

  ```sql
  PREFIX dbp: <http://dbpedia.org/property/>
  PREFIX ex: <http://inf.ed.ac.uk/examples#>

  SELECT ?cafe ?name ?person ?knows
  WHERE {
    ?cafe dbp:locatedIn ex:eastEnd.
    ?cafe <http://purl.org/dc/elements/1.1/title> ?name.
    ?cafe ex:lovedBy ?person.
    OPTIONAL {?person <http://xmlns.com/foaf/0.1/knows> ?knows}.
  }
  ```
</details>

## Ontologien

### Ermitteln Sie die Anzahl an Ländern auf DBpedia

<details>
  <summary><b>Lösung</b></summary>

  ```sql
  SELECT DISTINCT ?country ?name WHERE {
    ?country rdf:type dbo:Place .
    ?country rdfs:label ?name .
    FILTER(lang(?name) = "de")
  }
  ```
</details>

### Alle Schweizer Kantone in der deutschen DBpedia

<details>
  <summary><b>Lösung</b></summary>

  ```sql
  SELECT DISTINCT ?capital {
    ?capital dbo:wikiPageWikiLink dbc:Cantons_of_Switzerland .
  }
  ```
</details>

### Alle Schweizer Kantone in der deutschen DBpedia und die zugehörigen Hauptorte

<details>
  <summary><b>Lösung</b></summary>

  ```sql
  SELECT DISTINCT ?capital ?mainCity ?label WHERE {
    ?capital dbo:wikiPageWikiLink dbc:Cantons_of_Switzerland .
    ?capital dbp:seat ?mainCity .
    ?mainCity rdfs:label ?label .
    FILTER(lang(?label) = "de")
  }
  ```
</details>

### Die Abgeordneten des Schweizer Bundesrats und deren Geburtsort

<details>
  <summary><b>Lösung</b></summary>

  ```sql
  SELECT DISTINCT ?member ?birthPlace WHERE {
    ?member dcterms:subject dbc:Members_of_the_Federal_Council_\(Switzerland\).
    ?member dbo:birthPlace ?birthPlace.
  }
  ```
</details>

### Die Anzahl an Schweizer Abgeordneten per Geburtsort (es sollen nur Orte mit mindestens zwei Abgeordneten berücksichtigt werden)


<details>
  <summary><b>Lösung</b></summary>

  ```sql
  SELECT DISTINCT ?member ?birthPlace (count(?member) AS ?memberCount) WHERE {
    ?member dcterms:subject dbc:Members_of_the_Federal_Council_\(Switzerland\).
    ?member dbo:birthPlace ?birthPlace .
    FILTER(lang(?birthPlaceLabel) = "de")
  }
  GROUP BY ?birthPlace
  HAVING (count(?member) >= 2)
  ```
</details>

## Pizza Ontologie
![Aufgabenblatt 03 Pizza Ontologie](./images/homework_03_pizza.png)

<details>
  <summary><b>Lösung</b></summary>

  ```sql
  @base <http://www.ai.wu.ac.at/.../bibTeX#>.
  @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
  @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

  <Nicht_vegetarische_Pizza> rdfs:subClassOf <Pizza> .
  <Vegetarische_Pizza> rdfs:subClassOf <Pizza> .
  <Vegane_Pizza> rdfs:subClassOf <Vegetarische_Pizza> .
  <Nicht_vegetarischer_PizzaBelag> rdfs:subClassOf <PizzaBelag> .
  <Vegetarischer_PizzaBelag> rdfs:subClassOf <PizzaBelag> .
  <Veganer_PizzaBelag> rdfs:subClassOf <Vegetarischer_PizzaBelag> .

  aw:hatBelag rdf:type rdf:Property;
              rdfs:domain <Pizza>;
              rdfs:range <PizzaBelag> .

  aw:hatVegetarischenBelag rdf:type rdf:Property;
                           rdfs:domain <Pizza>;
                           rdfs:range <Vegetarischer_PizzaBelag> .

  aw:hatVeganenBelag rdf:type rdf:Property;
                     rdfs:domain <Pizza>;
                     rdfs:range <Veganer_PizzaBelag> .
  ```
</details>