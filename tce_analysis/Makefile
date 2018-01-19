#source https://cs.gmu.edu/~offutt/mujava/index-v3-nov2008.html
mujava_home := $(shell pwd)

mujava_dirs := ${mujava_home}/classes ${mujava_home}/result ${mujava_home}/src ${mujava_home}/testset

toolsjar := /Library/Java/JavaVirtualMachines/jdk1.8.0_66.jdk/Contents//Home/lib/tools.jar
CLASSPATH := ${CLASSPATH}:${mujava_home}/mujava-v3.jar:${mujava_home}/openjava2005.jar:${toolsjar}:${mujava_home}/classes

# these are the target set of mutants we wish to generate but we want to do this
# with one invocation of the GUI so we make it dependent on running the
# 'mutants' target
MUTANTS := result/Bisect/traditional_mutants/double_sqrt(double)/ \
	result/org.apache.commons.lang.WordUtils/traditional_mutants/java.lang.String_capitalize(java.lang.String,char)/ \
	result/org.apache.commons.lang.WordUtils/traditional_mutants/java.lang.String_wrap(java.lang.String,int,java.lang.String,boolean)/ \
	result/org.joda.time.chrono.BasicMonthOfYearDateTimeField/traditional_mutants/long_add(long,int)/ \
	result/pamvotis.core.Simulator/traditional_mutants/void_addNode(int,int,int,int,int,int)/ \
	result/pamvotis.core.Simulator/traditional_mutants/boolean_removeNode(int)/ \
	result/tr.Triangle/traditional_mutants/int_classify(int,int,int)/ \
	result/xcom.thoughtworks.xstream.io.xml.XmlFriendlyNameCoder/traditional_mutants/java.lang.String_decodeName(java.lang.String)/

# if we need to re-run make we do a submake targeting mutants which depends on
# all the source files. directly putting the sub-make call in all mutant
# targets results  in it being run once per file, but we desire one invocation
all: build/mutants 

# start the manual analysis workflow
.PHONY: analyze
analyze: build/tagged_programs.json build/final_analysis
	cat build/final_analysis

# call the mujava gui to generate mutants
$(MUTANTS):
	@echo Please use mujava GUI to generate $@

build/mutants: $(MUTANTS) | build/
	make mutants
	touch $@

# remove the relevant files from mujavas path so we can regenerate mutants
clean:
	-rm -rf classes/*
	-rm -rf src/*
	-rm -rf result/*

# download and parse listing of manually verified equivalent mutants
build/manual_analysis.html:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/equivalents.html

build/tagged_programs.json: build/manual_analysis.html build/mutants
	./do_manual_analysis.py -f $< -o $@ -m

build/final_analysis: build/tagged_programs.json
	./do_manual_analysis.py -o $< | tee $@

#source code examined by TCE
TCE_SOURCES := src/Bisect.java \
	src/org/apache/commons/lang/WordUtils.java \
	src/org/joda/time/chrono/BasicMonthOfYearDateTimeField.java \
	src/pamvotis/core/Simulator.java \
	src/tr/Triangle.java \
	src/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.java

build/Bisect.java:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/Bisect.java
	
src/Bisect.java: build/Bisect.java
	cp $< $@

#word utils can be a challenge to compile, these are the two needed files
classes/org/apache/commons/lang/WordUtils.class: build/commons-lang-2.4-src/target/classes/org/apache/commons/lang/WordUtils.class
	rsync -mra build/commons-lang-2.4-src/target/classes/ classes/ --include="WordUtils.class"

src/org/apache/commons/lang/WordUtils.java: build/commons-lang-2.4-src/src/java/org/apache/commons/lang/WordUtils.java
	rsync -mra build/commons-lang-2.4-src/src/java/ src/ --include="WordUtils.java" --include "*/" --exclude="*"

#how to build the rest of commons-lang to produce the above two files
build:/
	mkdir -p build

build/commons-lang-2.4-src/target/classes/org/apache/commons/lang/WordUtils.class: build/commons-lang-2.4-src/src/java/org/apache/commons/lang/WordUtils.java
	cd build/commons-lang-2.4-src/ && mvn compile

build/commons-lang-2.4-src/src/java/org/apache/commons/lang/WordUtils.java: build/commons-lang.zip
	unzip -o build/commons-lang.zip -d build/
	touch $@

build/commons-lang.zip:
	curl -L -o build/commons-lang.zip http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/commons-lang.zip

#joda time needed files
# note that classes have dependent classes so they must all be included (but we can make sure we only include the target source file)
classes/org/joda/time/chrono/BasicMonthOfYearDateTimeField.class: build/joda-time-2.4/target/classes/org/joda/time/chrono/BasicMonthOfYearDateTimeField.class
	rsync -mra build/joda-time-2.4/target/classes/ classes/ --include="BasicMonthOfYearDateTimeField.class" 

src/org/joda/time/chrono/BasicMonthOfYearDateTimeField.java: build/joda-time-2.4/src/main/java/org/joda/time/chrono/BasicMonthOfYearDateTimeField.java
	rsync -mra build/joda-time-2.4/src/main/java/ src/ --include="BasicMonthOfYearDateTimeField.java" --include "*/" --exclude="*"

#joda time benchmark supporting materials
build/joda-time.zip:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/joda-time.zip

build/joda-time-2.4/src/main/java/org/joda/time/chrono/BasicMonthOfYearDateTimeField.java: build/joda-time.zip
	unzip -o build/joda-time.zip -d build/
	touch $@

build/joda-time-2.4/target/classes/org/joda/time/chrono/BasicMonthOfYearDateTimeField.class:
	cd build/joda-time-2.4 && mvn compile

# pamvotis benchmark:
src/pamvotis/core/Simulator.java: build/pamvotis/src/pamvotis/core/Simulator.java
	rsync -mra build/pamvotis/src/ src/ --include="Simulator.java" --include "*/" --exclude="*"

# pamvotis lacks a build system so we just use a lame way to get it compiled
classes/pamvotis/core/Simulator.class: build/pamvotis/src/pamvotis/core/Simulator.java
	find build/pamvotis -iname "*.java" -exec javac {} -d classes/ -sourcepath build/pamvotis/src/ -classpath build/pamvotis/lib/xercesImpl.jar:build/pamvotis/lib/xml-apis.jar \;

# pamvotis benchmark supporting materials
build/pamvotis.zip:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/pamvotis.zip

build/pamvotis/src/pamvotis/core/Simulator.java:
	unzip -o build/pamvotis.zip -d build/
	touch $@

# triangle benchmark needs to go in the right spot
src/tr/Triangle.java: build/Triangle/src/tr/Triangle.java
	mkdir -p src/tr
	cp $< $@

classes/tr/Triangle.java: src/tr/Triangle.java
	javac $< -d classes/

# triangle benchmark supporting materials
build/triangle.zip:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/triangle.zip

build/Triangle/src/tr/Triangle.java:
	unzip -o build/triangle.zip -d build/

# xstream benchmark:
src/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.java: build/xstream/src/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.java
	rsync -mra build/xstream/src/ src/ --include="XmlFriendlyNameCoder.java" --include "*/" --exclude="*"

classes/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.class: build/xstream/src/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.java
	find build/xstream -iname "*.java" -exec javac {} -d classes/ -sourcepath build/xstream/src/ -classpath build/xstream/lib/\* \;

# xstream supporting materials
build/xstream.zip:
	curl -L -o $@ http://pages.cs.aueb.gr/~kintism/papers/tce/java_exp/manual-analysis/xstream.zip

build/xstream/src/xcom/thoughtworks/xstream/io/xml/XmlFriendlyNameCoder.java:
	unzip -o build/xstream.zip -d build/

#mujava setup
openjava2005.jar:
	curl -L -o $@ https://cs.gmu.edu/~offutt/mujava/openjava2005.jar

mujava-v3.jar:
	curl -L -o $@ https://cs.gmu.edu/~offutt/mujava/mujava-v3.jar

#MuJava_HOME=C:\offutt\mujava
mujava.config: | ${mujava_dirs}
	echo "MuJava_HOME=${mujava_home}" > $@
	touch $@

${mujava_dirs}:
	mkdir -p $@

#classes := $(patsubst src/%.java,classes/%.class,$(wildcard src/*.java))
classes := $(patsubst src/%.java,classes/%.class,$(TCE_SOURCES))
classes/%.class: src/%.java
	javac $< -d classes/

# starts tool to generate mutants
mutants: mujava.config $(classes) openjava2005.jar mujava-v3.jar $(TCE_SOURCES)
	CLASSPATH=${CLASSPATH} java mujava.gui.GenMutantsMain
