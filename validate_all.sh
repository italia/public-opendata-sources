#!/bin/bash

DIR="dist"
SCHEMA_ALL="schemas/all.schema.json"
SCHEMA_NESTED="schemas/nested.schema.json"

echo "Validating all files in $DIR/..."
jsonschema -i $DIR/index.json $SCHEMA_ALL
jsonschema -i $DIR/nested/index.json $SCHEMA_NESTED
echo "... done!"
