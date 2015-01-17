import rdflib, re
from rdflib import URIRef, BNode, RDF, Literal
from rdflib.namespace import XSD

g=rdflib.Graph()
newg=rdflib.Graph()
g.parse("cerif.d2rq.n3", format="n3")

for subject,predicate,object in g.triples( (None,  RDF.type, URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#ClassMap')) ):
   #generates the SubjectMap
   logicalTableNode = subject + "_LogicalTable"
   print logicalTableNode
   newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'),URIRef(logicalTableNode)])
   newg.add([URIRef(logicalTableNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#LogicalTable')])
   subjectNode = subject + "_subjectMap"
   newg.add([subject, RDF.type, URIRef('http://www.w3.org/ns/r2rml#TriplesMap')])
   newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#subjectMap'),subjectNode])

   if((subject,URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#class'),None) in g):
      for subject,predicate,object in g.triples( (subject,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None) ):
         tableName = re.search('(.+?)\.', re.search('@@(.+?)@@', object).group(1)).group(1)
         newg.add([URIRef(logicalTableNode), URIRef('http://www.w3.org/ns/r2rml#tableName'),Literal(tableName)])
         p = re.compile( '@@(.+?)@@')
         #intermediate = p.search(object.replace("|urlencode","").replace("|urlify","")).group(1)
         new_obj = p.sub( r'{\1}', object.replace("|urlencode","").replace("|urlify",""))
         newg.add([subjectNode, URIRef('http://www.w3.org/ns/r2rml#template'),Literal(new_obj)])
      for subject,predicate,object in g.triples( (subject,  URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#class'), None) ):
   		newg.add([subjectNode, URIRef('http://www.w3.org/ns/r2rml#class'),URIRef(object)])

   for preObj,predicate,object in g.triples( (None,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#belongsToClassMap'), subject) ):
      newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#predicateObjectMap'), URIRef(preObj)])
      newg.add([preObj, RDF.type, URIRef('http://www.w3.org/ns/r2rml#PredicateObjectMap')])

      #generates rr:predicate
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#property'), None) ):
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#predicate'), obj])

      #generates rr:predicateMap
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#dynamicProperty'), None) ):
         preNode = obj + "_PreMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#predicateMap'), URIRef(preNode)])
         newg.add([URIRef(preNode), URIRef('http://www.w3.org/ns/r2rml#constant'), Literal(obj)])
         newg.add([URIRef(preNode), URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#IRI')])

      #template-valued object
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         p = re.compile( '@@(.+?)@@')
         new_obj = p.sub( r'{\1}', obj.replace("|urlencode","").replace("|urlify",""))
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#template'), Literal(new_obj)])

      #template-valued Literal object
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#pattern'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         p = re.compile( '@@(.+?)@@')
         new_obj = p.sub( r'{\1}', obj.replace("|urlencode","").replace("|urlify",""))
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#template'), Literal(new_obj)])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#Literal')])

      #constant-valued object
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#constantValue'), None) ):
         print obj
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#constant'), URIRef(obj.replace("|urlencode",""))])

      #column valued object
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#column'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#column'), obj])
         for preObj,pre,datatype in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#datatype'), None) ):
            newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#datatype'), datatype])
         for preObj,pre,lang in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#lang'), None) ):
            newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#language'), lang])

      #column valued URI object
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriColumn'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#column'), obj])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#IRI')])

      #Referencing object map
      for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#refersToClassMap'), None) ):
         objNode = preObj + "_ObjMap"
         newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), objNode])
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#parentTriplesMap'), obj])
         numJoins = 0
         for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#join'), None) ):
            joinNode = preObj + "_JoinMap_" + str(numJoins)
            numJoins = numJoins + 1
            newg.add([preObj, URIRef('http://www.w3.org/ns/r2rml#joinCondition'), URIRef(joinNode)])
            #TODO: better split parent and child
            table = re.split(' |=',obj)
            newg.add([joinNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#Join')])
            print tableName
            print table[0]
            print table[len(table)-1]
            newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#parent'), Literal(table[0])])
            newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#child'), Literal(table[len(table)-1])])

newg.serialize("cerif.r2rml.ttl",format='turtle')