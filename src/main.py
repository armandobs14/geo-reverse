from src.malha.malha import get_address
from typing import Optional
from fastapi import FastAPI
import json
import os

app = FastAPI()


@app.get("/reverse/{x}/{y}")
def read_item(x: float, y: float, q: Optional[str] = None):
    return get_address(x, y)
