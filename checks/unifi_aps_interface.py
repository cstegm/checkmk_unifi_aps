#!/usr/bin/python
#import pprint

def inventory_unifi_interface(info):
    import json
    parsed = json.loads(" ".join([item for sublist in info for item in sublist]))
    for interface in parsed["vap_table"]:
        name = interface["radio_name"]
        yield name, {}



def check_unifi_interface(item, params, info):
    import json
    parsed = json.loads(" ".join([thing for sublist in info for thing in sublist]))
    if "vap_table" not in parsed:
        return 3, "no vap_table"
    for interface in parsed["vap_table"]:
        name = interface["radio_name"]
        if name == item:
            # rx = in
            in_bytes = interface["rx_bytes"]
            in_discards = interface["rx_dropped"]
            in_errors = interface["rx_errors"]
            in_packets = interface["rx_packets"]
            in_tcp_avg_lat = interface["rx_tcp_stats"]["lat_avg"]

            # tx = out
            out_bytes = interface["tx_bytes"]
            out_discards = interface["tx_dropped"]
            out_errors = interface["tx_errors"]
            out_packets = interface["tx_packets"]
            out_tcp_avg_lat = interface["tx_tcp_stats"]["lat_avg"]
               
            dns_avg_latency = interface["dns_avg_latency"]
            essid = interface["essid"]
            channel = interface["channel"]

            state = interface["state"]
            satisfaction = interface["satisfaction"]
            perfdata = [("dns_avg_lat",int(dns_avg_latency)),( "in", int(in_bytes)), ("indisc",int(in_discards)), ("inerr",int(in_errors)), ("out",int(out_bytes)), ("outdisc", int(out_discards)), ("outerr",int(out_errors)), ("inpck", int(in_packets)), ("outpck", int(out_packets)), ("satisfaction", int(satisfaction)), ("in_tcp_avg_lat", int(in_tcp_avg_lat)), ( "out_tcp_avg_lat", int(out_tcp_avg_lat)) ]
            out = "ESSID: %s, Channel: %s, State: %s, Satisfaction: %s%%" % (essid, channel, state, satisfaction)
            state = 0
            return 0, out, perfdata




check_info['unifi_aps.interface'] = {
    'inventory_function': inventory_unifi_interface,
    'check_function': check_unifi_interface,
    'service_description': 'Interface %s',
    'has_perfdata': True,
}
