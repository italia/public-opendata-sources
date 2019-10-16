# Italian Public Open Data Sources

[![Join the #pdnd-ckan channel](https://img.shields.io/badge/Slack%20channel-%23pdnd--ckan-blue.svg?logo=slack)](https://developersitalia.slack.com/messages/CMX9ZDPK3)
[![Get invited](https://slack.developers.italia.it/badge.svg)](https://slack.developers.italia.it/)
[![PDND/DAF on forum.italia.it](https://img.shields.io/badge/Forum-PDND-blue.svg)](https://forum.italia.it/c/daf)

This repository aims to collect and share an updated list of Italian public open data sources as complete as possible in both human- and machine-readable formats.

It is also the official repository of harvesting sources for [CKAN-IT](https://github.com/italia/ckan-it) when configured as open data harvester,
ie. within the [Piattaforma Digitale Nazionale Dati (PDND) - previously DAF](https://pdnd.italia.it/).

CKAN-IT provides everything you need to run CKAN plus a set of extensions for supporting Italian open data in a set of Docker images.
If you are interested in an open data catalogue up and running in minutes, see [italia/ckan-it](https://github.com/italia/ckan-it).

## How to import these resources in CKAN-IT

Install, setup and run CKAN from [the official repository](https://github.com/italia/ckan-it).

If you are ok with the official docker images provided, simply run them setting the environment variable `CKAN_HARVEST="true"`.
Read more [here](https://github.com/italia/ckan-it#ckan-it-harvesting-optional) for details.

Otherwise you can manually use the `import_all.sh` script on a running instance of CKAN-IT.

1. Run `bash import_all.sh APIKEY HOST` where APIKEY is the API key of your admin user ([read more here](https://docs.ckan.org/en/2.6/api/index.html#authentication-and-api-keys) for details) and HOST is the CKAN host (ie. `localhost:5000`).
2. Browse to [http://localhost:5000/organization](http://localhost:5000/organization) to check all imported organizations
3. Browse to [http://localhost:5000/harvest](http://localhost:5000/harvest) to check all imported sources

Now follow [these steps](https://github.com/italia/ckan-it#ckan-it-harvesting-optional) to run CKAN-IT harvesting process.

## How to export your resources

If you are running a CKAN-IT instance with many harvesting sources defined (ie. using the web interface), you can export them all using `orgs/export_orgs.py` and `sources/export_sources.py` scripts.

## How to contribute

Contributions are welcome. Feel free to open issues and submit a pull request at any time!
