# UDF Hashing Library
This library is will hash a given function reference and return a SHA256 hash
string.

# Installation
```
mvn install
```

# CLI Usage
A command line tool can be used to test basic and view debug json debug output:
```
./cli.sh ./path/to/compiled/class
```

# Library Usage
Add to your pom.xml:
```
	  <dependency>
        <groupId>ca.ubc.ece.systems</groupId>
        <artifactId>udf-hash</artifactId>
        <version>1.0-SNAPSHOT</version>
      </dependency>
```

Use it in your program:
```
import ca.ubc.ece.systems.ClosureHash

// to receive just the hash
	val hash:Option[String] = ClosureHash.hash(func)

// to receive the hash trace:
	val r:Option[(String, HashMap[String,Any])]  = ClosureHash.hashWithTrace(func)
	val hash =  r.map( (x) => {x._1} )
	val trace =  r.map( (x) => {x._2} )
```
