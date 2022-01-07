from btlewrap import BluepyBackend

from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY

class MiFlora:
    def __init__(self, mac: str):
        self.poller = MiFloraPoller(mac, BluepyBackend)

    def get_data(self):
        data = {
            'temp':       self.poller.parameter_value(MI_TEMPERATURE,False),
            'moist':      self.poller.parameter_value(MI_MOISTURE,False),
            'light':      self.poller.parameter_value(MI_LIGHT,False),
            'conduct':    self.poller.parameter_value(MI_CONDUCTIVITY,False),
            'battery':    self.poller.parameter_value(MI_BATTERY,False)
        }
        return data