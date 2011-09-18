# ACDC Converter

# Cheers to `deetch` (https://github.com/deetch) that allowed me to
# use his code :)

import struct

Coords = {
    1: {"label": "x", "isValue": True},
    2: {"label": "width", "isValue": True},
    3: {"label": "y", "isValue": True},
    4: {"label": "height", "isValue": True}
}

Info = {
    15690847: {
        "label": "UIStuff",
        "isValue": False,
        "contents": {
            1: {
                "label": "Coords",
                "isValue": False,
                "contents": Coords
            },
            2: {
                "label": "some int",
                "isValue": True
            },
            3: {
                "label": "image for result type",
                "isValue": False,
                "contents": {
                    1: {"label": "image to show", "isValue": True},
                    2: {"label": "url (list?)", "isValue": True, "contents": {}},
                    3: {"label": "site where the image originates", "isValue": True}
                }
            },
            6: {
                "label": "language",
                "isValue": True
            }
        }
    },
    15693652: {
        "label": "Search query for request",
        "isValue": False,
        "contents": {
            2: {"label": "url", "isValue": True}
        }
    },
    16045192: {
        "label": "direct result",
        "isValue": False,
        "contents": {
            1: {"label": "result string", "isValue": True},
            3: {"label": "result description", "isValue": True}
        }
    }
}

ReplyItem = {
    1: {
        "label": "Info",
        "isValue": False,
        "contents": Info
    } 
}

AlternativeInfo = {
    1: {
        "label": "Alternative Info",
        "isValue": False,
        "contents": Info
    },
    2: {
        "label": "some 64bit value",
        "isValue": True,
    }
}

parse_dict = {
    1: {
        "label": "Reply",
        "isValue": False,
        "contents": {
            1: {
                "label": "ReplyItem",
                "isValue": False,
                #"contents": ReplyItem
                "contents": Info
            },
            15705729: {
                "label": "unknown",
                "isValue": False,
                "contents": AlternativeInfo
            }
        }
    }
}

RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

dtypes = {0: 'varint', 1: "64bit", 2: "lengthdelim", 3: "startgroup", 4: "endgroup", 5: "32bit"}

def parse_varint(input, pos):
    res = 0
    shift = 0
    while True:
        b = (input[pos])
        res |= ((b & 0x7f) << shift)
        pos += 1
        if not (b & 0x80):
            res &= (1 << 64) - 1
            return (res, pos)
        shift += 7
        if shift >= 64:
            print("error parsing varint")
            break
            
def parse_32(input, pos):
    return (struct.unpack('<I', input[pos:pos+4])[0], pos+4)

def parse_64(input, pos):
    return (struct.unpack('<Q', input[pos:pos+8])[0], pos+8)
            
def parse_tag(input, pos):
    start = pos
    while (input[pos]) & 0x80:
        pos += 1
    pos += 1
    tag, _ = parse_varint(input[start:pos], 0)
    dtype = dtypes[tag & 0x7]
    field = tag >> 3
    return(field, dtype, pos)

def parse(input, pos=0):
    res = []
    while pos is not None:
        data = ""
        #print repr(input[pos:])
        field, dtype, pos = parse_tag(input, pos)
        #print GREEN, field, dtype, ENDC
        if dtype == "lengthdelim":
            length, pos = parse_varint(input, pos)
            data = input[pos:pos+length]
            pos += length
        elif dtype == "varint":
            data, pos = parse_varint(input, pos)
        elif dtype == "32bit":
            data, pos = parse_32(input, pos)
        elif dtype == "64bit":
            data, pos = parse_64(input, pos)
        elif dtype == "startgroup":
            data = "startgroup"
        elif dtype == "endgroup":
            data = "endgroup"
        else:
            print(RED+"NEW DTYPE:", dtype, ENDC)
        if pos >= len(input):
            pos = None
        res.append((field, dtype, data))
    return res

def gen_res(input, descr=parse_dict):
    res = []
    for field, dtype, data in parse(input):
        if field in descr:
            d = dict(descr[field])
            if d["isValue"]:
                d["contents"] = data
            else:
                d["contents"] = gen_res(data, descr[field]["contents"])
            del d["isValue"]
            d["field"] = field
            res.append(d)
        else:
            print(GREEN+str(field)+ENDC)  
            print(RED+repr(data)+ENDC)
            res.append({"field": field, "contents": data})
    return res

def pprint(input):
    def print_item(item, tabs=""):
        print(tabs+GREEN+str(item["field"])+ENDC)
        if "label" in item: print(tabs+RED+item["label"]+ENDC)
        if type(item["contents"]) is list:
            for i in item["contents"]:
                print_item(i, tabs+"\t")
        else:
            print(tabs+repr(item["contents"]))

    data = gen_res(input)
    print ("### start of non-debug output ###")
    for item in data:
        print_item(item)



