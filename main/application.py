from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS1820
from main.log import Log
from numpy import median

scale = Scale()
log = Log()
dht = DHT22(21)
wire = DS1820("28-000008e2f080")

