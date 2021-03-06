import psycopg2
import psycopg2.extras
import configparser
import uuid

from apparatuses.bme680 import BME680
from apparatuses.si1145 import SI1145
from apparatuses.veml6070 import VEML6070

config = configparser.ConfigParser()
config.read('configuration.ini')

psycopg2.extras.register_uuid()

def create_tables():
    sql_statements = [
        """CREATE TABLE stations (
        uuid UUID,
        name VARCHAR,
        mobile BOOLEAN, 
        PRIMARY KEY (uuid)
) ""","""
        CREATE TABLE apparatuses (
        uuid UUID,
        name VARCHAR,
        station_uuid UUID,
        PRIMARY KEY (uuid),
        FOREIGN KEY (station_uuid) REFERENCES stations(uuid) ON UPDATE CASCADE
) ""","""
CREATE TABLE observables (
        uuid UUID,
        unit VARCHAR,
        name VARCHAR, 
        short_name VARCHAR, 
        kind VARCHAR, 
        apparatus_uuid UUID,
        PRIMARY KEY (uuid),
        FOREIGN KEY (apparatus_uuid) REFERENCES apparatuses(uuid) ON UPDATE CASCADE
)  ""","""
CREATE TABLE observations (
        uuid UUID,
        time TIMESTAMP,
        outcome FLOAT8,
        observable_uuid UUID,
        PRIMARY KEY (uuid),
        FOREIGN KEY (observable_uuid) REFERENCES observables(uuid) ON UPDATE CASCADE
) """
    ]
    conn = None
    try:
        params = config["postgresql"]
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for statement in sql_statements: cur.execute(statement)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def create_station():
    sql = """
INSERT INTO stations(uuid, name, mobile) 
VALUES (%s, %s, %s)"""
# ON CONFLICT (uuid)
# DO UPDATE SET name = EXCLUDED.name, mobile = EXCLUDED.mobile;
# """
    conn = None
    try:
        params = config["postgresql"]
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (uuid.UUID(config["station"]["uuid"]), config["station"]["name"], config["station"]["mobile"]))
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
       print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    # create_tables()

    # create_station()
        
    # bme680 = BME680(uuid.UUID(config["apparatuses"]["BME680"]))
    # bme680.db_create()
    # for o in bme680.observables: o.db_create()

    # si1145 = SI1145(uuid.UUID(config["apparatuses"]["SI1145"]))
    # si1145.db_create()
    # for o in si1145.observables: o.db_create()

    # veml6070 = VEML6070(uuid.UUID(config["apparatuses"]["VEML6070"]))
    # veml6070.db_create()
    # for o in veml6070.observables: o.db_create()
    
    print('done')
