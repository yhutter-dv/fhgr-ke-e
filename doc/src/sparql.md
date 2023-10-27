# SPARQL
* Ist eine Abfragesprache um `triples` aus einem Triple Story zu holen.
* Ist angelehnt an SQL
* Gibt ein `XML` basiertes Format zurück

## Wichtige Query Typen
* `SELECT`: Gibt Ergebnisse (Zeilen) aus einer Tabelle zurück
* `CONSTRUCT`: Konstruiert einen neuen RDF Graph auf basis eines bestehenden Query
* `ASK`: Gibt `true` oder `false` zurück
* `DESCRIBE`: Gibt eine vom Maintainer für sinnvoll erachtete Beschreibung zurück
* `OPTIONAL`: Gibt an dass ein RDF Statement nicht zwingend erfüllt werden muss
* `FILTER`: Kann genutzt um nach gewissen Kriterien zu filtern

## Struktur eines Query
* **Result Clause**: Definiert die Informationen, welche vom Query zurückgegeben und angezeigt werden sollen
* **Dataset Definition**: Definiert, welche RDF Graphen abgefragt werden sollen
* **Query Pattern**: Definiert die RDF Statements welche erfüllt werden müssen
* **Query Modifiers**: Modifiziert, reduziert das Resultat
* Variablen werden mit `$` oder `?` angegeben, bspw. `?name`

```sql
# prefix (namespace) declarations
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
…
# result clause (variables to bind, i.e. the columns to return)
SELECT …
# dataset definition (optional)
FROM < … >
# query pattern
WHERE {
…
}
# query modifiers
GROUP BY …            # SPARQL 1.1
HAVING …              # SPARQL 1.1
ORDER BY …
```
## Wichtige Filter Operatoren
| Kategorie | Funktionen und Operatoren | Beispiele |
|-----------|---------------------------|-----------|
| Logische  | !, &&, !=, <, >           |?age >= 42 |
| Mathematik| +,-,*,/                   |?discount * ?price >= 42.0|
| Überprüfungen | isURI, isBLANK, isLITERAL, bound |!bound(?person)|
| Accessors | str, lang, datatype |lang(?name) = "en"|
| Übriges | sameTerm, langMatches, regex|regex(?isbn, '9-\d{4}-\d{3}')|


## Wichtige Mengen Operatoren

### Union (Disjunction)
**Vereinigt** zwei Mengen miteinander.

```sql
PREFIX rdf: <http://www.w3.org/..../#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/ex/>

SELECT ?person ?name
WHERE {
    ?person foaf:name ?name .
    { ?person rdf:type ex:Adult. }
    UNION
    { ?person foaf:age ?age.
      FILTER (?age >=18)
    }
}
```

### Minus (Negation)
**Zieht** eine Menge von einer anderen ab.

```sql
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX ex: <http://example.org/ex/>

SELECT ?person ?name
WHERE {
   { ?person foaf:name ?name.}
   MINUS
   { ?person foaf:age ?age.
     FILTER (?age < 18)
   }
}
```

## Umgang mit Duplikaten
Hier gibt es die zwei Befehle `DISTINCT` und `REDUCE`. REDUCE ist ein schnellerer Algorightmus, entfernt jedoch möglicherweise nicht alle Duplikate.
Die zwei Begriffe beziehen sich immer auf die gesamte Zeile (alle Variablen):

```sql
SELECT DISTINCT ?name ?person ?title WHERE {
  ...
}
```

## Sortierung, Limiterung und Slicing
Um die Ergebnisse zu **sortieren** kann der Befhel `ORDER BY ASC` und `ORDER BY DESC` verwendet werden:

```sql
SELECT DISTINCT ?name ?person ?title WHERE {
  ...
} ORDER BY ASC(?name)
```
Um die Anzahl der Ergebnisse zu **limitieren** wird der Befehl `LIMIT` verwendet:

```sql
SELECT DISTINCT ?name ?person ?title WHERE {
  ...
} ORDER BY ASC(?name) LIMIT 10
```
Um die **nächste Anzahl** von Ergebnissen zu verhalten wird der Befehl `OFFSET` verwendet:

```sql
SELECT DISTINCT ?name ?person ?title WHERE {
  ...
} ORDER BY ASC(?name) LIMIT 10 OFFSET 10
```

## Aggregationen
Um Ergebnisse nach **bestimmten Merkmalen** zu gruppieren können Aggregationen verwendet werden:
```sql
PREFIX rdf: <http://www.w3.org/...#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX yago: <http://dbpedia.org/class/yago/>

SELECT ?nation (count(?res) AS ?medalists)
WHERE {
    ?res rdf:type yago:WinterOlympicsMedalists .
    ?res dbpedia-owl:nationality ?nation .
}
GROUP BY ?nation
ORDER BY DESC(?medalists)
```

Um Aggregationen **zu filtern** kann der `HAVING` Befehl verwendet werden:
```sql
PREFIX rdf: <http://www.w3.org/...#>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
PREFIX yago: <http://dbpedia.org/class/yago/>

SELECT ?nation (count(?res) AS ?medalists)
WHERE {
    ?res rdf:type yago:WinterOlympicsMedalists .
    ?res dbpedia-owl:nationality ?nation .
}
GROUP BY ?nation
HAVING (?medalists >= 2)
ORDER BY DESC(?medalists)
```

## Kombination von Datenquellen
Um zwei unterschiedliche Datenquellen miteinander zu verbinden wird der `SERVICE` Befehl verwendet:
```sql
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
...
SELECT ?actor_name ?birth_date
WHERE {
    SERVICE <http://data.linkedmdb.org/sparql> {
        ?movie  rdfs:label       "Star Trek: The Motion Picture";
                movie:actor      ?actor .
        ?actor  movie:actor_name ?actor_name .
    }
    SERVICE <http://dbpedia.org/sparql> {
        ?actor2 a                 dbpedia:Actor ;
                foaf:name         ?actor_name_en ;
                dbpedia:birthDate ?birth_date .
        FILTER(STR(?actor_name_en) = ?actor_name)
    }
}
```
Wichtig anzumerken ist jedoch, dass der Service Befehl **aus Sicherheitsgründen** deaktiviert sein kann.
