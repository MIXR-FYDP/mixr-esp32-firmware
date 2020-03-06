import mixrnetwork
import network
import gc
import picoweb
import ulogging as logging
import mixrpower

gc.collect()
logging.basicConfig(level=logging.debug)

mp = mixrpower.MixrPower()
mp.initialize()
# import mixrui

# miui = mixrui.MixrUI()
# miui.initialize()

# while True:
#     pass
