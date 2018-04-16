
all: build/resilience_outcome.json

build/resilience_outcome.json: ./resilience_programs.js resilience_templates.py ./resilience_test.py build/
	./resilience_test.py -f resilience_programs.js -o build/ -r $@

.PHONY: test
test: ./build/resilience_outcome.json ./test/resilience_check_regressions.py
	./test/resilience_check_regressions.py -o ./test/resilience_outcome.json -n $<

charts: ./build/resilience_outcome.json test ./charts.py ./build/hashing_time.pdf
	./charts.py -o build/ -f build/resilience_outcome.json

./build/hash_overhead.csv: ./hls_hash_summarize_traces.py
	./hls_hash_summarize_traces.py -f `find build/java -iname "*.bc"` `find build/scala -iname "*.bc"`  -o build/

./build/hashing_time.pdf: ./build/hash_overhead.csv ./hls_hash_plot_overheads.py
	./hls_hash_plot_overheads.py -c build/hash_overhead.csv -o build/
	
build/:
	mkdir -p $@

.PHONY: clean
clean:
	-rm -rf build/
