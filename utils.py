from hashlib import sha1
import json
import time
import base64
import hmac
import struct
import json


def read_config():
    with open('files/config.json', 'r') as f:
        config = json.load(f)
    return config

def generate_one_time_code(shared_secret: str, timestamp: int = None) -> str:
    if timestamp is None:
        timestamp = int(time.time())
    time_buffer = struct.pack('>Q', timestamp // 30) # pack as Big endian, uint64
    time_hmac = hmac.new(base64.b64decode(shared_secret), time_buffer, 
        digestmod=sha1).digest()
    begin = ord(time_hmac[19:20]) & 0xf
    full_code = struct.unpack('>I', time_hmac[begin:begin + 4])[0] \
        & 0x7fffffff  # unpack as Big endian, uint32
    chars = '23456789BCDFGHJKMNPQRTVWXY'
    code = ''
    for _ in range(5):
        full_code, i = divmod(full_code, len(chars))
        code += chars[i]
    return code

def is_json(string):
  try:
    json.loads(string)
  except ValueError as e:
    return False
  return True