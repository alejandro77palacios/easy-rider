import json

from entry import Entry, ArrayEntries

if __name__ == "__main__":
    data = json.loads(input())
    data = sorted(data, key=lambda x: x['bus_id'])
    entries = [Entry(**entry) for entry in data]
    entries = ArrayEntries(entries)
    entries.analyse_on_demand()
