
all: ./resilience_programs.js resilience_templates.py ./resilience_test.py build/
	./resilience_test.py -f resilience_programs.js -o build/ -r build/resilience_outcome.json
	
build/:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -rf build/
