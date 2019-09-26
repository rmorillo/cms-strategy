import sys
import zmq
import struct

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect ("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

# Subscribe to zipcode, default is NYC, 10001
socket.setsockopt(zmq.SUBSCRIBE, (1).to_bytes(1,"big"))
socket.setsockopt(zmq.SUBSCRIBE, (2).to_bytes(1,"big"))
# Process 5 updates
total_value = 0
while True:
    incoming_data = socket.recv()
    topic, bid_price = struct.unpack('if', incoming_data)
    print("topic: %d bid price: %f" % (topic,bid_price))
