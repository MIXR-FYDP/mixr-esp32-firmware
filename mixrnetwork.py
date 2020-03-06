import network
 
def connect(ssid, password):
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())

def ap_connect():
    ssid = 'MIXR-AP'
    password = 'mixr'

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while ap.active() == False:
        pass

    print('Connection successful')
    print(ap.ifconfig())
    return ap.ifconfig()[0]
