# CKAN Harvesting Sources for Piattaforma Digitale Nazionale Dati (PDND) - previously DAF

[![Join the #pdnd-ckan channel](https://img.shields.io/badge/Slack%20channel-%23pdnd--ckan-blue.svg?logo=slack)](https://developersitalia.slack.com/messages/CMX9ZDPK3)
[![Get invited](https://slack.developers.italia.it/badge.svg)](https://slack.developers.italia.it/)
[![PDND/DAF on forum.italia.it](https://img.shields.io/badge/Forum-PDND-blue.svg)](https://forum.italia.it/c/daf)

CKAN is a powerful data management system that makes data accessible – by providing tools to streamline publishing, sharing, finding and using data. CKAN is a key component consumed by the PDND project. This repository collects all open data sources PDND harvests.

## What is PDND?

PDND stays for "Piattaforma Digitale Nazionale Dati" (the Italian Digital Data Platform), previously known as Data & Analytics Framework (DAF).

You can find more informations about the PDND on the official [Digital Transformation Team website](https://teamdigitale.governo.it/it/projects/daf.htm).

## How to import these resources

Install, setup and run CKAN from [the official repository](https://github.com/italia/ckan-it).

1. Run `bash import_all.sh` (assuming CKAN is running on localhost:5000).
2. Browse to [http://localhost:5000/organization](http://localhost:5000/organization) to check all imported organizations
3. Browse to [http://localhost:5000/harvest](http://localhost:5000/harvest) to check all imported sources

## How to run CKAN harvesting

1. Identify the name of the CKAN Container and run the following command: `containerid=$(docker ps | grep dati-ckan-docker_ckan | awk '{print $11}') && docker exec -it $containerid /periodic-harvest-run.sh && docker exec -it $containerid /periodic-harvester-joball.sh` where in `$containerid` there is the name of the container as per `docker ps` command output

You can see logs during harvesting import with following command: `docker logs ckan -f`. Specific logs are in `/var/log/ckan` folder inside the container.

### Run CKAN periodic harvesting

Schedule a CRON job on the host machine to run the `/periodic-harvest.sh` script at the root of the file system of the CKAN container.

How to do this really depends on how you run the containers. When running containers with docker-compose for instance we did this by getting the container id and using `docker-exec` to run a command inside the container, as follows:

```
containerid=`docker ps | grep dati-ckan-docker_ckan | awk '{print $11}'`
docker exec -it $containerid /periodic-harvest-run.sh 2>&1 /var/log/periodic-harvest-run.out
docker exec -it $containerid /periodic-harvester-joball.sh 2>&1 /var/log/periodic-harvest-joball.out
```

So you can schedule a periodic run of the above script every 15 minutes with CRON on the host machine.

## How to contribute

Contributions are welcome. Feel free to open issues and submit a pull request at any time!
