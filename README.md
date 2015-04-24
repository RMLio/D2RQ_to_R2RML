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

| D2RQ                      | R2RML                  		      	     	     | 
| --------------------------|:------------------------------------------------------:| 
| d2rq:ClassMap             | rr:TriplesMap          		      	  	     |
| d2rq:PropertyBridge       | rr:PredicateObjectMap  		      	  	     |
| d2rq:class                | rr:class               		      	  	     |
| d2rq:uriPattern           | rr:template            		      	  	     |
| 		            | rr:logicalTable (deducted from uriPattern of ClassMap) |
| d2rq:belongsToClassMap    | ~rr:predicateObjectMap (inverse)	      	  	     |
| d2rq:refersToClassMap	    | 					      	  	     |
| d2rq:property             | rr:predicate	  		      	  	     |
| d2rq:properties	    | rr:predicate .., ..,.. 		      	  	     |
| d2rq:dynamicProperty      | rr:PredicateMap        		      	  	     |
| d2rq:constantValue	    | rr:constant				      	     |
| d2rq:column		    | rr:column		  		       	  	     |
| d2rq:uriColumn	    | rr:column "..." ; rr:termType rr:IRI      	     |
| d2rq:datatype		    | rr:datatype		  		      	     |
| d2rq:lang		    | rr:language		  		      	     |
| d2rq:pattern		    | rr:template "...", rr:termType rr:Literal 	     |
| d2rq:uriColumn	    | rr:column "...", rr:termType rr:IRI           	     |
| d2rq:refersToClassMap     | rr:parentTriplesMap			      	     |
| d2rq:join		    | rr:joinCondition (only if equality)		     |
| d2rq:condition	    | rr:joinCondition (only if equality)		     |
| d2rq:bNodeIdColumns	    | rr:termType rr:BlankNode (not supported yet)  	     |
| d2rq:Configuration	    | -- (out of scope for R2RML)	   	             |
| d2rq:Database		    | -- (out of scope for R2RML)		             |
| d2rq:DownloadMap	    | -- (out of scope for R2RML)		             |
| d2rq:AdditionalProperty   | -- (schema definition oriented)	      	  	     |
| d2rq:Translation	    | -- (not supported in R2RML)		      	     |
| d2rq:TranslationTable     | -- (not supported in R2RML)		      	     |
| d2rq:alias		    | -- (out of scope in R2RML)			     |
| d2rq:dataStorage	    | -- (out of scope for R2RML)			     |
| d2rq:containsDuplicates   | -- (out of scope for R2RML)			     |
| d2rq:classDefinitionLabel |--  (out of scope - schema definition oriented)	     |
| d2rq:classDefinitionComment | --  (out of scope - schema definition oriented)      |
| d2rq:propertyDefinitionLabel   | --  (out of scope - schema definition oriented)   |
| d2rq:propertyDefinitionComment | --  (out of scope - schema definition oriented)   |
| d2rq:sqlExpression	    | -- (not supported in R2RML)		 	     |
| d2rq:uriSqlExpression     | -- (not supported in R2RML)		      	     |
| d2rq:limit		    | -- (not supported in R2RML)		      	     |
| d2rq:limitInverse	    | -- (not supported in R2RML)		      	     |
| d2rq:orderAsc		    | -- (out of scope for R2RML)		      	     |
| d2rq:orderDesc	      | -- (out of scope for R2RML)		             |
| d2rq:valueMaxLength	      | -- (out of scope for R2RML)			     |
| d2rq:valueContains	      | -- (out of scope for R2RML)			     |
| d2rq:valueRegex	      | -- (out of scope for R2RML)			     |
		
	
More Information
----------------

More information about the solution can be found at http://rml.io

This application is developed by Multimedia Lab http://www.mmlab.be

Copyright 2015, Multimedia Lab - Ghent University - iMinds

License
-------

The RMLProcessor is released under the terms of the [MIT license](http://opensource.org/licenses/mit-license.html).
