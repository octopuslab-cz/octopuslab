# octopusLAB test - 2019
# web server - ap_setup_wifi

# ap = ap_init()
#from examples.ap_setup_wifi import *
#s = webserver_init() 
#webserver_run(s) 

ver = "8.9.2019 - 0.11"

from time import sleep
from util.octopus import printLog, printFree, get_eui, temp_init, get_temp, w, ap_init

from util.pinout import set_pinout
pinout = set_pinout()
from util.led import Led #?VCh
led = Led(pinout.BUILT_IN_LED)
wnum = 0
web_wifi = ""
ssidTemp = ""
passTemp = ""

def webserver_init():
    
    printLog("simple web server2 ver: " + ver)
    print(ver)
    printFree()
    
    try:
        import usocket as socket
    except:
        import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    printFree()

    return s

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

wcss = """<style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: Silver; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: Orange; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: Navy;}</style>"""

wbott = "<br /><hr />octopusLAB - wifi setup - uID: <br />" + get_eui()
wform = """
  <form>
  ssid: <br><input type="text" name="ssid"><br>
  password: <br><input type="text" name="pass"><br><br>
  <input type="submit" value="Submit">
  </form>"""

def web_page():
  web_info = "web-info"
  # web_wifi = "test-wifi"

  html = """<html><head> <title>octopusLAB - ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> """ + wcss + """
  </head><body> <h1>octopus LAB - ESP Web Server</h1>
  """ + wform + """
  <p>""" + web_wifi + """</p>
  <p><br />""" + wbott + """</p></body></html>"""

  return html


def webconn(s):
  global wnum, wform, ssidTemp, passTemp, web_wifi
  
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)

  try:
    rs = request.split(" ")[1]
    rs = (rs[2:]).split("&")
    ssidTemp = rs[0].split("=")
    passTemp = rs[1].split("=")

    if ssidTemp[0] == "ssid": 
      ssidTemp = ssidTemp[1]
      print("ssid.ok")
      if len(ssidTemp) > 1:
        wform = "ssid: " + ssidTemp + "<hr />" + wform

    if passTemp[0] == "pass": 
      passTemp = passTemp[1]
      print("pass.ok")

  except:
    rs = "err"
    
  print()
  print('Content = ' + str(rs))
  print("ssid: " + str(ssidTemp) + " | pass: " + str(passTemp))

  # led_on = request.find('/?led=on')
  print()
  print("wifi_config: ")
  from util.wifi_connect import WiFiConnect
  wc = WiFiConnect()

  webWc = "<hr /><b>Saved networks: </b><br />"
  for k, v in wc.config['networks'].items():
      webWc += k + "<br />"

  # w.add_network(ssidTemp, passTemp)

  wnum += 1
  web_wifi = webWc + "<br /> refresh (" + str(wnum) + ")"

  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

trySetup = True

def webserver_run(s):
    printLog("> run:")
    while trySetup:
        webconn(s)


w()
# ap = ap_init()
sleep(3)

print("ap_scann")
try:
  sc = ap.scan()
  print(len(sc))
  for wi in sc:
    print(wi[0])
  # sc[0][0]
except:
  print("err")


s = webserver_init()
webserver_run(s)