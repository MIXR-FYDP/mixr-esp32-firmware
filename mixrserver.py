import mixrnetwork
import network
import gc
import picoweb

gc.collect()

import ulogging as logging
logging.basicConfig(level=logging.debug)

host = mixrnetwork.ap_connect()

app = picoweb.WebApp('mixr')

@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("This is webapp #1")

@app.route("/setinstruments")
def set_instruments(req, resp):
    pass

@app.route("/record")
def record(req, resp):
    pass

@app.route("/stop")
def stop(req, resp):
    pass

@app.route("/process")
def process(req, resp):
    pass

@app.route("/logo")
def imagelogo(req, resp):
    yield from picoweb.start_response(resp, "image/png")
    yield from resp.awrite(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x000\x00\x00\x000\x01\x03\x00\x00\x00m\xcck"
        b"\xc4\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00U\xc2\xd3~\x00\x00\x00\xd2IDAT\x18\xd3c`"
        b"\x80\x01\xc6\x06\x08-\x00\xe1u\x80)\xa6\x040\xc5\x12\x00\xa18\xc0\x14+\x84\xe2\xf5\x00Sr"
        b"\x10J~\x0e\x98\xb2\xff\x83\x85\xb2\x86P\xd2\x15\x10\x95\x10\x8a\xff\x07\x98b\xff\x80L\xb1"
        b"\xa5\x83-?\x95\xff\x00$\xf6\xeb\x7f\x01\xc8\x9eo\x7f@\x92r)\x9fA\x94\xfc\xc4\xf3/\x80\x94"
        b"\xf8\xdb\xff'@F\x1e\xfcg\x01\xa4\xac\x1e^\xaa\x01R6\xb1\x8f\xff\x01);\xc7\xff \xca\xfe\xe1"
        b"\xff_@\xea\xff\xa7\xff\x9f\x81F\xfe\xfe\x932\xbd\x81\x81\xb16\xf0\xa4\x1d\xd0\xa3\xf3\xfb"
        b"\xba\x7f\x02\x05\x97\xff\xff\xff\x14(\x98\xf9\xff\xff\xb4\x06\x06\xa6\xa8\xfa\x7fQ\x0e\x0c"
        b"\x0c\xd3\xe6\xff\xcc\x04\xeaS]\xfet\t\x90\xe2\xcc\x9c6\x01\x14\x10Q )\x06\x86\xe9/\xc1\xee"
        b"T]\x02\xa68\x04\x18\xd0\x00\x00\xcb4H\xa2\x8c\xbd\xc0j\x00\x00\x00\x00IEND\xaeB`\x82"
    )


@app.route("/zuheir")
def zuheir(req,resp):
    print(req)
    print(dir(req))
    if req.method == "POST":
        print("POST at /zuheir")
        yield from req.read_form_data()
        print(req.form)
        yield from picoweb.start_response(resp)
        yield from resp.awrite("Posted Zuheir")
    elif req.method == "GET":
        print("GET at /zuheir")

        yield from picoweb.start_response(resp)
        yield from resp.awrite("Got Zuheir")    
    else:
        print("Unrecognized HTTP Method")
        yield from picoweb.start_response(resp)
        yield from resp.awrite("Bad Request")
# @app.route("/test")
# def endpointA(req, resp):
#     print(req)
#     print(dir(req))
#     if req.method == "POST":
#         print("POST at /test was gotten")
#         yield from picoweb.start_response(resp)
#         yield from resp.awrite("Got Zuheir")
#     else:
#         print("")
#         yield from picoweb.start_response(resp)
#         yield from resp.awrite("HTTP method was allowed")    



app.run(debug=True, port="8089", host=host)

# 192.168.4.1