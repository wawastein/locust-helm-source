# Locust Helm Chart

This chart installs [Locust](http://locust.io) instance for load testing using Kubernetes.
Based on stable/locust chart, this variation provides ability to override path to locustfile and uses more recent version of locust package (0.8.1 as of time of writing)

## Pre Requisites:

* Tested with helm `v2.8.2`

## Chart details

This chart will do the following:

* Convert file defined by values `locustFile.dir` + `locustFile.filename` into a configmap (dir and filename separation allows you to provide arbitrary path to file on your local file system without reworking templates so the app can find them inside container)
* Create a Locust master and Locust worker deployment with the Target host
  and Tasks file specified.


### Installing the chart

To install the chart with the release name `locust`:
1. Clone this repository
2. Create your locustfile, place it in a directory inside this chart
3. Run
```bash
helm install -n locust --set targetHost=http://example.com --set locustFile.dir="my_dir" --set locustFile.filename="my_locust.py" . 
```
**PSA**
Unfortunately user cannot install this chart from external helm repository and use their local files, see [Issue](https://github.com/helm/helm/issues/3276).
This is also the biggest caveat of stable/locust chart as well as all values being hardcoded.

| Parameter                    | Description                             | Default                                               |
| ---------------------------- | ----------------------------------      | ----------------------------------------------------- |
| `Name`                       | Locust master name                      | `locust`                                              |
| `image.repository`           | Locust container image name             | `wawastein/locust`                                    |
| `image.tag`                  | Locust Container image tag              | `0.8.1`                                               |
| `image.pullSecrets`          | Locust Container image registry secret  | `None`                                                |
| `service.type`               | k8s service type exposing master        | `LoadBalancer`                                        |
| `service.nodePort`           | Port on cluster to expose master        | `0`                                                   |
| `service.annotations`        | KV containing custom annotations        | `{}`                                                  |
| `service.extraLabels`        | KV containing extra labels              | `{}`                                                  |
| `targetHost`                 | Locust target host                      | `http://example.com`                                  |
| `locustFile.dir`             | Directory which contains locustfile     | `tasks`                                               |
| `locustFile.filename`        | Locustfile name                         | `locustfile.py`                                       |
| `worker.replicaCount`        | Number of workers to run                | `2`                                                   |

Specify parameters using `--set key=value[,key=value]` argument to `helm install`

You can start the swarm from the command line using Port forwarding as follows:

Get the Locust URL following the Post Installation notes.

for example:
```bash
export LOCUST_URL=http://127.0.0.1:8089
```

Start / Monitor & Stop the Locust swarm via the web panel or with following commands:

Start:
```bash
curl -XPOST $LOCUST_URL/swarm -d"locust_count=100&hatch_rate=10"
```

Monitor:
```bash
watch -n 1 "curl -s $LOCUST_URL/stats/requests | jq -r '[.user_count, .total_rps, .state] | @tsv'"
```

Stop:
```bash
curl $LOCUST_URL/stop
```
