# vce-1.0-fw-header-reader
VCE 1.0 firmware header reader for amdgpu driver 

This script reads a VCE 1.0 firmware using the new format for amdgpu and displays the header information.

Structure of the header is as follow:

struct common_firmware_header {
    uint32_t size_bytes; /* size of the entire header with full offset+image(s) in bytes: 256+original firmware's length */
    uint32_t header_size_bytes; /* size of just the header's structure in bytes: 32 */
    uint16_t header_version_major; /* header version: 1 */
    uint16_t header_version_minor; /* header version: 0 */
    uint16_t ip_version_major; /* IP version: 1 */
    uint16_t ip_version_minor; /* IP version: 0 */
    uint32_t ucode_version;
    uint32_t ucode_size_bytes; /* size of ucode in bytes: original firmware's length */
    uint32_t ucode_array_offset_bytes; /* payload offset from the start of the header: 256 */
    uint32_t crc32;  /* crc32 checksum of the payload */
};

This can be used on any VCE 1.0. It wasn't tested on other VCE versions, but if the header's structure is the same, it should work.