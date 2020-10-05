import bme680

def init() :
    # Air Quality, Temp, Pressure, RH sensor setup
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except IOError:
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
 
    return sensor


def acq(sensor):
    if sensor.get_sensor_data():
        output = '{0:.2f} C | {1:.2f} hPa | {2:.2f} %RH'.format(
            aq_sensor.data.temperature,
            aq_sensor.data.pressure,
            aq_sensor.data.humidity)

        if aq_sensor.data.heat_stable:
            print('{0} | {1} Ohms'.format(
                output,
                aq_sensor.data.gas_resistance))

            bme680data = [
                (uuid.uuid4(), timestamp, aq_sensor.data.temperature, 'C - Temperature'),
                (uuid.uuid4(), timestamp, aq_sensor.data.pressure, 'hPa - Pressure'),
                (uuid.uuid4(), timestamp, aq_sensor.data.humidity, '% - Relative Humidity'),
                (uuid.uuid4(), timestamp, aq_sensor.data.gas_resistance, 'Ohm - Gas resistance')]
            insert_observations(bme680data)
                
        else:
            print(output)
            bme680data = [
                (uuid.uuid4(), timestamp, aq_sensor.data.temperature, 'C - Temperature'),
                (uuid.uuid4(), timestamp, aq_sensor.data.pressure, 'hPa - Pressure'),
                (uuid.uuid4(), timestamp, aq_sensor.data.humidity, '% - Relative Humidity'),
                (uuid.uuid4(), timestamp, aq_sensor.data.gas_resistance, 'Ohm - Gas resistance')]
            insert_observations(bme680data)
