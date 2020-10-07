#!/usr/bin/python
#import pprint

def inventory_unifi_cpu(parsed):
    #if 'load' in parsed:
    yield '', {}



def check_unifi_cpu(item, params, info):
    import json
    parsed = json.loads(" ".join([thing for sublist in info for thing in sublist]))
    if "sys_stats" not in parsed:
        return 3, "no sys_stats"
    load1 = parsed["sys_stats"]["loadavg_1"]
    load5 = parsed["sys_stats"]["loadavg_5"]
    load15 = parsed["sys_stats"]["loadavg_15"]
    perfdata = [ ( "load1", float(load1)), ("load5",float(load5)), ("load15",float(load15)) ]
    out = "15 min load: " + load15
    state = 0
    return 0, out, perfdata




check_info['unifi_aps.cpu'] = {
    'inventory_function': inventory_unifi_cpu,
    'check_function': check_unifi_cpu,
    'service_description': 'CPU load',
    'has_perfdata': True,
}
