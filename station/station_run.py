from pathlib import Path
import sqlite3
from datetime import datetime
import time
import SI1145.SI1145 as SI1145


#conn = sqlite3.connect('./measurements.db')

# looking for db

current_dir = Path('.')
db_dir = current_dir / 'db'
db_file = db_dir / 'measurements.db'

if not db_dir.exists() or not db_dir.is_dir():
	db_dir.mkdir()

db_conn = sqlite3.connect(db_file)
db = db_conn.cursor()

# db.execute('''
# CREATE TABLE measurements
# (timestamp text, value text, unit text, kind text, comment text)
# ''')

# UV sensor setup 
sensor = SI1145.SI1145(busnum=1)

# Data acquisition

print('Press Cntrl + Z to cancel')

while True:
        timestamp = str(datetime.now())
        vis = sensor.readVisible()
        IR = sensor.readIR()
        UV = sensor.readUV()
        uvIndex = UV 
        print('Vis:             ', str(vis))
        print('IR:              ', str(IR))
        print('UV:              ', str(uvIndex))

        # db.execute("INSERT INTO measurements VALUES (timestamp, str(vis), 'AU', 'Visible light intensity', '-')")
        # db.execute("INSERT INTO measurements VALUES (timestamp, str(IR), 'AU', 'IR light intensity', '-')")
        # db.execute("INSERT INTO measurements VALUES (timestamp, str(uvIndex), 'AU', 'UV index', '-')")


        si1145data = [
                (timestamp, str(vis), 'AU', 'Visible light intensity', '-'),
                (timestamp, str(IR), 'AU', 'IR light intensity', '-'),
                (timestamp, str(uvIndex), 'AU', 'UV index', '-')]

        db.executemany('INSERT INTO measurements VALUES (?,?,?,?,?)', si1145data)
        db_conn.commit()
        
        time.sleep(1)
