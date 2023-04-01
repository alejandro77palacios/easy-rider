import re
from datetime import datetime

from data import Data


class BusId(Data):
    def __init__(self, bus_id):
        self.bus_id = bus_id

    def check_type(self):
        return isinstance(self.bus_id, int)

    def check_required(self):
        return str(self.bus_id) != ''


class StopId(Data):
    def __init__(self, stop_id):
        self.stop_id = stop_id

    def check_type(self):
        return isinstance(self.stop_id, int)

    def check_required(self):
        return str(self.stop_id) != ''


class StopName(Data):
    def __init__(self, stop_name):
        self.stop_name = stop_name

    def check_type(self):
        return isinstance(self.stop_name, str)

    def check_required(self):
        return str(self.stop_name) != ''

    def check_format(self):
        test = re.search(r'^[A-Z].*(Road|Avenue|Boulevard|Street)$', self.stop_name)
        return bool(test)


class NextStop(Data):
    def __init__(self, next_stop):
        self.next_bus = next_stop

    def check_type(self):
        return isinstance(self.next_bus, int)

    def check_required(self):
        return str(self.next_bus) != ''


class StopType(Data):
    required = False

    def __init__(self, stop_type):
        self.stop_type = stop_type

    def check_type(self):
        return isinstance(self.stop_type, str) and len(self.stop_type) <= 1

    def check_required(self):
        return True

    def check_format(self):
        return self.stop_type in 'SOF'


class ArriveTime(Data):
    format = re.compile(r'^([01][0-9]|2[0-3]):[0-5][0-9]$')

    def __init__(self, arrive_time):
        self.arrive_time = arrive_time
        self.time = datetime.strptime(arrive_time, '%H:%M')

    def check_type(self):
        return isinstance(self.arrive_time, str)

    def check_required(self):
        return str(self.arrive_time) != ''

    def check_format(self):
        return bool(self.format.match(self.arrive_time))

    def __le__(self, other):
        return self.time <= other.time
