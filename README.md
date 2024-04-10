# hse_mlops airflow 
Airflow stack postgres and localstack .

## Minimum Requirements
This project supports Ubuntu Linux 18.04 and up. 
- [Docker 20.10 +](https://docs.docker.com/)
- [docker-compose  2.25.0 + ](https://docs.docker.com/compose/)

 # You must innit Airflow defore working with it by running . 

```bash
$ make init 
```
# You can run Airflow stack 

```bash
$ make run 
```

# You can stop Airflow stack 

```bash
$ make stop
```

# You can run local s3
```bash
$ make run_local_s3
```

# You can stop local s3
```bash
$ make stop_local_s3
```

### Jupiter notebook run in container and can be accessed on port 8888

 
