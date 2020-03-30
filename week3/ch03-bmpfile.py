import sys
import struct
import imghdr


def bmp_unpack(file_name):

    bmp_data = {}
    bmp_data["Format"] = imghdr.what(file_name)

    with open(file_name, 'rb') as f:
        bmp = f.read()

        bmp_data["FormatSignature"] = bmp[0:2].decode()

        bmp_data['FileSize'], _, bmp_data['ImageDataOffset'] = struct.unpack(
            "III", bmp[2:14])

        dib_header = bmp[14:54]

        bmp_data['BitmapHeabmp_dataerSize'], bmp_data['Wibmp_datath'], bmp_data['Height'], \
            bmp_data['NumPlanes'], bmp_data['BitDepth'], bmp_data['CompressionType'], \
            bmp_data['BitmapSize'], bmp_data['HorzResolution'], bmp_data['VertResolution'], \
            bmp_data['NumColorsUsebmp_data'], bmp_data['NumImportantColors'] = \
            struct.unpack("iiihhiiiiii", dib_header)

        if bmp_data['CompressionType'] == 0:
            bmp_data['CompressionType'] = "none (0:BI_RGB)"

        return bmp_data


def main():
    try:
        file_name = sys.argv[1]

        bmp_data = bmp_unpack(file_name)

        max_key_len = max([len(i) for i in bmp_data.keys()])

        for key in bmp_data:
            output_format = "{:>" + str(max_key_len) + "}: {}"
            print(output_format.format(key, bmp_data[key]))
    except IndexError:
        print("Usage: python ch03-bmpfile {file_name}")


if __name__ == "__main__":
    main()
