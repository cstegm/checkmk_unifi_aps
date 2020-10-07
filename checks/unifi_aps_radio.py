#!/usr/bin/python
#import pprint

def inventory_unifi_radio(info):
    import json
    parsed = json.loads(" ".join([item for sublist in info for item in sublist]))
    for radio in parsed["radio_table_stats"]:
        name = radio["name"]
        yield name, {}



def check_unifi_radio(item, params, info):
    import json
    parsed = json.loads(" ".join([thing for sublist in info for thing in sublist]))
    if "radio_table_stats" not in parsed:
        return 3, "no radio_table_stats"
    for radio in parsed["radio_table_stats"]:
        name = radio["name"]
        if name == item:
            satisfaction = radio["satisfaction"]
            state = radio["state"]
            perfdata = [( "satisfaction", int(satisfaction))]# ( "load1", float(load1)), ("load5",float(load5)), ("load15",float(load15)) ]
            out = "State: %s Satisfaction: %s%%" % (state, satisfaction)
            state = 0
            return 0, out, perfdata




check_info['unifi_aps.radio'] = {
    'inventory_function': inventory_unifi_radio,
    'check_function': check_unifi_radio,
    'service_description': 'Unifi radio %s',
    'has_perfdata': True,
}
