#!/usr/bin/env python3
#################################################################################
import csv
from typing import List, Dict


###
def generate_prototype_dict(csvfile: str, delimiter=',') -> List[Dict]:
    """
    generate prototype
    :param delimiter:
    :param csvfile: a csv file of following format, first line is header
            a,b,c
            1,t1,4
            1,t2,56
    :return: list of dictionaries
    """
    if csvfile:
        with open(csvfile, mode='r') as infile:
            file_data = csv.reader(infile, delimiter=delimiter)
            headers = next(file_data)
            return [dict(zip(headers, i)) for i in file_data]


###
def generate_prototype_obj(csvfile: str, delimiter=',') -> List[object]:
    """
    generate prototype
    :param delimiter:
    :param csvfile: a csv file of following format, first line is header
            a,b,c
            1,t1,4
            1,t2,56
    :return: list of on the fly objects
    """
    if csvfile:
        with open(csvfile, mode='r') as infile:
            file_data = csv.reader(infile, delimiter=delimiter)
            headers = next(file_data)
            return [type('prototype', (object,), dict(zip(headers, i))) for i in file_data]


###
def main():
    data = generate_prototype_dict(csvfile = "data/config.csv")
    print(*data, sep = "\n")
    print("\n")

    uuid_dict = { i['uuid'] : i for i in data}
    print(uuid_dict)
    print("\n")

    data = generate_prototype_obj(csvfile = "data/config.csv")
    [print(vars(i)) for i in data]
    print(data[2].uuid)

    setattr(data[4], 'name', 'test123')
    print(data[4].name)
    name = getattr(data[4], 'name')
    print(name)
    print(hasattr(data[4], "age"))


###
if __name__ == "__main__":
    main()

