import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("stuti_dhrn_2.4", "stuti@linux@dhrn")
