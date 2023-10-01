from fastapi import FastAPI
import uvicorn
import uuid
import logging
import hazelcast
from hazelcast.core import HazelcastJsonValue
import os
from pydantic import BaseModel
from typing import Union
import logging
import hazelcast


logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Items API", openapi_url="/openapi.json")


logging.basicConfig(level=logging.INFO)

hazelcast_address = os.environ.get('hazelcast_address', 'localhost:5701')

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

    def id(self):
        return self.name
client = hazelcast.HazelcastClient(cluster_members=[hazelcast_address])

# Initialize the client configuration
#config = hazelcast.ClientConfig()
# Use the hazelcast_address for the network configuration
#config.network_config.addresses.append(hazelcast_address)
# Start the Hazelcast client with the provided configuration
#client = hazelcast.HazelcastClient(config)
items_map = client.get_map("items").blocking()


@app.get("/items/{item_id}", status_code=200)
async def read_item(item_id: str):
    t = items_map.get(item_id)
    print(t)
    return items_map.get(item_id)


@app.post("/items/", status_code=200)
async def create_item(item: Item):
    id = uuid.uuid4()
    items_map.put(id, HazelcastJsonValue(item.model_dump()))
    return id


@app.get("/items/")
def read_all_item():
    return items_map.key_set()






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
    # uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 --log-level info
    print("I am here.")