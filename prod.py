import struct
import pprint
import os
import json
import sys

def parseProd(data):

    assert data[0x00:0x04] == b'PrOD'
    assert data[0x04:0x08] == bytes([1,0,0,0])

    binary_count, binary_len = struct.unpack('>II',data[0x08:0x10])
    assert binary_count == 1
    filesize, cluster_count, strings_ptr, padding = struct.unpack('>IIII',data[0x10:0x20])
    assert strings_ptr == binary_len + 8
    assert padding == 0
    strings_count, strings_len = struct.unpack('>II',data[strings_ptr:0x08+strings_ptr])
    assert cluster_count == strings_count
    assert 0x10 + binary_len + strings_len == filesize



    offset = 0x20
    objects = {}
    for _ in range(cluster_count):
        cluster_size, element_count, cluster_strptr, padding = struct.unpack('>IIII',data[offset:offset+0x10])
        assert padding == 0
        assert cluster_size == element_count * 0x20
        name = data[strings_ptr+cluster_strptr:].split(b'\0')[0].decode('ascii')
        objects[name] = []
        for j in range(element_count):
            x, y, z, rotX, rotY, rotZ, scale, unk = struct.unpack('>ffffffff',data[offset+0x10+j*0x20:offset+0x30+j*0x20])
            assert unk == 0
            objects[name].append((x,y,z,rotX, rotY, rotZ, scale))
        offset += 0x10 + cluster_size
    return objects

