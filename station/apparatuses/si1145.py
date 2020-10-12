import logging
import SI1145.SI1145 as Sensor
import uuid
from datetime import datetime, timezone
import configparser

from .observable import Observable
from .apparatus import Apparatus

logger = logging.getLogger(__name__)

class SI1145(Apparatus):
    def __init__(self, apparatus_uuid):
        super().__init__('SI1145', apparatus_uuid)

        try:
            self.sensor = Sensor.SI1145(busnum=1)
            logger.info(f'Apparatus initialized.')                            
        except:
            logger.critical('Failed to initialize apparatus, cannot connect to sensor.')
            raise NameError('Failed to initialize apparatus, cannot connect to sensor.')

        self.data = {"ir":None, "vi":None, "uv":None}

        config = configparser.ConfigParser()
        config.read('configuration.ini')
        
        self.ir = Observable(uuid.UUID(config["observables"]["SI1145.ir"]), 'AU', 'Infrared', 'ir', 'raw', self)
        self.vi = Observable(uuid.UUID(config["observables"]["SI1145.vi"]), 'AU', 'Visible', 'vi', 'raw', self)
        self.uv = Observable(uuid.UUID(config["observables"]["SI1145.uv"]), 'AU', 'Ultraviolet', 'uv', 'raw', self)

        self.observables = [self.ir, self.vi, self.uv]
        logger.info('3 Observables available.')
        
    def observe(self): 
        self.data["ir"] = self.sensor.readIR()
        self.data["vi"] = self.sensor.readVisible()
        self.data["uv"] = self.sensor.readUV()
        self.data["time"] = datetime.fromtimestamp(datetime.now().timestamp(), tz=timezone.utc)
        for i in self.data: 
            logger.debug(f'outcome: {self.data[i]}, short_name: {i}')
