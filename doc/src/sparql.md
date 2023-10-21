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


