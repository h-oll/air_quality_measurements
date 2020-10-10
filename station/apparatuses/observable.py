from .observation import Observation
#from .observation import format_observation

class Observable:
    def __init__(self, uuid, unit, name, short_name, kind, apparatus):
        self.uuid = uuid
        self.unit = unit
        self.name = name
        self.short_name = short_name
        self.kind = kind
        self.apparatus = apparatus

    # def read_observation(self, short_name):
    #     observation = format_observation(self, self.apparatus.data[short_name])
    #     return observation

    def get_observation(self):
        return Observation(self)
