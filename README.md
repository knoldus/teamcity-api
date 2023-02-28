# DESCRIPTION

    This template is can be used to create a dataset of teamcity pipeline.
---

## Prerequiste

* api-token from teamcity server
* python environment

## Steps

### 0. Clone the source code from github

```bash
git clone https://github.com/knoldus/teamcity-api.git
cd teamcity-api/
```

### 1. create python virtual_env

```bash
python3 -m venv ./venv
source ./venv/bin/activate
```

### 2. install dependencies

```
pip3 -r install ./requirements.txt
```

### 3. create the dataset

```
python3 project_details.py
```

* Note: create a **.env** file with following data:
  * *token-value*
  * *server-url*
