import logging
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
print(os.path.dirname(__file__))
from kafka import KafkaConsumer, KafkaProducer

try:
    from src.malha.malha import get_address
except:
    from malha.malha import get_address

logging.basicConfig(filename="reverse.log", level=logging.INFO)

from typing import Optional
from fastapi import FastAPI


def api():
    app = FastAPI()

    @app.get("/reverse/{x}/{y}")
    async def read_item(x: float, y: float, q: Optional[str] = None):
        return get_address(x, y)


def kafka_consumer():
    logging.info("Connecting with kafka")
    consumer = KafkaConsumer(
        "locations",
        group_id="geo_reverse",
        bootstrap_servers=os.environ["KAFKA_BROKERCONNECT"],
    )
    producer = KafkaProducer(
        bootstrap_servers=os.environ["KAFKA_BROKERCONNECT"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    logging.info("Conected to kafka")
    for message in consumer:
        position = json.loads(message.value)
        address = get_address(float(position["x"]), float(position["y"]))

        if address is not None:
            position.update(address)
            producer.send("locations_processed", position)

        logging.debug(position)


if __name__ == "__main__":
    kafka_consumer()
    # api()
