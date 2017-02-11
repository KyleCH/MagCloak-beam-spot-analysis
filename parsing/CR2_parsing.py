#!/usr/bin/env python3

# ======================================================================
# Main CR2 processing function.
# ======================================================================

def CR2(fname_in, fname_out):
    with open(fname_in, 'rb') as file:
        fi = file.read()
    with open(fname_out, 'w') as fo:
        fo.write('Input File: {}'.format(fname_in))
        
        # File header.
        fo.write('\n\nFile header.')
        header, header_key_list, header_format, byteorder = file_header(fi)
        write(fo, header, header_key_list, header_format)
        
        # RAW IFD.
        fo.write('\n\nRAW image file directory.')
        ifd, ifd_key_list, ifde_key_list, ifd_format = IFD(fi,
            header['RAW IFD offset'], byteorder)
        write_IFD(fo, ifd, ifd_key_list, ifde_key_list, ifd_format)
        
    return 0

# ======================================================================
# Write to output file.
# ======================================================================

def write(output_file, dictionary, key_list, output_format):
    for i, key in enumerate(key_list):
        of = output_format[i]
        if ((len(of) > 0) and (of[-1] == 'x')):
            of = '0x{:'+of+'}'
        else:
            of = '{}'
        output_file.write('\n\t{}: {}'.format(key, of).format(dictionary[key]))
    return 0

# ======================================================================
# Write IFD to output file.
# ======================================================================

def write_IFD(output_file, dictionary, key_list, e_key_list, output_format):
    for i, key in enumerate(key_list):
        of = output_format[i]
        if (i > 0):
            output_file.write('\n\t{}:'.format(key))
            for j, ekey in enumerate(e_key_list):
                eof = output_format[i][j]
                if ((len(eof) > 0) and (eof[-1] == 'x')):
                    eof = '0x{:'+eof+'}'
                else:
                    eof = '{}'
                output_file.write('\n\t\t{}: {}'.format(ekey, eof).format(
                    dictionary[key][ekey]))
        else:
            if ((len(of) > 0) and (of[-1] == 'x')):
                of = '0x{:'+of+'}'
            else:
                of = '{}'
            output_file.write('\n\t{}: {}'.format(key, of).format(
                dictionary[key]))
    return 0

# ======================================================================
# File header.
# ======================================================================

def file_header(f):
    
    # Byte order.
    dictionary = {'byte order' : chr(f[0]) + chr(f[1])}
    key_list = ['byte order']
    output_format = ['s']
    
    if dictionary['byte order'] == 'II':
        byteorder = 'little'
    elif dictionary['byte order'] == 'MM':
        byteorder = 'big'
    
    # TIFF magic word.
    dictionary['TIFF magic word'] = int.from_bytes(f[2:4], byteorder)
    key_list += ['TIFF magic word']
    output_format += ['04x']
    
    # TIFF offset.
    dictionary['TIFF offset'] = int.from_bytes(f[4:8], byteorder)
    key_list += ['TIFF offset']
    output_format += ['08x']
    
    # CR2 magic word.
    dictionary['CR2 magic word'] = chr(f[8]) + chr(f[9])
    key_list += ['CR2 magic word']
    output_format += ['s']
    
    # CR2 major version.
    dictionary['CR2 major version'] = f[0x0a]
    key_list += ['CR2 major version']
    output_format += ['']
    
    # CR2 minor version.
    dictionary['CR2 minor version'] = f[0x0b]
    key_list += ['CR2 minor version']
    output_format += ['']
    
    # RAW IFD offset.
    dictionary['RAW IFD offset'] = int.from_bytes(f[0x0c:0x10], byteorder)
    key_list += ['RAW IFD offset']
    output_format += ['08x']
    
    return dictionary, key_list, output_format, byteorder

# ======================================================================
# Image file directory.
# ======================================================================

def IFD(f, offset, byteorder):
    
    offsetp2 = offset + 2
    dictionary = {}
    
    # Number of entries.
    dictionary['number of entries'] = int.from_bytes(f[offset:offsetp2],
        byteorder)
    key_list = ['number of entries']
    output_format = ['04x']
    
    # Entries.
    for n in range(dictionary['number of entries']):
        key_list += ['entry#{}'.format(n)]
        e_dictionary, e_key_list, e_output_format = IFD_entry(f, offsetp2+12*n,
            byteorder)
        dictionary[key_list[n+1]] = e_dictionary
        output_format += [e_output_format]
    
    return dictionary, key_list, e_key_list, output_format

# ======================================================================
# Image file directory entry.
# ======================================================================

def IFD_entry(f, offset, byteorder):
    
    # Tag ID.
    dictionary = {'tag ID': int.from_bytes(f[offset:offset+2], byteorder)}
    key_list = ['tag ID']
    output_format = ['04x']
    
    # Tag type.
    dictionary['tag type'] = int.from_bytes(f[offset+2:offset+4], byteorder)
    key_list += ['tag type']
    output_format += ['04x']
    
    # Number of value.
    dictionary['number of value'] = int.from_bytes(f[offset+4:offset+8],
        byteorder)
    key_list += ['number of value']
    output_format += ['08x']
    
    # Value, or pointer to the data.
    dictionary['value, or pointer to the data'] = int.from_bytes(
        f[offset+8:offset+12], byteorder)
    key_list += ['value, or pointer to the data']
    output_format += ['08x']
    
    return dictionary, key_list, output_format

# ======================================================================
# Run test.
# ======================================================================

CR2('./IMG_0478.CR2', 'test.txt')
