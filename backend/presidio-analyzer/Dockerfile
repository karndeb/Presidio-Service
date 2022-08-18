FROM tiangolo/uvicorn-gunicorn:python3.8

ARG NAME
ARG NLP_CONF_FILE=conf/default.yaml
WORKDIR /usr/bin/${NAME}

COPY ./presidio-analyzer-requirements.txt /usr/bin/${NAME}/
RUN pip install -r /usr/bin/${NAME}/presidio-analyzer-requirements.txt \
    && rm -rf /root/.cache/pip
# install nlp models specified in conf/default.yaml
COPY ./install_nlp_models.py /usr/bin/${NAME}/
COPY ${NLP_CONF_FILE} /usr/bin/${NAME}/${NLP_CONF_FILE}
RUN python install_nlp_models.py --conf_file ${NLP_CONF_FILE}

COPY . /usr/bin/${NAME}/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]