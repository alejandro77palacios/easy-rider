from datetime import datetime
from typing import List

from data_types import BusId, StopId, StopName, NextStop, StopType, ArriveTime


class Entry:
    fields = ['bus_id', 'stop_id', 'stop_name', 'next_stop', 'stop_type', 'a_time']

    def __init__(self, bus_id, stop_id, stop_name, next_stop, stop_type, a_time):
        self.bus_id = BusId(bus_id)
        self.stop_id = StopId(stop_id)
        self.stop_name = StopName(stop_name)
        self.next_stop = NextStop(next_stop)
        self.stop_type = StopType(stop_type)
        self.a_time = ArriveTime(a_time)

    def problem_summary(self) -> dict:
        return {field: getattr(self, field).problem() for field in self.fields}

    def get_bus_id(self):
        return self.bus_id.bus_id

    def get_stop_type(self):
        return self.stop_type.stop_type

    def get_stop_name(self):
        return self.stop_name.stop_name

    def get_time(self) -> datetime:
        return self.a_time.time

    def __le__(self, other):
        return self.get_time() <= other.get_time()


class ArrayEntries:
    def __init__(self, entries: List[Entry]):
        self.entries = entries

    def summary(self):
        # TODO cambiar
        summary = dict.fromkeys(('stop_name', 'stop_type', 'a_time'), 0)
        for entry in self.entries:
            problem = entry.problem_summary()
            for field in ('stop_name', 'stop_type', 'a_time'):
                # TODO cambiar por for field in summary:
                summary[field] += problem[field]
        total = sum(summary.values())
        print(f'Type and required field validation: {total} errors')
        for field in summary:
            print(f'{field}: {summary[field]}')

    def count_buses(self):
        count = {}
        for entry in self.entries:
            if entry.bus_id.bus_id not in count:
                count[entry.bus_id.bus_id] = 0
            count[entry.bus_id.bus_id] += 1
        print('Line names and number of stops:')
        for bus_id, count in count.items():
            print(f'bus_id: {bus_id}, stops: {count}')
        return count

    def analyse_stops(self):
        start = set()
        finish = set()
        stations: list = []
        stop = False
        last_stop_type = self.entries[0].get_stop_type()
        last_bus_id = self.entries[0].get_bus_id()
        for entry in self.entries:
            bus_id = entry.get_bus_id()
            stop_type = entry.get_stop_type()
            stop_name = entry.get_stop_name()
            if entry == self.entries[0]:
                last_bus_id = bus_id
                last_stop_type = stop_type
                if stop_type != 'S':
                    print(f'There is no start or end stop for the line: {bus_id}.')
                    stop = True
                    break
                else:
                    start.add(stop_name)
                    stations.append((bus_id, stop_name))
            elif last_stop_type == 'F':
                if bus_id == last_bus_id or stop_type != 'S':
                    print(f'There is no start or end stop for the line: {bus_id}.')
                    stop = True
                    break
                else:
                    start.add(stop_name)
                    stations.append((bus_id, stop_name))
                    last_stop_type = stop_type
                    last_bus_id = bus_id
            elif stop_type == 'S':
                if bus_id in start or last_stop_type != 'F' or last_bus_id == bus_id:
                    print(f'There is no start or end stop for the line: {last_bus_id}.')
                    stop = True
                    break
                else:
                    stations.append((bus_id, stop_name))
                    start.add(stop_name)
                    last_stop_type = stop_type
                    last_bus_id = bus_id
            elif stop_type == 'F':
                if bus_id not in finish and last_bus_id == bus_id:
                    stations.append((bus_id, stop_name))
                    finish.add(stop_name)
                    last_stop_type = stop_type
                    last_bus_id = bus_id
                else:
                    print(f'There is no start or end stop for the line: {bus_id}.')
                    stop = True
                    break
            else:
                stations.append((bus_id, stop_name))
                last_stop_type = stop_type
                last_bus_id = bus_id

        if not stop:
            transfer = set()
            unique_stations = set([pair[1] for pair in stations])
            for station in unique_stations:
                ids = set([pair[0] for pair in stations if pair[1] == station])
                if len(ids) > 1:
                    transfer.add(station)

            print(f'Start stops: {len(start)} {sorted(start)}')
            print(f'Transfer stops: {len(transfer)} {sorted(transfer)}')
            print(f'Finish stops: {len(finish)}, {sorted(finish)}')

    def analyse_times(self):
        print('Arrival time test:')
        previous_time = self.entries[0].get_time()
        last_bus_id = self.entries[0].get_bus_id()
        previous_wrong = False
        success = True
        for entry in self.entries:
            current_time = entry.get_time()
            bus_id = entry.get_bus_id()
            assert type(current_time) == type(previous_time)
            if entry == self.entries[0]:
                continue
            elif last_bus_id == bus_id:
                if previous_time > current_time and not previous_wrong:
                    print(f'bus_id line {bus_id}: wrong time on station {entry.get_stop_name()}')
                    previous_wrong = True
                    success = False
                else:
                    last_bus_id = bus_id
                    previous_time = current_time
                    previous_wrong = False
            else:
                last_bus_id = bus_id
                previous_time = current_time
                previous_wrong = False
        if success:
            print('OK')

    def analyse_on_demand(self):
        print('On demand stops test:')
        stop_types = [entry.get_stop_type() for entry in self.entries]
        stop_names = [entry.get_stop_name() for entry in self.entries]
        on_demand = [entry.get_stop_name() for entry in self.entries if entry.get_stop_type() == 'O']
        not_on_demand = [entry.get_stop_name() for entry in self.entries if entry.get_stop_type() != 'O']
        wrong = []
        for stop_name in on_demand:
            if stop_name in not_on_demand:
                wrong.append(stop_name)
        if len(wrong) == 0:
            print('Wrong stop type: OK')
        else:
            print(f'Wrong stop type: {sorted(set(wrong))}')
