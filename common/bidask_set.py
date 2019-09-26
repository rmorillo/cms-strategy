import struct
from collections import namedtuple

BidAskSetColumns = namedtuple('BidAskSetColumns', 'ts_date ts_time ts_microsecond currency_pair_id bid_price ask_price')

class BidAskSetFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.format = 'iiiiff'
        self.row_size = struct.calcsize(self.format)
        self.file = None
        self.row_count = 0
        
    def open(self):
        self.file = open(self.file_path, 'rb')
        current_position = self.file.tell()
        self.file.seek(0, 2)
        last_position = self.file.tell()
        self.file.seek(current_position)
        self.row_count = int((last_position - current_position) / self.row_size)

    def read(self):
        byte_data = self.file.read(self.row_size)
        if (len(byte_data) > 0):
            row_data = struct.unpack(self.format, byte_data)            
            date_part = row_data[0]        
            time_part = row_data[1]
            microsecond_part = row_data[2]
            currency_pair_id = row_data[3]
            bid_price = row_data[4]
            ask_price = row_data[5]
            return BidAskSetColumns(date_part, time_part, microsecond_part, currency_pair_id, bid_price, ask_price)
        else:
            return None

    def close(self):
        self.file.close()
