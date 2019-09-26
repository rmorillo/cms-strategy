import zmq
import time
import sys
import struct
from threading import Thread
from collections import deque
from acme.acme_common import AdminCommand, AdminResponse
from common import ZmqCommand, ZmqResponse

from common.bidask_set import BidAskSetFileReader

def start_feed(incoming_queue, outgoing_queue):
    bidask_set = BidAskSetFileReader("FXMAJOR7-2012-09-2017-09.bidaskset")
    bidask_set.open()
    port = "5556"
    if len(sys.argv) > 1:
        port = sys.argv[1]
        int(port)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    is_enabled = True
    while True:
        if is_enabled:
            bidask_set_row = bidask_set.read()
            topic = bidask_set_row.currency_pair_id
            messagedata = bidask_set_row.bid_price
            print("%d %d %d % d %f %f" % (
            topic, bidask_set_row.ts_date, bidask_set_row.ts_time, bidask_set_row.ts_microsecond, bidask_set_row.bid_price,
            bidask_set_row.ask_price))
            socket.send(struct.pack('if', topic, bidask_set_row.bid_price))
            time.sleep(0.1)
        else:
            if incoming_message == "pause":
                time.sleep(1)

        if len(incoming_queue) > 0:
            incoming_message = incoming_queue.pop()
            if incoming_message == "stop":
                break
            elif incoming_message == "pause":
                is_enabled = False
            elif incoming_message == "resume":
                is_enabled = True

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

incoming_queue = deque()
outgoing_queue = deque()

while True:
    #  Wait for next request from client
    message = socket.recv()
    command = AdminCommand.get_command_by_id(ZmqCommand.unpack(message))
    print("Received request: %s" % command.value.command_name)

    if command == AdminCommand.Start:
        print("starting feed")
        t = Thread(target = start_feed, args=(incoming_queue, outgoing_queue))
        t.start()
    elif command == AdminCommand.Stop:
        incoming_queue.append("stop")
    elif command == AdminCommand.Pause:
        incoming_queue.append("pause")
    elif command == AdminCommand.Resume:
        incoming_queue.append("resume")

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(AdminResponse.Success.value.pack())