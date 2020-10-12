import logging
import uuid
import time
import configparser

import psycopg2
import psycopg2.extras

from apparatuses.bme680 import BME680
from apparatuses.si1145 import SI1145

## Enable logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

## Read configuration file
config = configparser.ConfigParser()
config.read('configuration.ini')

## Create apparatuses
logger.info(f'Found {len(config["apparatuses"])}: {config["apparatuses"]}')

if "BME680" in config["apparatuses"]:
    bme680 = BME680(uuid.UUID(config["apparatuses"]["BME680"])) #temperature, pressure, rel. humidity, gas resistance

if "SI1145" in config["apparatuses"]:
    si1145 = SI1145(uuid.UUID(config["apparatuses"]["SI1145"])) #ir, visible, uv levels

## Configure Postgre
psycopg2.extras.register_uuid() # Allow uuid in postgre


## Observable Insertion function
def insert_observations(observations):
    """ insert new observation """
    sql = """INSERT INTO observations(uuid, time, outcome, observable_uuid) VALUES(%s, %s, %s, %s)"""
    conn = None
    try:
        # read database configuration
        params = config["postgresql"]            
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, observations)
        # close communication with the database
        cur.close()
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

while True: 
    time.sleep(1)

    # Measure
    if "BME680" in config["apparatuses"]:
        bme680.observe()
    if "SI1145" in config["apparatuses"]:
        si1145.observe()

    # Get observations
    observations = []
    if "BME680" in config["apparatuses"]:
        observations = observations + bme680.get_observations()
    if "SI1145" in config["apparatuses"]:
        observations = observations + si1145.get_observations()

    # Insert observations in DB
    insert_observations([(o.uuid, o.time, o.outcome, o.observable.uuid) for o in observations])

        

