from machine import SDCard
import uos

class MixrSD:
    def __init__(self):
        self.sd = SDCard(slot=1, width=1, mosi=15, miso=2, sck=14, cs=13)
        uos.mount(sd, "/sd")


    def sd_read(self, path):
        content = None
        with open(path, 'rb') as f:
            content = f.read()

        return content

    def sd_write(self, path, writebytes):
        f = open(path, "w")
        f.write(writebytes)
        f.close()

    def sd_ls(self, path='/'):
        listings = uos.ilistdir(path)
        for f in listings:
            print(f)
