from numpy.random import normal

class HX711:
    def __init__(self, dout_pin=5, pd_sck_pin=6, gain=64, channel='A'):
        self.dout_pin = dout_pin
        self.pd_sck_pin = pd_sck_pin
        self.gain = gain
        self.channel = channel

    def get_raw_data(self, samples=5):
        return normal(500, 10, samples)

    def reset(self):
        pass