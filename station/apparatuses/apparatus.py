import psycopg2
import psycopg2.extras
import configparser
import logging 

logger = logging.getLogger(__name__)

class Apparatus:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid
        self.observables = [] 
        
    def observe(self):
        logger.critical('Observe method not implemented.')
        raise NameError('Observe method not implemented.')
        
    
    def get_observations(self):
        # for o in self.observables:
        #     o.read_observation(o.short_name)
        return [o.get_observation() for o in self.observables]
        

    def db_create_apparatus(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')

        sql = """
INSERT INTO apparatuses(uuid, name, station_uuid) 
VALUES (%s, %s, %s)
"""
        conn = None
        try:
            params = config["postgresql"]
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(sql, (self.uuid, self.name, config["station"]["uuid"]))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def db_create_observables(self):
        config = configparser.ConfigParser()
        config.read('configuration.ini')

        sql = """
INSERT INTO observables(uuid, unit, name, short_name, kind, apparatus_uuid) 
VALUES (%s, %s, %s, %s, %s, %s)
"""
        conn = None
        try:
            params = config["postgresql"]
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.executemany(sql, [(o.uuid, o.unit, o.name, o.short_name, o.kind, o.apparatus.uuid) for o in self.observables])
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
