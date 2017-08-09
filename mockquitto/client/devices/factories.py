from mockquitto.client.devices.gps import GPS
from mockquitto.client.devices.luminocity import LuminocityDevice
from mockquitto.client.devices.multipurpose import TempHumDevice, MultichannelADC
from mockquitto.client.devices.values import GPSCoordinates, Humidity, Temperature, Luxes, MilliVolts
from mockquitto.client.generator.laws import RandomReal, RandomInteger
from mockquitto.client.generator.generator import GeneratorInfinite


class IoTAcademyFactory:
    """
    Declare interface for operations that create products
    """

    @staticmethod
    def create_gps():
        coords_gps = GPSCoordinates(55.4507, 37.3656)
        gen_law_list = RandomReal(coords_gps[0], (-1, 1)), RandomReal(coords_gps[1], (-1, 1))
        generator = GeneratorInfinite(GPSCoordinates, gen_law_list, freq_value=0.5)
        return GPS(generator)

    @staticmethod
    def create_temp_hum():
        topic_bme280 = "devices/lora/807B85902000019A/bme280"
        gen_laws = RandomReal(20, 40), RandomInteger(0, 100)
        generators = GeneratorInfinite(Temperature, gen_laws[0], generator_name="Temperature", freq_value=0.5),\
                     GeneratorInfinite(Humidity, gen_laws[1], generator_name="Humidity", freq_value=0.5)
        return TempHumDevice(generators, topic=topic_bme280)

    @staticmethod
    def create_luminocity():
        topic_opt3001 = "devices/lora/807B85902000019A/opt3001"
        gen_law = RandomInteger(0, 65535)
        generator = GeneratorInfinite(Luxes, gen_law, freq_value=0.5)
        return LuminocityDevice(generator, topic=topic_opt3001)

    @staticmethod
    def create_adc():
        topic_adc = "devices/lora/807B85902000019A/adc"
        num_adc = 8
        gen_laws = [RandomInteger(0, 5000) for _ in range(0, num_adc)]
        generators = [GeneratorInfinite(MilliVolts, gl, generator_name="ADC_{}".format(num), freq_value=0.5) for
                      gl, num in zip(gen_laws, range(1, num_adc+1))]
        return MultichannelADC(generators, topic=topic_adc)

