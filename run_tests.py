#!/usr/bin/env python

# run test cases, gather HLS hash traces, and present results
# expected pass/fail numbers are important but this is all largely
# written to help characterize what kind of behaviour we can expect on the JVM
# perhaps in the future we can expand this to also work for LLVM
#
#

def run_test(test_case):

    :require /Users/craig/Documents/School-UBC/Code/spark-private/core/target/spark-core_2.11-2.2.1-SNAPSHOT.jar
    :require /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/

    :require /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/JavaEWAH-0.3.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/RoaringBitmap-0.5.11.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/ST4-4.0.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/activation-1.1.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/antlr-2.7.7.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/antlr-runtime-3.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/antlr4-runtime-4.5.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/aopalliance-1.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/aopalliance-repackaged-2.4.0-b34.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/apache-log4j-extras-1.2.17.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/apacheds-i18n-2.0.0-M15.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/apacheds-kerberos-codec-2.0.0-M15.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/api-asn1-api-1.0.0-M20.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/api-util-1.0.0-M20.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/arpack_combined_all-0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/asm-5.0.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/asm-tree-5.0.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/asm-util-5.0.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/avro-1.7.7.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/avro-ipc-1.7.7.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/avro-mapred-1.7.7-hadoop2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/base64-2.3.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/bcprov-jdk15on-1.51.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/bonecp-0.8.0.RELEASE.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/breeze-macros_2.11-0.13.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/breeze_2.11-0.13.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/calcite-avatica-1.2.0-incubating.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/calcite-core-1.2.0-incubating.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/calcite-linq4j-1.2.0-incubating.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/chill-java-0.8.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/chill_2.11-0.8.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-beanutils-1.7.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-beanutils-core-1.8.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-cli-1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-codec-1.10.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-collections-3.2.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-compiler-3.0.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-compress-1.4.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-configuration-1.6.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-crypto-1.0.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-dbcp-1.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-digester-1.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-httpclient-3.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-io-2.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-lang-2.6.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-lang3-3.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-logging-1.1.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-math3-3.4.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-net-2.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/commons-pool-1.5.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/compress-lzf-1.0.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/core-1.1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/curator-client-2.6.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/curator-framework-2.6.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/curator-recipes-2.6.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/datanucleus-api-jdo-3.2.6.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/datanucleus-core-3.2.10.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/datanucleus-rdbms-3.2.9.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/derby-10.12.1.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/eigenbase-properties-1.1.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/gson-2.2.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/guava-14.0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/guice-3.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/guice-servlet-3.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-annotations-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-auth-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-client-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-common-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-hdfs-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-mapreduce-client-app-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-mapreduce-client-common-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-mapreduce-client-core-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-mapreduce-client-jobclient-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-mapreduce-client-shuffle-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-yarn-api-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-yarn-client-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-yarn-common-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-yarn-server-common-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hadoop-yarn-server-web-proxy-2.7.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hive-beeline-1.2.1.spark2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hive-cli-1.2.1.spark2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hive-exec-1.2.1.spark2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hive-jdbc-1.2.1.spark2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hive-metastore-1.2.1.spark2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hk2-api-2.4.0-b34.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hk2-locator-2.4.0-b34.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/hk2-utils-2.4.0-b34.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/honest-profiler-1.0-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/htrace-core-3.1.0-incubating.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/httpclient-4.5.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/httpcore-4.4.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/ivy-2.4.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-annotations-2.6.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-core-2.6.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-core-asl-1.9.13.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-databind-2.6.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-jaxrs-1.9.13.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-mapper-asl-1.9.13.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-module-paranamer-2.6.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-module-scala_2.11-2.6.5.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jackson-xc-1.9.13.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/janino-3.0.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/java-xmlbuilder-1.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javassist-3.18.1-GA.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javax.annotation-api-1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javax.inject-1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javax.inject-2.4.0-b34.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javax.servlet-api-3.1.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javax.ws.rs-api-2.0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/javolution-5.5.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jaxb-api-2.2.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jcl-over-slf4j-1.7.16.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jdo-api-3.0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-client-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-common-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-container-servlet-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-container-servlet-core-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-guava-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-media-jaxb-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jersey-server-2.22.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jets3t-0.9.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jetty-6.1.26.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jetty-util-6.1.26.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jline-2.12.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/joda-time-2.9.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jodd-core-3.5.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jpam-1.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/json4s-ast_2.11-3.2.11.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/json4s-core_2.11-3.2.11.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/json4s-jackson_2.11-3.2.11.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jsp-api-2.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jsr305-1.3.9.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jta-1.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jtransforms-2.4.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/jul-to-slf4j-1.7.16.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/kryo-shaded-3.0.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/leveldbjni-all-1.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/libfb303-0.9.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/libthrift-0.9.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/log4j-1.2.17.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/lz4-1.3.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/machinist_2.11-0.6.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/macro-compat_2.11-1.1.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/mail-1.4.7.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/metrics-core-3.1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/metrics-graphite-3.1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/metrics-json-3.1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/metrics-jvm-3.1.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/minlog-1.3.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/mx4j-3.0.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/netty-3.9.9.Final.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/netty-all-4.0.43.Final.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/objenesis-2.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/opencsv-2.3.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/oro-2.0.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/osgi-resource-locator-1.0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/paranamer-2.6.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-column-1.8.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-common-1.8.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-encoding-1.8.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-format-2.3.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-hadoop-1.8.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-hadoop-bundle-1.6.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/parquet-jackson-1.8.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/pmml-model-1.2.15.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/pmml-schema-1.2.15.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/protobuf-java-2.5.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/py4j-0.10.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/pyrolite-4.13.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scala-compiler-2.11.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scala-library-2.11.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scala-parser-combinators_2.11-1.0.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scala-reflect-2.11.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scala-xml_2.11-1.0.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/scalap-2.11.8.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/shapeless_2.11-2.3.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/slf4j-api-1.7.16.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/slf4j-log4j12-1.7.16.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/snappy-0.2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/snappy-java-1.1.2.6.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-catalyst_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-core_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-graphx_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-hive-thriftserver_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-hive_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-launcher_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-mllib-local_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-mllib_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-network-common_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-network-shuffle_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-repl_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-sketch_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-sql_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-streaming_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-tags_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-unsafe_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spark-yarn_2.11-2.2.1-SNAPSHOT.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spire-macros_2.11-0.13.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/spire_2.11-0.13.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/stax-api-1.0-2.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/stax-api-1.0.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/stream-2.7.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/stringtemplate-3.2.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/super-csv-2.2.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/univocity-parsers-2.2.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/validation-api-1.1.0.Final.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/xbean-asm5-shaded-4.4.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/xercesImpl-2.9.1.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/xmlenc-0.52.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/xz-1.0.jar /Users/craig/Documents/School-UBC/Code/spark-private/assembly/target/scala-2.11/jars/zookeeper-3.4.6.jar

run_test("./test_cases/constants-1.scala")
