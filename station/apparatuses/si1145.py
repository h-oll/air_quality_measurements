import logging
import SI1145.SI1145 as Sensor
import uuid
import types
from datetime import datetime

from .observable import Observable
from .observation import format_observation
from .apparatus import Apparatus

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def read_ir(self):
    return format_observation(self, self.apparatus.sensor.readIR())

def read_vi(self):
    return format_observation(self, self.apparatus.sensor.readVisible())

def read_uv(self):
    return format_observation(self, self.apparatus.sensor.readUV())
  
class SI1145(Apparatus):
    def __init__(self, uuid):
        super().__init__('SI1145', uuid)

        try:
            self.sensor = Sensor.SI1145(busnum=1)
            logger.info(f'Apparatus initialized.')                            
        except:
            logger.critical('Failed to initialize apparatus, cannot connect to sensor.')
            raise NameError('Failed to initialize apparatus, cannot connect to sensor.')

        self.ir = Observable('1111', 'AU', 'Infrared', 'IR', 'raw', self)
        self.vi = Observable('1111', 'AU', 'Visible', 'Vis', 'raw', self)
        self.uv = Observable('1111', 'AU', 'Ultraviolet', 'UV', 'raw', self)

        self.ir.read_observation = types.MethodType(read_ir, self.ir)
        self.vi.read_observation = types.MethodType(read_vi, self.vi)
        self.uv.read_observation = types.MethodType(read_uv, self.uv)
                            
        self.observables = [self.ir, self.vi, self.uv]
        logger.info('3 Observables available.')
                            
    def observe(self): 
        pass
        
    
