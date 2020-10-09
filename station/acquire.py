import logging
import uuid
import datetime
import time
import psycopg2
import psycopg2.extras

from sensors import bme680
import config

## Enable logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

## Create sensors
bme680 = bme680.Sensor(uuid.uuid4()) #temperature, pressure, rel. humidity, gas resistance
si1145 = si1145.Sensor(uuid.uuid4()) #ir, visible, uv levels

## Configure Postgre
psycopg2.extras.register_uuid() # Allow uuid in postgre

bme680.acq()
for o in bme680.observables:
    o.read()

si1145.acq()
for o in si1145.observables:
    o.read()
