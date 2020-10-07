# Install

* Requirement: checkmk agent is installed
* copy the content of the plugins directory to: /usr/lib/check_mk_agent/plugins/
* copy the content of the checks directory to your checkmksites directory: /omd/sites/<yoursitename>/local/share/check_mk/checks/

# How does it work
The plugin will create piggybackdata for every found Unifi AP. If you configure checkmks DCD it will automatically create hosts for every AP you have: https://checkmk.com/cms_dcd.html

