#!/usr/bin/python
#import pprint

def inventory_unifi_anomalies(info):
    import json
    parsed = json.loads(" ".join([item for sublist in info for item in sublist]))
    for anomalies in parsed["vap_table"]:
        name = anomalies["radio_name"]
        yield name, {}



def check_unifi_anomalies(item, params, info):
    import json
    parsed = json.loads(" ".join([thing for sublist in info for thing in sublist]))
    if "vap_table" not in parsed:
        return 3, "no vap_table"
    for anomalies in parsed["vap_table"]:
        name = anomalies["radio_name"]
        state = 0
        out = ""
        if name == item:
            for anoitem in anomalies["anomalies_bar_chart_now"]:
                val = anomalies["anomalies_bar_chart_now"][anoitem]
                s = ""
                if val != 0:
                    state = 2
                    s = "(!!)"
                out += anoitem + ":" + str(val) + " " + s + ", "
            return state, out


check_info['unifi_aps.anomalies'] = {
    'inventory_function': inventory_unifi_anomalies,
    'check_function': check_unifi_anomalies,
    'service_description': 'Anomalies %s',
}
