import logging
import bme680
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
    return format_read_value(self, self.sensor.data.temperature)

def read_pres(self):
    return format_read_value(self, self.sensor.data.pressure)

def read_relh(self):
    return format_read_value(self, self.sensor.data.humidity)

def read_gasr(self):
    if self.sensor.data.heat_stable:
        return format_read_value(self, self.sensor.data.gas_resistance)
    else:
        return format_read_value(self, None)

class Sensor:
    def __init__(self, uuid):
        self.uuid = uuid
        self.name = 'BME680'
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

            logger.info('Sensor initialized.')
                            
        except:
            logger.critical('Cannot connect to sensor.')
            raise NameError('Cannot connect to sensor.')

        self.temp = Observable('1111', 'C', 'Temperature', 'Temp', 'raw', self.sensor)
        self.pres = Observable('1111', 'hPa', 'Pressure', 'Pres', 'raw', self.sensor)
        self.relh = Observable('1111', '%', 'Relative Humidity', 'RH', 'raw', self.sensor)
        self.gasr = Observable('1111', 'Ohms', 'Gas Resistance', 'Gas Res', 'raw', self.sensor)

        temp.read = types.MethodType(read_temp, temp)
        pres.read = types.MethodType(read_pres, pres)
        relh.read = types.MethodType(read_relh, relh)
        gasr.read = types.MethodType(read_gasr, gasr)
                            
        self.observables = [temp, pres, relh, gasr]
        logger.info('4 Observables available.')
                            
    def acq(self): 
        self.sensor.get_sensor_data()
