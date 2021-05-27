from osgeo import ogr
import os


def update(context_list, index):
    aux = context_list[index]
    context_list.remove(aux)
    context_list.insert(0, aux)


def get_bbox(poly):
    """
    Returns a polygon of the bounding rectangle of an input polygon.
    Parameters
    ----------
    poly
        An ogr.Geometry object containing a polygon

    Returns
    -------
    An ogr.Geometry object with a four-point polygon representing the bounding rectangle.

    """
    aoi_bounds = ogr.Geometry(ogr.wkbLinearRing)
    x_min, x_max, y_min, y_max = poly.GetEnvelope()
    aoi_bounds.AddPoint(x_min, y_min)
    aoi_bounds.AddPoint(x_max, y_min)
    aoi_bounds.AddPoint(x_max, y_max)
    aoi_bounds.AddPoint(x_min, y_max)
    aoi_bounds.AddPoint(x_min, y_min)
    bounds_poly = ogr.Geometry(ogr.wkbPolygon)
    bounds_poly.AddGeometry(aoi_bounds)
    return bounds_poly


# load shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
shape_path = os.environ["SHAPE_PATH"] if "SHAPE_PATH" in os.environ else "/tmp/shape"
path = f"{shape_path}/BR_Municipios_2019.shp"
cityShapefile = driver.Open(path)
cities = []
boundaries = []

# loading layers
cityLayer = cityShapefile.GetLayer()

# caching cities
for i in range(cityLayer.GetFeatureCount()):
    city = cityLayer.GetFeature(i)
    cities.append(city)
    boundaries.append(get_bbox(city.geometry()))


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

    for index, boundary in enumerate(boundaries):
        if boundary.Contains(point):
            if cities[index].geometry().Contains(point):
                update(cities, index)
                update(boundaries, index)
                return cities[0].items()

    if index == len(cities):
        return None