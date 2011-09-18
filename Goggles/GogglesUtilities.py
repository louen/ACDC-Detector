# ACDC Converter

# utility functions for google goggles API
def intToBinaryStr(n):
  """ convert int in base 10 to a string of 0 and 1"""
  binary =''
  if n==0:
    return "0"
  while n>0:
    binary = str(n%2) + binary
    n = n >> 1
  return binary

def binaryStrToInt(bstr):
  n = 0
  nstr = bstr[::-1]
  i = 0
  for c in nstr :
    if c =="1":
      n+= 2 ** i
    i = i +1
  return n
    
def intToVarint(i):
  """ Converts an int to a base 128 varint"""
  bin_str = intToBinaryStr(i)
  
  # step 1 :  group bits by 7 and left padding with 0
  if (len(bin_str)%7 != 0):
    for i in range(0,7 - len(bin_str)%7):
      bin_str = "0" + bin_str
  bytes_array=[]
  for i in range(0,len(bin_str)//7):
    bytes_array.append(bin_str[7*i:7*(i+1)])
  bytes_array.reverse()

  #step 2 : put a '1' in front of all the groups except the last which gets a '0'
  for i in range(0,len(bytes_array) -1):
    bytes_array[i] = '1' + bytes_array[i]
  bytes_array[-1]= '0' + bytes_array[-1]

  #step 3 : convert the bytes in a bytearray
  int_array = []
  for i in bytes_array:
    int_array.append(binaryStrToInt(i))

  return bytes(int_array)
