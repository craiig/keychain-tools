
SPARK_JARS = "/Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/*"

TESTCLASS := build/org/apache/spark/HashTesting/Constants1.class
all: ${TESTCLASS}

${TESTCLASS}: test_cases/constants-1.scala
	scalac -d build/ -classpath ${SPARK_JARS} $<

shell:
	scala -classpath ${SPARK_JARS}:build/ 

test: ${TESTCLASS}
	scala -classpath ${SPARK_JARS}:build/ org.apache.spark.HashTesting.Constants1

clean: 
	-rm ${TESTCLASS}
