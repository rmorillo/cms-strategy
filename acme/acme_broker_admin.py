import zmq
from acme.acme_common import AdminCommand, AdminResponse
from common import ZmqCommand, ZmqResponse

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
while True:
    input_command = input("=> ")
    command = AdminCommand.get_command_by_name(input_command)
    print("Sending request %s …" % command.value.command_name)
    socket.send(command.value.pack())

    #  Get the reply.
    message = socket.recv()
    response = AdminResponse.decode(message)

    print("Received reply %s [ %s ]" % (command.value.command_name, response.value.response_name))
