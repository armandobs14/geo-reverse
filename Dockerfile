FROM alpine as builder


COPY src /app/src
ADD requirements.txt /tmp/requirements.txt

WORKDIR /app

# Conainer depencencies
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py-pip \
    build-base \
    alpine-sdk \
    gcc \
    geos \
    gdal-dev \
    curl \
    bash \
    unzip

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip \
    && pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==$(gdal-config --version) \
    && pip install --no-cache -r /tmp/requirements.txt \
    && curl https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_municipios_20200807.zip --output /tmp/shape.zip \
    &&  unzip /tmp/shape.zip -d /tmp/shape \
    && rm /tmp/shape.zip

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
