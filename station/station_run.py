#from pathlib import Path
#import sqlite3

import psycopg2
import psycopg2.extras
psycopg2.extras.register_uuid()
from config import config

import uuid
from datetime import datetime
import time
import SI1145.SI1145 as SI1145
import bme680


# #conn = sqlite3.connect('./measurements.db')

# # looking for db

# current_dir = Path('.')
# db_dir = current_dir / 'db'
# db_file = db_dir / 'measurements.db'

# if not db_dir.exists() or not db_dir.is_dir():
# 	db_dir.mkdir()

# db_conn = sqlite3.connect(db_file)
# db = db_conn.cursor()

# # db.execute('''
# # CREATE TABLE measurements
# # (timestamp text, value text, unit text, kind text, comment text)
# # ''')

def insert_observations(observations):
    """ insert new observations """
    sql = """INSERT INTO observations(id, time, value, unit) VALUES(%s, %s, %s, %s)"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, observations)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# UV sensor setup 
uv_sensor = SI1145.SI1145(busnum=1)

# Air Quality, Temp, Pressure, RH sensor setup
try:
    aq_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    aq_sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

aq_sensor.set_humidity_oversample(bme680.OS_2X)
aq_sensor.set_pressure_oversample(bme680.OS_4X)
aq_sensor.set_temperature_oversample(bme680.OS_8X)
aq_sensor.set_filter(bme680.FILTER_SIZE_3)
aq_sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

aq_sensor.set_gas_heater_temperature(320)
aq_sensor.set_gas_heater_duration(150)
aq_sensor.select_gas_heater_profile(0)

    
# Data acquisition

print('Press Cntrl + Z to cancel')

while True:
        timestamp = str(datetime.now())
        vis = uv_sensor.readVisible()
        IR = uv_sensor.readIR()
        UV = uv_sensor.readUV()
        uvIndex = UV 
        print('Vis:             ', str(vis))
        print('IR:              ', str(IR))
        print('UV:              ', str(uvIndex))

        # db.execute("INSERT INTO measurements VALUES (timestamp, str(vis), 'AU', 'Visible light intensity', '-')")
        # db.execute("INSERT INTO measurements VALUES (timestamp, str(IR), 'AU', 'IR light intensity', '-')")
        # db.execute("INSERT INTO measurements VALUES (timestamp, str(uvIndex), 'AU', 'UV index', '-')")

        si1145data = [
                (uuid.uuid4(), timestamp, vis, 'AU - Visible light intensity'),
                (uuid.uuid4(), timestamp, IR, 'AU - IR light intensity'),
                (uuid.uuid4(), timestamp, uvIndex, 'AU - UV index')]

        insert_observations(si1145data)
        
        if aq_sensor.get_sensor_data():
                output = '{0:.2f} C | {1:.2f} hPa | {2:.2f} %RH'.format(
                        aq_sensor.data.temperature,
                        aq_sensor.data.pressure,
                        aq_sensor.data.humidity)

                if aq_sensor.data.heat_stable:
                        print('{0} | {1} Ohms'.format(
                                output,
                                aq_sensor.data.gas_resistance))

                        bme680data = [
                                (uuid.uuid4(), timestamp, aq_sensor.data.temperature, 'C - Temperature'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.pressure, 'hPa - Pressure'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.humidity, '% - Relative Humidity'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.gas_resistance, 'Ohm - Gas resistance')]
                        insert_observations(bme680data)
                
                else:
                        print(output)
                        bme680data = [
                                (uuid.uuid4(), timestamp, aq_sensor.data.temperature, 'C - Temperature'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.pressure, 'hPa - Pressure'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.humidity, '% - Relative Humidity'),
                                (uuid.uuid4(), timestamp, aq_sensor.data.gas_resistance, 'Ohm - Gas resistance')]
                        insert_observations(bme680data)

        # db.executemany('INSERT INTO measurements VALUES (?,?,?,?,?)', si1145data)
        # db_conn.commit()

        # db.executemany('INSERT INTO measurements VALUES (?,?,?,?,?)', bme680data)
        # db_conn.commit()


        

        time.sleep(1)
