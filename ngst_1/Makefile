

extract:
	MDEMO_HOME=`pwd` xfile --config extract_test_ng1.yaml --delimiter '|' --map testmap data_to_load.csv

run-pipeline-file:
	MDEMO_HOME=`pwd` xfile --config extract_test_ng1.yaml --delimiter '|' --map testmap data_to_load.csv | ngst --config ingest_test_ng1.yaml --target textfile
