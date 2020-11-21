import logging

import busio
import board
import adafruit_veml6070 as Sensor
import uuid
from datetime import datetime, timezone
import configparser

from .observable import Observable
from .apparatus import Apparatus

logger = logging.getLogger(__name__)

class VEML6070(Apparatus):
    def __init__(self, apparatus_uuid):
        super().__init__('VEML6070', apparatus_uuid)

        self.data = {"uv":None}

        config = configparser.ConfigParser()
        config.read('configuration.ini')
        
        self.uv = Observable(uuid.UUID(config["observables"]["VEML6070.uv"]), '\muW/cm^2', 'Ultraviolet', 'uv', 'raw', self)

        self.observables = [self.uv]
        logger.info('1 Observable available.')
        
    def observe(self): 
        with busio.I2C(board.SCL, board.SDA) as i2c:
            self.data["uv"] = Sensor.VEML6070(i2c).uv_raw
            self.data["time"] = datetime.fromtimestamp(datetime.now().timestamp(), tz=timezone.utc)
            for i in self.data: 
                logger.debug(f'outcome: {self.data[i]}, short_name: {i}')
