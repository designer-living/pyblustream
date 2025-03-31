# Telnet Interface

## Power Off / Power On

```
EL-4KPM-V88> POFF
[SUCCESS]Set system power OFF.

EL-4KPM-V88> PON
[SUCCESS]Set system power ON, please wait a moment... Done

EL-4KPM-V88>
```


# HTTP Interface (e.g. from mobile app)

Flow is:
On app startup: Request Matrix Details
Poll Request Info on current state
Send other commands based off user clicking buttons


1. Request Source Change:
URL: /cgi-bin/submit?cmd=out06fr04
URL: /cgi-bin/submit?cmd=out05fr07
URL: /cgi-bin/submit?cmd=out<outputID>fr<inputID>
No Response


4. Request vol change:
URL: /cgi-bin/submit?cmd=vol25%20tx%206
URL: /cgi-bin/submit?cmd=vol15%20tx%205
URL: /cgi-bin/submit?cmd=vol<precentage>%20tx%20<outputID>
No Response

5. Requset Mute
URL: /cgi-bin/submit?cmd=muteoff%20tx%206
URL: /cgi-bin/submit?cmd=muteon%20tx%206
URL: /cgi-bin/submit?cmd=mute[on|off]%20tx%20<outputID>
No Response

6. Request Matrix details (on start up)
URL: /cgi-bin/getxml.cgi?xml=usersta
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<USERSTA>
  <docver>108</docver>
  <normaluser>
    <index>1</index>
    <name>guest</name>
    <ctrloutput>0,1,2,3,4,5,6,7</ctrloutput>
    <canselinput>0,1,2,3,4,5,6,7</canselinput>
    <canselpreset>0,1,2,3,4,5,6,7</canselpreset>
  </normaluser>
  <adminuser>
    <index>1</index>
    <name>admin</name>
    <ctrloutput>0,1,2,3,4,5,6,7</ctrloutput>
    <canselinput>0,1,2,3,4,5,6,7</canselinput>
    <canselpreset>0,1,2,3,4,5,6,7</canselpreset>
  </adminuser>
</USERSTA>
```

6. Request Info on current state:
URL: /cgi-bin/getxml.cgi?xml=mxsta
Respose:
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<MATRIX>
  <docver>104</docver>
  <webserver>
    <softver>6.22</softver>
    <dhcp>1</dhcp>
    <ip>192.168.1.160</ip>
    <gateway>192.168.1.1</gateway>
    <mask>255.255.255.0</mask>
    <mac>
      F8:57:2E:02:42:FD
    </mac>
    <telnet>23</telnet>
  </webserver>
  <mxsta>
    <devname>EL-4KPM-V88</devname>
    <guiname>Loading...</guiname>
    <softver>3.08</softver>
    <devtype>4</devtype>
    <inputport>8</inputport>
    <outputport>8</outputport>
    <power>1</power>
    <ir>1</ir>
    <key>1</key>
    <beep>0</beep>
    <lcd>1</lcd>
    <rs232>1</rs232>
  </mxsta>
  <output>
    <name>TV1</name>
    <from>6</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>1</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <output>
    <name>TV_2</name>
    <from>5</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>1</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
<output>
    <name>TV3</name>
    <from>5</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>0</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <output>
    <name>TV4</name>
    <from>5</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>1</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>2</delay>
    <vol>30</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <output>
    <name>TV5</name>
    <from>3</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>1</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <output>
    <name>TV6</name>
    <from>0</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>0</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
<output>
    <name>TV_7</name>
    <from>0</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>0</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>25</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <output>
    <name>TV_8</name>
    <from>6</from>
    <hdmihpd>0</hdmihpd>
    <hdbthpd>0</hdbthpd>
    <outputen>1</outputen>
    <poh>1</poh>
    <edidprio>1</edidprio>
    <audtype>4</audtype>
    <audport>0</audport>
    <delay>0</delay>
    <vol>30</vol>
    <mute>0</mute>
    <eq>0,0,0,0,0,0</eq>
  </output>
  <presets>1,1,0,1,0,0,0,1</presets>
  <presets>3,3,0,3,0,0,0,3</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <presets>0,0,0,0,0,0,0,0</presets>
  <input>
  <name>Input1</name>
  <edid>3</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>0</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>2</srcprio>
  <audsig>0</audsig>
  <poh>1</poh>
  </input>
  <input>
  <name>Input_2</name>
  <edid>18</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>0</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>2</srcprio>
  <audsig>0</audsig>
  <poh>1</poh>
  </input>
<input>
  <name>Input_3</name>
  <edid>18</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <input>
  <name>Input_4</name>
  <edid>0</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <input>
  <name>Input_5</name>
  <edid>1</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <input>
  <name>Input_6</name>
  <edid>0</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <input>
  <name>Sky_Box</name>
  <edid>18</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <input>
  <name>Input_8</name>
  <edid>18</edid>
  <hdmi5v>0</hdmi5v>
  <hdbt5v>2</hdbt5v>
  <srcsel>0</srcsel>
  <srcprio>4</srcprio>
  <audsig>0</audsig>
  <poh>2</poh>
  </input>
  <rhri>0</rhri>
  <rhri>1</rhri>
  <rhri>2</rhri>
  <rhri>3</rhri>
  <rhri>4</rhri>
  <rhri>5</rhri>
  <rhri>6</rhri>
  <rhri>7</rhri>
  <girto>255,255,255</girto>
  <girfrom>255,255,255</girfrom>
  <girloop>1</girloop>
  <lrsptp>0</lrsptp>
  <lrsto>9</lrsto>
  <lrsto>10</lrsto>
  <lrsto>11</lrsto>
  <lrsto>12</lrsto>
  <lrsto>13</lrsto>
  <lrsto>14</lrsto>
  <lrsto>15</lrsto>
  <lrsto>16</lrsto>
  <grsto>0</grsto>
</MATRIX>
```
