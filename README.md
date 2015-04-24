D2RQ_to_R2RML
=============

Python script that converts D2RQ mapping documents to R2RML mapping documents

Usage
-----
You can run a conversion by executing the following command:
    
    python D2RQ_to_R2RML.py -i <inputFile> -o <ouptutFile>

With 
    
    <inputFile> = The D2RQL mapping document 
    <outputFile> = The corresponding R2RML mapping document

Features
--------
Non-supported D2R(Q) Classes and Propertes (because they are out-of-scope for R2RML):

d2r:Server

d2rq:Database

| D2RQ                   | R2RML                  		     | 
| -----------------------|:-----------------------------------------:| 
| d2rq:ClassMap          | rr:TriplesMap          		     |
| d2rq:PropertyBridge    | rr:PredicateObjectMap  		     |
| d2rq:class             | rr:class               		     |
| d2rq:uriPattern        | rr:template            		     |
| d2rq:uriPattern        | ~rr:logicalTable (deducted) 		     |
| d2rq:belongsToClassMap | ~rr:predicateObjectMap (inverse)	     |
| d2rq:property          | rr:property		  		     |
| d2rq:properties	 | rr:predicate .., ..,.. 		     |
| d2rq:dynamicProperty   | rr:PredicateMap        		     |
| d2rq:column		 | rr:column		  		     |
| d2rq:uriColumn	 | rr:column "..." ; rr:termType rr:IRI      |
| d2rq:datatype		 | rr:datatype		  		     |
| d2rq:lang		 | rr:language		  		     |
| d2rq:pattern		 | rr:template "...", rr:termType rr:Literal |
| d2rq:uriColumn	 | rr:column "...", rr:termType rr:IRI       |
| d2rq:refersToClassMap  | rr:parentTriplesMap			     |
| d2rq:join		 | rr:joinCondition (only if equality)       |

More Information
----------------

More information about the solution can be found at http://rml.io

This application is developed by Multimedia Lab http://www.mmlab.be

Copyright 2015, Multimedia Lab - Ghent University - iMinds

License
-------

The RMLProcessor is released under the terms of the [MIT license](http://opensource.org/licenses/mit-license.html).
