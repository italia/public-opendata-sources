# Italian Public Open Data Sources

[![Join the #pdnd-ckan channel](https://img.shields.io/badge/Slack%20channel-%23pdnd--ckan-blue.svg?logo=slack)](https://developersitalia.slack.com/messages/CMX9ZDPK3)
[![Get invited](https://slack.developers.italia.it/badge.svg)](https://slack.developers.italia.it/)
[![PDND/DAF on forum.italia.it](https://img.shields.io/badge/Forum-PDND-blue.svg)](https://forum.italia.it/c/daf)

This repository aims to collect and share an updated list of Italian public open data sources as complete as possible in both human- and machine-readable formats.

It is also the official repository of harvesting sources for [CKAN-IT](https://github.com/italia/ckan-it) when configured as open data harvester,
ie. within the [Piattaforma Digitale Nazionale Dati (PDND) - previously DAF](https://pdnd.italia.it/).
CKAN-IT provides everything you need to run CKAN plus a set of extensions for supporting Italian open data in a set of Docker images.
If you are interested in an open data catalogue up and running in minutes, see [italia/ckan-it](https://github.com/italia/ckan-it).

## Entities: organizations and harvesting sources

There are two entities: an organization and a harvesting source. Both are described by a json file compliant with the schemas provided.
In `orgs/` folder there are all organizations. In `sources/` folder, all harvesting sources.

Before importing or just after exporting you should check compliance with schemas in `schemas/` folder using two provided scripts.
You must have Python3 and the [jsonschema module](https://pypi.org/project/jsonschema/) installed in your system.

* Organizations: `bash validate_orgs.sh`
* Sources: `bash validate_sources.sh`

If you want to run them in a virtual environment, a Pipfile is provided to use with [pipenv](https://pipenv.kennethreitz.org/en/latest/).
If you have pipenv, just run `pipenv shell` and then `pipenv install` before launch the validation scripts.

You can combine all entities from `orgs/` and `sources/` folders in single json files using `export_all.py` script that creates two files in `dist/` folder:

* `index.json` with a list of organizations and sources per organization;
* `nested/index.json` with a deeper nested object (see [#6](https://github.com/italia/public-opendata-sources/issues/6) for details).

To validate them you can use the provided `validate_all.sh` script.

### Naming convention

Organizations:

* the name of the organization should be the extended version if there is also an acronym, ie. MIUR -> Ministero dell'istruzione, dell'università e della ricerca, especially if in the name there is also a category term (ie. "Ministero")
* some organizations are known mainly by their acronym, ie. INPS, so it's ok to use it, but use description field for the extended name, ie. Istituto Nazionale Previdenza Sociale
* here are some category terms to maintain in organization names:
  * "Comune di"
  * "Provincia di"
  * "Provincia autonoma di"
  * "Regione"
  * "Ministero di"
  * "Città metropolitana di"
  * "Università di"

Harvesting sources:

* the name should following this rule:
  * "Catalogo open data " followed by its own name, if present, or the name of organization (also the acronym if present)
  * "Catalogo federato " followed by the name of organization (also the acronym if present)
  * "Geoportale " followed by the name of organization (also the acronym if present)
* if source is not harvestable by CKAN-IT, use `#` for the url field

The following different types of harvesters are currently supported.

* **CKAN** (`ckan`): this type of harvesting enables the metadata exchange between two instances of standard CKAN with no specific extensions enabled, it uses the [APIs version 3 offered by CKAN](https://docs.ckan.org/en/2.6/api/index.html) and it can be used when both instances do not comply with any specific national standards.

* **CSW server (multilang)** (`multilang`): this type of harvesting imports geospatial metadata made available through the [CSW protocol](https://en.wikipedia.org/wiki/Catalogue_Service_for_the_Web), the [multilang extension](https://github.com/italia/ckanext-multilang) manages multilingual fields for datasets, groups, tags and organizations.

* **Generic DCAT RDF Harvester** (`dcat_rdf`): this type of harvestings allows you to collect metadata that are described using the RDF ([Resource Description Framework](https://en.wikipedia.org/wiki/Resource_Description_Framework)) Web standard, following the [DCAT specifications](https://www.w3.org/TR/2018/WD-vocab-dcat-2-20180508/). It is used in order to harvest data sources that are compliant with [DCAT-AP_IT](https://docs.italia.it/italia/daf/linee-guida-cataloghi-dati-dcat-ap-it/it/stabile/dcat-ap_it.html), an extension we built upon the [CKAN's DCAT RDF harvester](https://github.com/ckan/ckanext-dcat).

* **DCAT JSON Harvester** (`dcat_json`): this type of harvesting is used when `data.json` metadata files are provided by data sources. The data.json is an API endpoint for describing open data catalogs by leveraging the [U.S. Project Open Data metadata schema standards](https://project-open-data.cio.gov/v1.1/schema/) and usually data management systems like Socrata and DKAN offer such an endpoint. Therefore, this type of harvest can be used in all those cases in which Socrata or DKAN platforms are used at data sources. This type of harvesting comes with the earlier mentioned CKAN's DCAT RDF harvester.

* **CKAN Harvester for DCATAPIT** (`CKAN-DCATAPIT`): this type of harvesting enables the metadata exchange between two instances of standard CKAN, dealing with some requirements of the DCAT-AP_IT specifications (e.g., mapping on the 13 data themes and on licences controlled vocabulary). This harvesting should be used when a DCAT-AP_IT compliant catalog wants to harvest a CKAN catalog of a data source that is not compliant with DCAT-AP_IT.

* **DCAT-AP_IT CSW Harvester** (`DCAT_AP-IT CSW Harvester`): this type of harvesting is used to collect metadata made available through the OGC CSW protocol. It is built upon the CKAN's spatial extension, and inherits all of its functionalities. This harvester allows you to harvest DCAT-AP_IT dataset fields from the ISO metadata. It is useful wben dealing with harvesting of open geospatial data.

## How to import orgs and sources in CKAN-IT

Install, setup and run CKAN from [the official repository](https://github.com/italia/ckan-it).

If you are ok with the official docker images provided, simply run them setting the environment variable `CKAN_HARVEST="true"`.
Read more [here](https://github.com/italia/ckan-it#ckan-it-harvesting-optional) for details.

Otherwise you can manually use the `import_all.sh` script on a running instance of CKAN-IT.

1. Run `bash import_all.sh APIKEY HOST` where APIKEY is the API key of your admin user ([read more here](https://docs.ckan.org/en/2.6/api/index.html#authentication-and-api-keys) for details) and HOST is the CKAN host (ie. `localhost:5000`).
2. Browse to [http://localhost:5000/organization](http://localhost:5000/organization) to check all imported organizations
3. Browse to [http://localhost:5000/harvest](http://localhost:5000/harvest) to check all imported sources

Now follow [these steps](https://github.com/italia/ckan-it#ckan-it-harvesting-optional) to run CKAN-IT harvesting process.

## How to export your orgs and sources

If you are running a CKAN-IT instance with many harvesting sources defined (ie. using the web interface), you can export them all using `export_orgs.py` and `export_sources.py` scripts. You must have Python3 installed or use pipenv with provided Pipfile.

## How to contribute

Contributions are welcome. Feel free to open issues and submit a pull request at any time!
