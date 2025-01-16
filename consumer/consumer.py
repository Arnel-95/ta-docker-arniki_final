import os
import pika
import json
from pymongo import MongoClient

#Sleep for 1 Minute
import time
time.sleep(60)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "AAPL")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")

# Verbindung zu RabbitMQ
params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Verbindung zu MongoDB
mongo_client = MongoClient(MONGODB_URL)
db = mongo_client.stockmarket
collection = db.stocks

def process_messages(messages):
    # messages ist eine Liste von (channel, method, properties, body)
    prices = []
    company_name = None
    for _, method, _, body in messages:
        data = json.loads(body)
        prices.append(data["price"])
        company_name = data["company"]
    
    if len(prices) > 0:
        avg_price = sum(prices) / len(prices)
        # upsert (falls schon ein Eintrag für company existiert, updaten wir den avgPrice)
        collection.update_one(
            {"company": company_name},
            {"$set": {"avgPrice": avg_price}},
            upsert=True
        )



def main():
    batch_size = 1000
    messages_buffer = []

    for method_frame, properties, body in channel.consume(queue=QUEUE_NAME, auto_ack=True):
        messages_buffer.append((channel, method_frame, properties, body))
        
        if len(messages_buffer) >= batch_size:
            process_messages(messages_buffer)
            messages_buffer = []

if __name__ == "__main__":
    main()
