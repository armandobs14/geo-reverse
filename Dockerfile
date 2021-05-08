FROM continuumio/miniconda3:4.9.2-alpine



COPY src /app/src
ADD requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN apk add --no-cache curl bash unzip && \
    curl https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_municipios_20200807.zip --output /tmp/shape.zip && \
    unzip /tmp/shape.zip -d /tmp/shape && \
    rm /tmp/shape.zip && \
    pip3 install --no-cache uvicorn==0.13.4 fastapi==0.63.0 kafka-python==2.0.2 && \
    conda install --yes --file /tmp/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
