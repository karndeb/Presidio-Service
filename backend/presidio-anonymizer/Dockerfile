FROM tiangolo/uvicorn-gunicorn:python3.8

ARG NAME
WORKDIR /usr/bin/${NAME}

COPY ./presidio-anonymizer-requirements.txt /usr/bin/${NAME}/
RUN pip install -r /usr/bin/${NAME}/presidio-anonymizer-requirements.txt \
    && rm -rf /root/.cache/pip

COPY . /usr/bin/${NAME}/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]