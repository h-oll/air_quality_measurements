import configparser
from .observation import Observation
#from .observation import format_observation

class Observable:
    def __init__(self, uuid, unit, name, short_name, kind, apparatus):
        self.uuid = uuid
        self.unit = unit
        self.name = name
        self.short_name = short_name
        self.kind = kind
        self.apparatus = apparatus

    # def read_observation(self, short_name):
    #     observation = format_observation(self, self.apparatus.data[short_name])
    #     return observation

    def get_observation(self):
        return Observation(self)


    def db_create(self):
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
            cur.execute(sql, (self.uuid, self.unit, self.name, self.short_name, self.kind, self.apparatus.uuid))
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
