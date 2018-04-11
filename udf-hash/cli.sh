#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
scala -classpath $DIR/target/udf-hash-1.0-SNAPSHOT.jar ca.ubc.ece.systems.HashCLI "$@"
