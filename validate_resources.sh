#!/bin/bash

DIR="resources"
SCHEMA_RESOURCES="schemas/resources.schema.json"
SCHEMA_NESTED="schemas/nested_resources.schema.json"

echo "Validating all resources in $DIR/..."
jsonschema -i $DIR/resources.json $SCHEMA_RESOURCES
jsonschema -i $DIR/nested_resources.json $SCHEMA_NESTED
echo "... done!"
