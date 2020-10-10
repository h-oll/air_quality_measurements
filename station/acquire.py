import logging
import uuid
from datetime import datetime
import psycopg2
import psycopg2.extras

from apparatuses.bme680 import BME680
from apparatuses.si1145 import SI1145
import config

## Enable logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

## Create apparatuses
bme680 = BME680(uuid.uuid4()) #temperature, pressure, rel. humidity, gas resistance
si1145 = SI1145(uuid.uuid4()) #ir, visible, uv levels

## Configure Postgre
psycopg2.extras.register_uuid() # Allow uuid in postgre

bme680.observe()
si1145.observe()

bme680.get_observations()
si1145.get_observations()
