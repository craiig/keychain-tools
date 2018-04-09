
all: build/resilience_outcome.json

build/resilience_outcome.json: ./resilience_programs.js resilience_templates.py ./resilience_test.py build/
	./resilience_test.py -f resilience_programs.js -o build/ -r $@

.PHONY: test
test: ./build/resilience_outcome.json ./test/resilience_check_regressions.py
	./test/resilience_check_regressions.py -o ./test/resilience_outcome.json -n $<

charts: ./build/resilience_outcome.json test ./charts.py
	./charts.py -o build/ -f build/resilience_outcome.json
	
build/:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -rf build/
