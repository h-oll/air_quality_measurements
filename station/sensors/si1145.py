import logging
import SI1145.SI1145 as SI1145
import uuid
import types

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class Observable:
    def __init__(self, uuid, unit, name, short_name, kind, sensor):
        self.uuid = uuid
        self.unit = unit
        self.name = name
        self.short_name = short_name
        self.kind = kind
        self.sensor = sensor

def format_read_value(observable, value):
    logger.info(f'time: {str(datetime.now())}, value: {value}, unit: {observable.unit}, short_name: {observable.short_name}.')
    return {
        "time": str(datetime.now()),
        "value": value,
        "unit": observable.unit,
        "name": observable.name,
        "short_name": observable.short_name,
        "kind": observable.kind,
        "sensor_uuid": observable.sensor.uuid,
        "sensor_name": observable.sensor.name              
    }
    
def read_temp(self):
    return format_read_value(self, self.sensor.readIR())

def read_pres(self):
    return format_read_value(self, self.sensor.readVisible())

def read_relh(self):
    return format_read_value(self, self.sensor.readUV())
  
class Sensor:
    def __init__(self, uuid):
        self.uuid = uuid
        self.name = 'SI1145'
        try:
            self.sensor = SI1145.SI1145(busnum=1)
            logger.info('Sensor initialized.')                            
        except:
            logger.critical('Cannot connect to sensor.')
            raise NameError('Cannot connect to sensor.')

        self.ir = Observable('1111', 'AU', 'Infrared', 'IR', 'raw', self.sensor)
        self.vi = Observable('1111', 'AU', 'Visible', 'Vis', 'raw', self.sensor)
        self.uv = Observable('1111', 'AU', 'Ultraviolet', 'UV', 'raw', self.sensor)


        ir.read = types.MethodType(read_ir, temp)
        vi.read = types.MethodType(read_vi, pres)
        uv.read = types.MethodType(read_uv, relh)

                            
        self.observables = [ir, vi, uv]
        logger.info('3 Observables available.')
                            
    def acq(self): 
        pass
