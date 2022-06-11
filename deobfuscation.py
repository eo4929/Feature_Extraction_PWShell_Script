import glob
import base64
import zlib
import re
import csv

count = 0


def count_deobf(raw_string, find_string):
    count = 0

    while True:
        if (raw_string.find(find_string) == -1):
            break
        raw_string = raw_string[raw_string.find(find_string) + len(find_string):]
        count += 1

    return count


def ascii_decode(dir_name):
    global count

    temp_item = glob.glob(dir_name)

    # F_name = "C:\\Users\\Admin\\Desktop\\ascii\\ascii.csv"
    # a_file = open(F_name, "a", newline='')

    for item in temp_item:
        # 1. Get a file name
        file_name = item.split('\\')[-1]
        print('file_name: ', file_name)

        # 2. Check a file encoding format
        f = open(item, "rb").read(1)

        encode_format = 'utf-8'
        if ((f == b'\xfe') | (f == b'\xff')):
            encode_format = 'utf-16'

        # 3. Read a file to a string
        origin_string = open(item, "rb").read()
        origin_string = origin_string.decode(encoding=encode_format, errors='ignore')

        # 4. Change the string to lowercase letters
        lower_string = origin_string.lower()

        if (lower_string.find('convert]::frombase64string(') == -1):
            continue

        if (lower_string[:lower_string.find('convert]::frombase64string(')].find("\n") != -1):
            continue

        check_depress = count_deobf(lower_string, "::decompress")
        check_ascii = count_deobf(lower_string, "text.encoding]::")

        # 5. Find a 'text.encoding]::' in the string
        if (check_ascii > 0):
            stringStart_point = lower_string.find('text.encoding]::') + len('text.encoding]::')
            findString = lower_string[stringStart_point:]
            stringEnd_point = stringStart_point + findString.find(")")
            findString = lower_string[stringStart_point:stringEnd_point]

        # 6. Check a encoded type
        encoded_type = ''
        if 'ascii' in findString:
            encoded_type = 'ascii'
        elif 'utf8' in findString:
            encoded_type = 'utf8'
        elif 'unicode' in findString:
            encoded_type = 'unicode'

        # 8. Get a base64string.
        no_gap_string = lower_string.replace(" ", "")

        if (no_gap_string.find("convert]::frombase64string(") != -1):
            baseStart_point = no_gap_string.find("convert]::frombase64string(") + len("convert]::frombase64string('")

        tmp_string = no_gap_string[baseStart_point:]
        if (tmp_string.find("),") != -1):
            baseEnd_point = tmp_string.find("),") + baseStart_point - 1

        lower_baseString = no_gap_string[baseStart_point:baseEnd_point]

        # 9. Get an origin base64string.
        origin_startPoint = lower_string.find(lower_baseString)
        origin_endPoint = origin_startPoint + len(lower_baseString)
        base64string = origin_string[origin_startPoint:origin_endPoint]

        # 9. Decode the base64string.
        base64string_new = base64string + "=="
        base64decode = base64.b64decode(base64string_new)

        # 10. Check the compress
        if (check_depress > 0):
            decompressed = zlib.decompress(base64decode, -zlib.MAX_WBITS)

        # 11. Decode string.
        if (check_ascii > 0):
            if encoded_type == "ascii":
                base64decode = decompressed.decode('utf-8')

        '''
        toint_count = count_deobf(lower_string, "[convert]::toint16(")
        base64_count = count_deobf(lower_string, "convert]::frombase64string")
        encode_count = count_deobf(lower_string, "text.encoding]::")
        depress_count = count_deobf(lower_string, "::decompress")
        toint_count_b = count_deobf(base64decode.lower(), "[convert]::toint16(")
        base64_count_b = count_deobf(base64decode.lower(), "convert]::frombase64string")
        encode_count_b = count_deobf(base64decode.lower(), "text.encoding]::")
        depress_count_b = count_deobf(base64decode.lower(), "::decompress")

        # 10. Save the file.
        wr = csv.writer(a_file)
        wr.writerow([file_name, toint_count, base64_count, encode_count, depress_count,\
                     toint_count_b, base64_count_b, encode_count_b, depress_count_b])
        '''
        f = open("C:\\Users\\Dae-Young Park\\PycharmProjects\\powershell_reverse_obfuscation\\trasformed_to_scripts\\" + file_name, "w")
        #print('file created')
        # f.write(front_originString)
        f.write(base64decode)
        # f.write(back_originString)
        f.close()
        #print('base64decode: ', base64decode)
        count += 1


# a_file.close()


if __name__ == "__main__":
    file_path = "C:\\Users\\Dae-Young Park\\Desktop\\AI스터디\\작년데이터셋\\(A트랙) AI기반 파워쉘 악성 스크립트 탐지_학습 데이터셋\\(A트랙) AI기반 파워쉘 악성 스크립트 탐지_학습 데이터셋\\phase0_v2\\*"
    ascii_decode(file_path)
    print(count)