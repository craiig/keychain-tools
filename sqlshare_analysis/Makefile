

all: ./build/sqlshare_data_release1/queries.txt

build/:
	mkdir -p $@

./build/sqlshare_data_release1.zip: build/
	cd build && wget https://s3-us-west-2.amazonaws.com/sqlsharedatarelease1/sqlshare_data_release1.zip

./build/sqlshare_data_release1/queries.txt: ./build/sqlshare_data_release1.zip build/
	unzip -d build $< sqlshare_data_release1/queries.txt
