# SFX-COVID-19

This docker image converts the raw COVID-19 data provided by Johns Hopkins CSSE Repository https://github.com/CSSEGISandData/COVID-19 into datapoints that can be ingested by signalFX.

## Build
Run the below to build the image
```
docker build -t <repo/name:tag> .
```

## Notes
In case of a restart and in order to not fully re-sync historical datapoints, the monitor persists the date of last sync into a file under /opt .
Make sure you start the container by creating a volume map between the host location and /opt to persist the file between restarts.
I noticed that CSSE Repository is getting updated multiple times a day and some of the updates adjust the values of previous datapoints;  SFX  
In SFX adjusting a datapoint with older timestamp is not permitted, when this happens the only solution is to start a new sync with a new `covid-version`
## Run
Run the below command after replacing \<xxxxx\> with the actual value
```
docker run -it --env SFX_ACCESS_TOKEN=<sfx_access_token> --env COVID_VERSION=<covid-version> -v </location/on/host/where/file/resides>:/opt/ <repo/name:tag>
```
`COVID_VERSION` env variable to set the version of the MTSes
`INGEST_URL` optional env variable; can be used to set the ingest URL. Default is: https://ingest.signalfx.com

## Metrics
| Metric | Type |
| --- | --- |
|`covid-19-confirmed`|Cumulative Counter|
|`covid-19-recovered`|Cumulative Counter|
|`covid-19-deaths`|Cumulative Counter|

## Dimensions
| Dimenstion | Description |
| --- | --- |
|`covid-version`|The version of the MTSes. Make sure to filter your charts by version |
|`Province-State`||
|`Country-Region`||
|`Lat`||
|`Long`||