# -*- coding: utf-8 -*-
import flat
import codecs

INPUT_FILE = "sold_flats_1.txt"


def get_empty_dict():
    d = {
        "sold-date": "",
        "price": -1.0,
        "price-per-m2": -1.0,
        "asked-price": -1.0,
        "address": "",
        "area": "",
        "city":"",
        "broker": "",
        "living-area-m2": -1.0,
        "living-area-rooms": -1.0,
        "land-area": -1,
        "supplemental-area": -1,
        "flat_type": ""
    }
    return d


def string2float(s_value):
    v = s_value.replace(" ", "").replace(",", "")
    return float(v)

def parse_living_area(s_living_area):
    #print s_living_area
    s_living_area = s_living_area.replace("m2", "").replace("rum", "")
    fields = s_living_area.split(";")

    v1, v2 = -1.0, -1.0
    if len(fields[0].strip()) > 0:
        v1 = float(fields[0].replace(",", ".").replace(" ", ""))
    if len(fields[1].strip()) > 0:
        v2 = float(fields[1].replace(",", "."))

    return v1, v2

def extract_info(line, flat_info):

    fields = line.split(":")
    if len(fields) < 2:
        print line
        return flat_info

    key = line.split(":")[0].strip()
    value = line.split(":")[1].strip()

    if len(value) < 1:
        return flat_info

    if key == "price" or key == "price-per-m2" or key == "asked-price" or key == "land-area" or \
                    key == "supplemental-area":
        flat_info[key] = string2float(value)
    elif key == "living-area":
        (flat_info["living-area-m2"], flat_info["living-area-rooms"]) = parse_living_area(value)
    else:
        flat_info[key] = value.decode("utf-8")

    return flat_info

"""
price :  2 340 000
price-per-m2 : 15 918
asked-price : 1 995 000
land-area : 2 732
supplemental-area : 24


sold-date : 2015-09-07
address : Sörfors 845
area : Sörfors
city :
broker : Svensk Fastighetsförmedling
living-area : 147 m2;4 rum
flat_type : Friliggande villa
"""

def load_data(input_file):
    flat_info = get_empty_dict()
    found_flat_info = False
    flats = []
    for l in open(input_file):
        if l.startswith("-------"):
            if found_flat_info:
                f = flat.Flat(**flat_info)
                flats.append(f)
                flat_info = get_empty_dict()
                found_flat_info = False
        else:
            found_flat_info = True
            flat_info = extract_info(l, flat_info)
    if found_flat_info:
        f = flat.Flat(**flat_info)
        flats.append(f)

    return flats

def save_data_to_file(flats, outfile):
    the_keys = get_empty_dict().keys()
    the_keys.sort()

    outf = codecs.open(outfile, "w", "utf-8")
    outf.write(u"\t".join(the_keys) + "\n")
    for f in flats:
        k = the_keys[0]
        outf.write(f.__dict__[k])
        for k in the_keys[1:]:
            v = f.__dict__[k]
            if type(v) == float or type(v) == int:
                v = str(v)
            outf.write(u"\t" + v)
        outf.write("\n")

    outf.close()


def main():
    flats = load_data(INPUT_FILE)
    save_data_to_file(flats, "sold_flats_formatted.txt")

if __name__ == '__main__':
    main()