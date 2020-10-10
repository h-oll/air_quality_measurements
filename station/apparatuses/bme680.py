import logging
import bme680
import uuid
import types
from datetime import datetime
import configparser

from .observable import Observable
from .apparatus import Apparatus

logger = logging.getLogger(__name__)
    
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
            logger.info(f'Sensor initialized.')
        except:
            logger.critical('Failed to initialize sensor, cannot connect.')
            raise NameError('Failed to initialize sensor, cannot connect.')

        self.data = {"temp":None, "pres":None, "relh":None, "gasr":None, "tsta":None}

        config = configparser.ConfigParser()
        config.read('configuration.ini')
        
        self.temp = Observable(config["observables"]["BME680.temp"], 'C', 'Temperature', 'temp', 'raw', self)
        self.pres = Observable(config["observables"]["BME680.pres"], 'hPa', 'Pressure', 'pres', 'raw', self)
        self.relh = Observable(config["observables"]["BME680.relh"], '%', 'Relative Humidity', 'relh', 'raw', self)
        self.gasr = Observable(config["observables"]["BME680.gasr"], 'Ohms', 'Gas Resistance', 'gasr', 'raw', self)
        self.tsta = Observable(config["observables"]["BME680.tsta"], 'NA', 'Temperature stability', 'tsta', 'raw', self)

        self.observables = [self.temp, self.pres, self.relh, self.gasr, self.tsta]
        logger.info('5 Observables available.')
                            
    def observe(self): 
        self.sensor.get_sensor_data()        
        self.data["temp"] = self.sensor.data.temperature
        self.data["pres"] = self.sensor.data.pressure
        self.data["relh"] = self.sensor.data.humidity
        self.data["gasr"] = self.sensor.data.gas_resistance
        self.data["tsta"] = float(self.sensor.data.heat_stable)
        self.data["time"] = datetime.now()
        for i in self.data: 
            logger.debug(f'outcome: {self.data[i]}, short_name: {i}')
