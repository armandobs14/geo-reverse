from osgeo import ogr
import os

# load shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
shape_path = os.environ["SHAPE_PATH"] if "SHAPE_PATH" in os.environ else "/tmp/shape"
path = f"{shape_path}/BR_Municipios_2019.shp"
cityShapefile = driver.Open(path)
cities = []

# loading layers
cityLayer = cityShapefile.GetLayer()

# caching cities
for i in range(cityLayer.GetFeatureCount()):
    cities.append(cityLayer.GetFeature(i))


def get_address(lng: float, lat: float):
    """
    Retrieves city info

    :param lng: longitude
    :param lat: latitude

    :return: dict with ibge_code, city name, uf and area or None

    """
    if lng == 0.0 and lat == 0.0:
        return None

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(lng, lat)

    for index, city in enumerate(cities):
        if city.geometry().Contains(point):
            aux = cities[index]
            cities.remove(aux)
            cities.insert(0, aux)
            break

    if city.geometry().Contains(point):
        return {
            "ibge_code": city.GetField("CD_MUN"),
            "city": city.GetField("NM_MUN"),
            "uf": city.GetField("SIGLA_UF"),
            "area_km2": city.GetField("AREA_KM2"),
        }
    else:
        return None