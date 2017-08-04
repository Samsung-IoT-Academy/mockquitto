from mockquitto.client.devices.device import Device


class GPS(Device):
    def __init__(self):
        super().__init__(format="\"lat\":{0},\"lon\":{1}")

    def get(self):

        pass