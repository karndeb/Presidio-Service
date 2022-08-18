## Presidio-As-A-Service

### Steps to run the Presidio analyzer

`docker build -t presidio/analyzer --build-arg NAME=presidio-analyzer --build-arg NLP_CONF_FILE=conf/default.yaml --no-cache .` <br>

`docker run -d --name presidio-analyzer -p 3000:3000 presidio/analyzer`

### Check the logs 

`docker logs -t presidio-analyzer`

### Steps to run the Presidio anonymizer

`docker build -t presidio/anonymizer --build-arg NAME=presidio-anonymizer --no-cache .`

`docker run -d --name presidio-anonymizer -p 3000:3000 presidio/anonymizer`

### Check the logs 

`docker logs -t presidio-anonymizer`