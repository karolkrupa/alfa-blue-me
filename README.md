# alfa-blue-me
Alfa Romeo/Fiat blue&amp;me infotainment system reimplementation based on raspberry Pi for Alfa Romeo 159 (939)

CAN bus setup:
```
sudo ip link set can0 type can bitrate 50000
sudo ifconfig can0 up
```

Python deps:
```
apt install python-dbus
pip3 install event-bus
pip install python-can
```

```
 $ modprobe vcan
 $ sudo ip link add dev vcan0 type vcan
 $ sudo ip link set up vcan0
```