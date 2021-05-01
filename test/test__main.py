import pytest
import requests


def test_api():
    geo = (-41.45861, -4.42472)
    url = f"http://localhost/reverse/{geo[0]}/{geo[1]}"

    expected_response = {
        "ibge_code": "2207900",
        "city": "Pedro II",
        "uf": "PI",
        "area_km2": 1544.565,
    }

    current_response = requests.get(url).json()
    assert current_response == expected_response


def test_zero_zero():
    geo = (0, 0)
    url = f"http://localhost/reverse/{geo[0]}/{geo[1]}"

    expected_response = None

    current_response = requests.get(url).json()
    assert current_response == expected_response