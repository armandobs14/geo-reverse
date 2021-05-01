# geo-reverse

Simple REST service for find city from latitude and longitude using shape files

## running with docker

```bash
# build image
docker build -t reverse .

# run container
docker run -d --name reverse -p 80:8000 reverse
```

## running with docker-compose

```bash
# run container
docker-compose up -d
```

## Request location

```bash
# request location
curl localhost:80/reverse/-41.45861/-4.42472
```

The response must be like

```json
{ "ibge_code": "2207900", "city": "Pedro II", "uf": "PI", "area_km2": 1544.565 }
```
