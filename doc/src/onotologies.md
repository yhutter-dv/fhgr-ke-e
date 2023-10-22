# Ontologien
Im Gegensatz zum Menschen ist für den Computer die **menschliche Sprache nicht verständlich**.
Aus diesem Grund wurden verschiedene Ansätze probiert:
* Vergabe von `Tags` um eine gewisse Struktur in die Daten zu kriegen. Der Nachteil hierbei ist jedoch dass der Computer zwar die Tags interpretieren kann, jedoch nicht den eigentlichen Inhalt, für welchen diese stehen
* Die nächste Möglichkeit ist es, dem Computer "hardcodierte Bedeutungen" mithilfe von `Dublin Core`, `FOAF` etc. beizubringen. Dies ist jedoch inflexibel und auf das in diesen Quellen definierte Vokabular beschränkt.

Aus diesem Grund wurden `Ontologiesprachen` erfunden:
* Applikation interpretiert Definitionen
* Ontologien spezifizieren die Bedeutung des Vokabulars in einer Domäne
* Vokabular kann aus anderen Domänen heraus referenziert werden (Knowledge Sharing)
* Besitzt Ähnlichkeit zu SQL, hat jedoch einen Fokus auf `Deduktion`, d.h. Ableitung von Zusammenhängen anstelle von Datenintegrität
* Sowohl der Computer als auch der Mensch haben so ein gemeinsames Verständnis

## TBox (Terminology Component)
* Beschreibt die verwendete Terminologie innerhalb einer Domäne
* Klassen, Eigenschaften und Beziehungen

## ABox (Assertion Component)
* Beschreibt Fakten, mithilfe der in der TBox definierten Terminologie

## Beschreibungssprachen
* Ressource Description Framework Schema (RDFS)
* Web Ontologie Language (OWL)

## Ressource Description Framework Schema (RDFS)
|Terminologie|Beschreibung|
|------------|------------|
|rdf:Property|Definierte eine Eigenschaft|
|rdfs:Class|Definiert eine Klasse|
|rdfs:subClassOf|Definierte eine Parent Child Relation zwischen Klassen|
|rdfs:subPropertyOf|Definiert eine Parent Child Relation zwischen Eigenschaften|
|rdfs:domain|Definiert gültige Klassen, Eigenschaften für ein bestimmtes Subjekt|
|rdfs:range|Definiert gültige Eigenschaften (Werte) für eine bestimmte Klasse|

## Beispiel RFDS Definition
```sql
@base <http://www.ai.wu.ac.at/.../bibTeX#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix aw: <http://bsp.at/.../bibTeX#>.

<Book>            rdfs:subClassOf   <Entry>  .
<Thesis>          rdfs:subClassOf   <Entry>  .
<MasterThesis>    rdfs:subClassOf   <Thesis> .
<PhdThesis>       rdfs:subClassOf   <Thesis> .
<Journal>         rdfs:subClassOf   <Entry>  .
...

aw:publishedIn   rdf:type              rdf:Property.
aw:inJournal     rdfs:subPropertyOf    aw:publishedIn.
aw:inProc        rdfs:subPropertyOf    aw:publishedIn.
```

```sql
@prefix aw:    <http://bsp.at/.../bibTeX#>.
@prefix p:     <http://bsp.at/.../people#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

p:Anna                 p:age          "-22".

p:age    rdfs:domain   p:Person;
         rdfs:range    xsd:nonNegativeInteger.
```

### TBox
```sql
@prefix family:<https://weichselbraun.net/semtech/family#> .
@prefix foaf:<http://xmlns.com/foaf/0.1/> .
@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> .

family:Female   rdf:type           foaf:Person;
                foaf:gender        "female".
family:Male     rdf:type           foaf:Person;
                foaf:gender        "male".

family:Relative rdfs:subClassOf    foaf:Person.
family:Father   rdfs:subClassOf    family:Relative, family:Male.
family:Mother   rdfs:subClassOf    family:Relative, family:Female.

family:related  rdfs:subClassOf    rdf:Property;
                rdfs:range         family:Relative;
                rdfs:domain        family:Relative.
```

### ABox

```sql
@base: <http://go.gl/test#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.

<Anna>      a               foaf:Person;
            foaf:name       "Anna Maria Toth";
            foaf:mbox       "mailto:anna@toth.org".
            family:Father   <Peter>;
            family:related  <Daniela>;
            foaf:img        <https://weichselbraun.net/img/anna.jpg>.

<Peter>     a               foaf:Person;
            foaf:name       "Peter Toth".

<Daniela>   a               foaf:Person;
            foaf:name       "Daniela Mayer" .
```

## OWL
OWL bietet im Gegensatz zu RDFS folgende **Vorteile**:
* Unterstützt das Ausdrücken von Kardinalitäten (mindestens 1, maximal 2 etc.)
* Erlaubt das Ausdrücken von erweiterten Eigenschaften

### Beziehungen zwischen zwei Eigenschaften
```sql
:hasAge    owl:equivalentProperty ex:age.
:hasParent owl:inverseOf          :hasChild.
```

### Symmetrische Eigenschaften
* Transitive Eigenschaften bedeutet, wenn `A` zu `B` eine Beziehung hat und `B` zu `C`, dann hat automatisch auch `C` zu `A` eine Beziehung. Ein Beispiel hierfür ist die `Verwandschaft`. Man kann sich dies auch als eine Art `Vererbung` vorstellen
* Symmetrische Eigenschaften gehen in `beide Richtungen`
* Asymmetrisch Bedeutet, es funktioniert nur in `eine Richtung`

```sql
:related     rdf:type    owl:SymmetricProperty.
:hasChild    rdf:type    owl:AsymmetricProperty.
:hasAncestor rdf:type    owl:TransitiveProperty.
```

### Funktionale Abhängigkeiten
* Funktionale Eigenschaften definieren die Beziehung `eindeutig`

```sql
:hasMother   rdf:type    owl:FunctionalProperty.
:hasChild    rdf:type    owl:InverseFunctionalProperty.
```

### Klassenhierarchie
```sql
@prefix family:<https://www.semanticlab.net/kee/family/>.
@prefix foaf:<http://xmlns.com/foaf/0.1/>.
@prefix owl:<http://www.w3.org/2002/07/owl#>.

family:Male     rdfs:subClassOf    foaf:Person.
family:Female   rdfs:subClassOf    foaf:Person.
family:Relative rdfs:subClassOf    foaf:Person.
family:Child    rdfs:subClassOf    family:Relative
family:Parent   rdfs:subClassOf    family:Relative.
family:Father   rdfs:subClassOf    family:Parent, family:Male.
family:Mother   rdfs:subClassOf    family:Parent, family:Female.
```
### Objekteigenschaften
```sql
family:related     rdf:type           owl:SymmetricProperty, 
                                      owl:TransiviteProperty;
                   rdfs:range         family:Relative;
                   rdfs:domain        family:Relative.
family:hasChild    rdfs:subPropertyOf family:related;
                   rdfs:domain        family:Parent;
                   rdfs:range         family:Child.
family:hasDaughter rdfs:subPropertyOf family:hasChild;
                   rdfs:range         family:Child, family:Female.
family:hasSon      rdfs:subClassOf    family:hasChild;
                   rdfs:range         family:Child, family:Male.
family:hasParent   rdfs:subPropertyOf family:related;
                   owl:inverseOf      family:hasChild.
family:hasFather   rdfs:subPropertyOf family:hasParent;
                   rdfs:range         family:Father.
family:hasMother   rdfs:subPropertyOf family:hasParent;
                   rdfs:range         family:Mother.
```
### Gleichbedeutende Klasse und Eigenschaften (SameAs)
* Für **Instanzen** wird `sameAs` und `differentFrom` verwendet
* Für **Klassen** wird `equivalentClass` verwendet
* Für **Eigenschaften** wird `equivalentProperty` verwendet

```sql
@prefix : <http://example.com/owl/families/>.
@prefix otherOnt: <http://example.org/other/families/>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

:Mary         owl:sameAs                otherOnt:MaryBrown.
:John         owl:sameAs                otherOnt:JohnBrown.
:Adult        owl:equivalentClass       otherOnt:Grownup.
:hasChild     owl:equivalentProperty    otherOnt:child.
:hasAge       owl:equivalentProperty    otherOnt:age.
```
