#!/usr/bin/python -utt

# Read a VCE 1.0 firmware using the new format for amdgpu, which simply added a header with some information.
# This work is based on Piotr Redlewski's work.
#
# Structure of the header is as follow:
#
#struct common_firmware_header {
#        uint32_t size_bytes; /* size of the entire header with full offset+image(s) in bytes: 256+original firmware's length */
#        uint32_t header_size_bytes; /* size of just the header's structure in bytes: 32 */
#        uint16_t header_version_major; /* header version: 1 */
#        uint16_t header_version_minor; /* header version: 0 */
#        uint16_t ip_version_major; /* IP version: 1 */
#        uint16_t ip_version_minor; /* IP version: 0 */
#        uint32_t ucode_version;
#        uint32_t ucode_size_bytes; /* size of ucode in bytes: original firmware's length */
#        uint32_t ucode_array_offset_bytes; /* payload offset from the start of the header: 256 */
#        uint32_t crc32;  /* crc32 checksum of the payload */
#};

import sys
import struct
import binascii

def payload_crc32_checksum(payload_file):
    crc32_checksum = 0
    payload = open(payload_file, mode='rb')
    for eachLine in payload:
        crc32_checksum = binascii.crc32(eachLine, crc32_checksum)
    payload.close
    return (crc32_checksum & 0xFFFFFFFF)

header_size_bytes = 0
header_version_major = 0
header_version_minor = 0
ip_version_major = 0
ip_version_minor = 0
ucode_version = 0
ucode_size_bytes = 0
ucode_array_offset_bytes = 0
firmware_size_bytes = ucode_size_bytes + ucode_array_offset_bytes
# crc32 = payload_crc32_checksum(sys.argv[1])
crc32 = 0

cfh_struct_format = "IIHHHHIIII"

with open(sys.argv[1], mode='rb') as input:
        CFH_content = struct.unpack(cfh_struct_format, input.read(struct.calcsize(cfh_struct_format)))

        firmware_size_bytes = CFH_content[0]
        header_size_bytes = CFH_content[1]
        header_version_major = CFH_content[2]
        header_version_minor = CFH_content[3]
        ip_version_major = CFH_content[4]
        ip_version_minor = CFH_content[5]
        ucode_version = CFH_content[6]
        ucode_size_bytes = CFH_content[7]
        ucode_array_offset_bytes = CFH_content[8]
        crc32 = CFH_content[9]

# with open(sys.argv[2], mode='wb') as output:
#        output.write(struct.pack('IIHHHHIIII',
#                                  firmware_size_bytes,
#                                  header_size_bytes,
#                                  header_version_major,
#                                  header_version_minor,
#                                  ip_version_major,
#                                  ip_version_minor,
#                                  ucode_version,
#                                  ucode_size_bytes,
#                                  ucode_array_offset_bytes,
#                                  crc32))
#         output.write(bytearray(ucode_array_offset_bytes - header_size_bytes))
#         output.write(fileContent)

# crc32_validation = payload_crc32_checksum(sys.argv[1])

# Interpret ucode_version as version major, minor, binary_id
# ucode's format is 32 bits as version_major 12 bits | version_minor 12 bits | binary_id 8 bits
# TODO: Do we have to consider the endianness?
version_major = int((ucode_version >> 20) & 0x0fff)
version_minor = int((ucode_version >> 8) & 0x0fff)
binary_id = int(ucode_version & 0x00ff)

print ("Header's properties read from VCE 1.0 firmware upgraded file [{}]".format(sys.argv[1]))
print ("Total size of the upgraded firmware [{}]: {}B [uint32]".format(sys.argv[1], firmware_size_bytes))
print ("Header's size: {}B [uint32]".format(header_size_bytes))
print ("Header's version: {}.{} [2*uint16]]".format(header_version_major, header_version_minor))
print ("IP [VCE] version: {}.{} [2*uint16]".format(ip_version_major, ip_version_minor))
print ("uCode version: {} [uint32]".format(ucode_version))
print("    Interpreted uCode version: {}.{}.{}".format(version_major, version_minor, binary_id))
print ("uCode's size: {}B [uint32]".format(ucode_size_bytes))
print ("uCode's offset: {}B [uint32]".format(ucode_array_offset_bytes))
print ("uCode's CRC32 checksum: {} [uint32]".format(crc32))