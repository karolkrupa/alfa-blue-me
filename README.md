# alfa-blue-me
Alfa Romeo/Fiat blue&amp;me infotainment system reimplementation based on raspberry Pi for Alfa Romeo 159 (939)

CAN bus setup:
```
sudo ip link set can0 type can bitrate 50000
sudo ifconfig can0 up
```