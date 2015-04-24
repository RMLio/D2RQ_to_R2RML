import sys,getopt
import rdflib, re
from rdflib import URIRef, BNode, RDF, Literal
from rdflib.namespace import XSD

g=rdflib.Graph()
newg=rdflib.Graph()

inputfile = ''
outputfile = ''

def main(argv):
   global inputfile, outputfile
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'python D2RQ_to_R2RML.py -i <D2RQ_mapDoc> -o <R2RML_mapDoc>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'python D2RQ_to_R2RML.py -i <D2RQ_mapDoc> -o <R2RML_mapDoc>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

if __name__ == "__main__":
    main(sys.argv[1:])

g.parse(inputfile, format="turtle")

for subject,predicate,object in g.triples( (None,  RDF.type, URIRef(u'http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#ClassMap')) ):
   #generates the SubjectMap
   logicalTableNode = subject + "_LogicalTable"
   newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'),URIRef(logicalTableNode)])
   newg.add([URIRef(logicalTableNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#LogicalTable')])
   subjectNode = subject + "_subjectMap"
   newg.add([subject, RDF.type, URIRef('http://www.w3.org/ns/r2rml#TriplesMap')])
   newg.add([subject, URIRef('http://www.w3.org/ns/r2rml#subjectMap'),subjectNode])
   newg.add([subjectNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#SubjectMap')])

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
         newg.add([URIRef(preNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#PredicateMap')])
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
         newg.add([objNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#RefObjectMap')])
         newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#parentTriplesMap'), obj])
         numJoins = 0
         for preObj,pre,obj in g.triples( (preObj,  URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#join'), None) ):
            joinNode = objNode + "_JoinMap_" + str(numJoins)
            numJoins = numJoins + 1
            newg.add([objNode, URIRef('http://www.w3.org/ns/r2rml#joinCondition'), URIRef(joinNode)])
            table = re.split(' |=',obj)
            newg.add([joinNode, RDF.type, URIRef('http://www.w3.org/ns/r2rml#Join')])
            #print subject
            for subject,pred,obj in newg.triples( (subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'), None) ):
               for obj,predd,tab in newg.triples( (obj, URIRef('http://www.w3.org/ns/r2rml#tableName'), None) ):
                  pp = re.compile( '.')
                  mm = re.search('(.+?)\.', table[0])
                  if str(mm.group(1)) == str(tab):
                     newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#parent'), Literal(table[len(table)-1])])
                     newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#child'), Literal(table[0])])
                  else:
                     newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#parent'), Literal(table[0])])
                     newg.add([URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#child'), Literal(table[len(table)-1])])

newg.serialize(outputfile,format='turtle')