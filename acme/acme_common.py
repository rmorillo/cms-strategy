from enum import Enum
from common import ZmqCommand, ZmqResponse

class AdminCommand(Enum):
    Start = ZmqCommand(1, "start")
    Stop = ZmqCommand(2, "stop")
    FastForward = ZmqCommand(3, "fastforward")
    Pause = ZmqCommand(4, "pause")
    Resume = ZmqCommand(5, "resume")
    Show = ZmqCommand(6, "show")

    @staticmethod
    def get_command_by_name(command_name):
        for command in AdminCommand:
            if command.value.command_name == command_name.lower():
                return command
        return None

    @staticmethod
    def get_command_by_id(command_id):
        for command in AdminCommand:
            if command.value.command_id == command_id:
                return command
        return None

class AdminResponse(Enum):
    Success = 1
    Failure = 0

    @staticmethod
    def get_response_by_id(response_id):
        for response in AdminResponse:
            if response.value.response_id == response_id:
                return response
        return None

    @staticmethod
    def decode(byte_response):
        response_id = int.from_bytes(byte_response[:4], "big")
        return AdminResponse.get_response_by_id(response_id)

    @staticmethod
    def encode(response):
        return response.value.to_bytes(4, "big")