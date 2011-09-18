# ACDC Converter
# http://notanothercodeblog.blogspot.com/2011/02/google-goggles-api.html
import http.client
import random
import struct

from GogglesUtilities import *
from GogglesResponseParser import *


class GogglesAPI(object):

  
  def __init__(self):

    # magic numbers
    self.cssid_request_body = bytearray.fromhex(" 22 00 62 3C 0A 13 22 02 65 6E BA D3 F0 3B 0A 08 01 10 01 28 01 30 00 38 01 12 1D 0A 09 69 50 68 6F 6E 65 20 4F 53 12 03 34 2E 31 1A 00 22 09 69 50 68 6F 6E 65 33 47 53 1A 02 08 02 22 02 08 01")
    self.image_request_trailing = bytearray.fromhex("18 4B 20 01 30 00 92 EC F4 3B 09 18 00 38 C6 97 DC DF F7 25 22 00")

    #initialization
    self.genCssid()
    self.validateCssid()

  def postDataToGoogle(self,data):

    
    conn = http.client.HTTPConnection("www.google.com")
#    conn.set_debuglevel(2)

    url = "http://www.google.com/goggles/container_proto?cssid="
    url += self.cssid  
    headers = {"Content-type":"application/x-protobuffer","Pragma":"no-cache","Keep-alive":"true"}
    conn.request("POST",url,(data),headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    result = response.read()
    conn.close()
    return result

  def genCssid(self):
    #generates 16 hex random digits
    self.cssid =""
    for i in range (0,16):
      self.cssid += (hex(random.randint(0,15))).replace('0x','')
    print(self.cssid)

  def validateCssid(self):
    body = self.cssid_request_body
#    body.append(0)
#    body.append(len(body) -1 )  
    self.postDataToGoogle(bytes(body))


  def sendImage(self,file_name):
    image = open(file_name,"rb")
    data = image.read()
    size = image.tell()
    
    data_array = bytearray(data)
    body = bytearray()
    body.append(0x0A)
    body += intToVarint(size + 32)
    body.append(0x0A)
    body += intToVarint(size + 14)
    body.append(0x0A)
    body += intToVarint(size + 10)
    body.append(0x0A)
    body += intToVarint(size)
    
    body += data
    body += (self.image_request_trailing)

    reply =self.postDataToGoogle(bytes(body))

    pprint(reply)
    

    
G = GogglesAPI()
G.sendImage("lol.jpg")
