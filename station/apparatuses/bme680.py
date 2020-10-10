import logging
import bme680
import uuid
import types
from datetime import datetime

from .observable import Observable
from .observation import format_observation
from .apparatus import Apparatus

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
    
def read_temp(self):
    return format_observation(self, self.apparatus.sensor.data.temperature)

def read_pres(self):
    return format_observation(self, self.apparatus.sensor.data.pressure)

def read_relh(self):
    return format_observation(self, self.apparatus.sensor.data.humidity)
    
def read_gasr(self):
    return format_observation(self, self.apparatus.sensor.data.gas_resistance)

def read_tsta(self): 
    return format_observation(self, self.apparatus.sensor.data.heat_stable)
    
class BME680(Apparatus):
    def __init__(self, uuid):
        super().__init__('BME680', uuid)

        try: 
            try:
                self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
                logger.info(f'Sensor found at {bme680.I2C_ADDR_PRIMARY}.')
            except IOError:
                self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
                logger.info(f'Sensor found at {bme680.I2C_ADDR_SECONDARY}.')
            self.sensor.set_humidity_oversample(bme680.OS_2X)
            self.sensor.set_pressure_oversample(bme680.OS_4X)
            self.sensor.set_temperature_oversample(bme680.OS_8X)
            self.sensor.set_filter(bme680.FILTER_SIZE_3)
            self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
            self.sensor.set_gas_heater_temperature(320)
            self.sensor.set_gas_heater_duration(150)
            self.sensor.select_gas_heater_profile(0)
            logger.info(f'Apparatus initialized.')
        except:
            logger.critical('Failed to initialize apparatus, cannot connect to sensor.')
            raise NameError('Failed to initialize apparatus, cannot connect to sensor.')

        self.temp = Observable('1111', 'C', 'Temperature', 'Temp', 'raw', self)
        self.pres = Observable('1111', 'hPa', 'Pressure', 'Pres', 'raw', self)
        self.relh = Observable('1111', '%', 'Relative Humidity', 'RH', 'raw', self)
        self.gasr = Observable('1111', 'Ohms', 'Gas Resistance', 'Gas Res', 'raw', self)
        self.tsta = Observable('1111', 'NA', 'Temperature stability', 'Temp Stab', 'raw', self)
        
        self.temp.read_observation = types.MethodType(read_temp, self.temp)
        self.pres.read_observation = types.MethodType(read_pres, self.pres)
        self.relh.read_observation = types.MethodType(read_relh, self.relh)
        self.gasr.read_observation = types.MethodType(read_gasr, self.gasr)
        self.tsta.read_observation = types.MethodType(read_tsta, self.tsta)
                            
        self.observables = [self.temp, self.pres, self.relh, self.gasr, self.tsta]
        logger.info('5 Observables available.')
                            
    def observe(self): 
        self.sensor.get_sensor_data()        
