#!/usr/bin/python
#import pprint

def inventory_unifi_mem(parsed):
    #if 'load' in parsed:
    yield '', {}



def check_unifi_mem(item, params, info):
    import json
    parsed = json.loads(" ".join([thing for sublist in info for thing in sublist]))
    if "sys_stats" not in parsed:
        return 3, "no sys_stats"
    mem_buffer = parsed["sys_stats"]["mem_buffer"]
    mem_total = parsed["sys_stats"]["mem_total"]
    mem_used = parsed["sys_stats"]["mem_used"]
    warn = None
    crit = None
    perfdata = [ ( "mem_used", float(mem_used), warn, crit, 0, float(mem_total)), ("mem_total",float(mem_total)), ("mem_buffer",float(mem_used)) ]
    out = "RAM used: %s of %s Buffers: %s" % (get_filesize_human_readable(mem_used), get_filesize_human_readable(mem_total), get_filesize_human_readable(mem_buffer))
    state = 0
    return 0, out, perfdata




check_info['unifi_aps.mem'] = {
    'inventory_function': inventory_unifi_mem,
    'check_function': check_unifi_mem,
    'service_description': 'Memory',
    'has_perfdata': True,
}
