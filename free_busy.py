from m5stack import *
from uiflow import *
from m5ui import *
import wifiCfg
import socket


state = 0 #state variable for the leds

#function for displaying the html 
def web_page():
    if state == 0:
        led_state="Free"
    else:
        led_state="Busy"
    batt = power.getBatteryLevel()
    isCharging = power.isCharging()
    isFull = power.isChargeFull()
    html = """<html><head> <title>Free/busy</title> <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,"> <style>html{font-family: Comic Sans MS; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #FF0000; border: none; 
    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 40px; margin: 2px; cursor: pointer;}
    .button2{background-color: #00ff00;}.button3{background-color: #ff00ff</style></head><body> <h1>Free/busy</h1> 
    <p>State: <strong>""" + str(led_state) + """</strong></p><p>battery: <strong>""" + str(batt) + """</strong></p><p>Charging?: <strong>""" + str(isCharging) + """</strong></p><p>Full?: <strong>""" + str(isFull) + """</strong></p><p><a href="/?led=on"><button class="button">BUSY</button></a></p>
    <p><a href="/?led=off"><button class="button button2">FREE</button></a></p>
    <p><a href="/?btn=on"><button class="button button3">Speaker</button></a></p>
    </html>"""
    return html

ip = wifiCfg.wlan_sta.ifconfig()

#create labels to display the information on the M5Stack screen
label1 = M5TextBox(0, 0, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
label2 = M5TextBox(0, 12, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
label3 = M5TextBox(0, 24, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
label4 = M5TextBox(0, 50, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
label5 = M5TextBox(120, 200, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)
rectangle0 = M5Rect(0, 0, 318, 240, 0xff0000, 0xFFFFFF)
busylabel = M5TextBox(61, 81, "BUSY", lcd.FONT_DejaVu72,0xFFFFFF, rotate=0)

rgb.setColorAll(0x000000)
setScreenColor(0x000000)
lcd.setBrightness(0)
rectangle0.hide()
busylabel.hide()

response = None
wifiCfg.doConnect('<<SSID>>', '<<PASSWORD>>')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('<<IP_ADDRESS>>', 80))
s.listen(5)

if wifiCfg.wlan_sta.isconnected():
  label1.setText('wifi connected')
  ip = wifiCfg.wlan_sta.ifconfig()
  label2.setText('Your IP Address is: ' + str(ip[0]))
else:
  label1.setText('wifi not connected')
  wait_ms(2)

while True:
  conn, addr = s.accept()
  request = conn.recv(1024)
  request = str(request)
  #label4.setText('Content = %s' % request)
  #label3.setText('Got a connection from %s' % str(addr))
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  btn_press = request.find('/?btn=on')

  if led_on == 6:
    state = 1
    #label5.setText('LED ON')
    rgb.setColorAll(0xFF0000)
    setScreenColor(0xFF0000)
    lcd.setBrightness(30)
    rectangle0.show()
    busylabel.show()
  if led_off == 6:
    state = 0
    #label5.setText('LED OFF')
    rgb.setColorAll(0x000000)
    setScreenColor(0x000000)
    lcd.setBrightness(0)
    rectangle0.hide()
    busylabel.hide()
  if btn_press == 6:
    speaker.tone(400,200)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
