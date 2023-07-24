## Presidio-As-A-Service

Presidio (Origin from Latin praesidium ‘protection, garrison’) helps to ensure sensitive data is properly managed and governed. It provides fast identification and anonymization modules for private entities in text and images such as credit card numbers, names, locations, social security numbers, bitcoin wallets, US phone numbers, financial data and more.

Goals
 - Allow organizations to preserve privacy in a simpler way by democratizing de-identification technologies and introducing transparency in decisions.
 - Embrace extensibility and customizability to a specific business need.
 - Facilitate both fully automated and semi-automated PII de-identification flows on multiple platforms.

![Presidio Detection Flow]("https://github.com/karndeb/Presidio-Service/blob/main/detection_flow.gif")

This is a Fastapi wrapper service around the presidio module

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
