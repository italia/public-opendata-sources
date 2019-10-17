#!/bin/bash

DIR="orgs"
SCHEMA="orgs.schema.json"

echo "Validating all organizations in $DIR/..."
for f in $DIR/*; do
    jsonschema -i "$f" $SCHEMA
done
echo "... done!"
