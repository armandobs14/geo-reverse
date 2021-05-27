from src.malha.malha import get_address
from typing import Optional
from fastapi import FastAPI
import json
import os


class App:
    def api():
        app = FastAPI()

        @app.get("/reverse/{x}/{y}")
        async def read_item(x: float, y: float, q: Optional[str] = None):
            return get_address(x, y)

        return app

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


app = App.api() if os.environ["APPLICATTION"] == "API" else App.kafka_consumer()
