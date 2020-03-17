# SFX-COVID-19

This docker image converts the raw COVID-19 data provided by Johns Hopkins CSSE Repository https://github.com/CSSEGISandData/COVID-19 into datapoints that can be ingested by signalFX.

## Build
Run the below to build the image
```
docker build -t <repo/name:tag> .
```

## Notes
In case of a restart and in order to not re-sync the historical datapoints, the monitor persistd the last data date we synced into a file under /opt .
Make sure you start the container by mapping the volume location on host to keep the file between restarts.
The monitor checks for new data every 1h, but the repo currently updates their data every 24 hours.
## Run
Run the below command after replacing \<xxxxx\> with the actual value
```
docker run -it --env SFX_ACCESS_TOKEN=<sfx_access_token>  -v </location/on/host/where/file/resides>:/opt/ <repo/name:tag>
```

`INGEST_URL` env variable can be used to set the ingest URL. Default is: https://ingest.signalfx.com

## Metrics
| Metric | Type |
| --- | --- |
|`covid-19-confirmed`|Cumulative Counter|
|`covid-19-recovered`|Cumulative Counter|
|`covid-19-deaths`|Cumulative Counter|

## Dimensions
| Dimenstion | Description |
| --- | --- |
|`covid-version`|The version of ths data set, currently is 'v1.0'|
|`Province-State`||
|`Country-Region`||
|`Lat`||
|`Long`||