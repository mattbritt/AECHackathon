Background
- in the AEC Hackathon Dallas (June 2018)
- team Futsies did a mashup which 'terminated' in a blinking light on a Puck.js device

End to End - Mash-Up Summary
- RPi device with 2 Time of Flight LiDAR sensors detects foot traffic / crossing beams and directionality
- That sensor places an http call to a back-end server, such as the "MQTT -n- Dashboard Server" node-red based server in this repo
- That server detects the http call, and then
--- updates a dashboard to indicate a that somebody or something has crossed the threshold FORWARD or REVERSE
--- sends an MQTT packet to the "rPi-3 MQTT - BLE Server" node-red based server also in this repo
- that server receives the MQTT message, and sends a corresponding MQTT message to EspruinHub, which sends the message to a Puck.js device
- the Puck.js device accepts that command, and blinks it's LED either blue or red, indicating either FORWARD or REVERSE

Learn more about the Puck.js here
https://www.puck-js.com/

And learn about it's related products at this site
http://www.espruino.com/


Code for the Puck is in puckTrialsV3.js, and can easily be loaded via the Espruino IDE


