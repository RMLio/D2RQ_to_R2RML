import rdflib, re
from rdflib import URIRef, BNode, RDF, Literal
from rdflib.namespace import XSD

g=rdflib.Graph()
newg=rdflib.Graph()
g.parse("EwiLodD2R_TM.n3", format="n3")
#g.load('http://dbpedia.org/resource/Semantic_Web')

len(g) # prints 2

for subject,predicate,object in g.triples( (None,  RDF.type, URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#ClassMap')) ):
   for subject,predicate,object in g.triples( (subject,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#dataStorage'), None) ):
      for object,predicate,database in g.triples( (object,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#jdbcDSN'), None) ):
         newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'),URIRef(database)])
         newg.add([URIRef(database), RDF.type, URIRef('http://www.w3.org/ns/r2rml#LogicalTable')])
         newg.add([URIRef(database), URIRef('http://www.w3.org/ns/r2rml#tableName'), Literal(database)])

   #generates the SubjectMap
   subjectNode = subject + "_subjectMap"
   newg.add([subject, RDF.type, URIRef('http://www.w3.org/ns/r2rml#TriplesMap')])
   newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#subjectMap'),subjectNode])
   #change @@*@@ to{*} and make it string if relative
   #newg.add([URIRef(subjectNode), URIRef('http://www.w3.org/ns/r2rml#template'),URIRef(object.replace("|urlencode",""))])
   if((subject,URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#class'),None) in g):
      for subject,predicate,object in g.triples( (subject,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None) ):
         newg.add([subjectNode, URIRef('http://www.w3.org/ns/r2rml#template'),URIRef(object.replace("|urlencode",""))])
      for subject,predicate,object in g.triples( (subject,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#class'), None) ):
   		newg.add([subjectNode, URIRef('http://www.w3.org/ns/r2rml#class'),URIRef(object)])

   for preObj,predicate,object in g.triples( (None,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#belongsToClassMap'), subject) ):
      newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#predicateObjectMap'), URIRef(preObj)])
      newg.add([preObj, RDF.type, URIRef('http://www.w3.org/ns/r2rml#PredicateObjectMap')])

      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#property'), None) ):
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#predicate'), obj])

      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#template'), URIRef(obj.replace("|urlencode",""))])

      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#column'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#column'), obj])
         print preObj
         for preObj,pre,datatype in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#datatype'), None) ):
            newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#datatype'), datatype])
         for preObj,pre,lang in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#lang'), None) ):
            print "language %s"%datatype
            newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#language'), lang])

newg.serialize("newMapping.r2rml.ttl",format='turtle')