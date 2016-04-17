# -*- coding: utf-8 -*-

# author: mehmet@mkorkmaz.com
# last_updated: 2016-03-12

import ujson as json
import yaml


def json_serializer(key, value):
    key = None
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")


def is_json(my_json):

    try:
        json_object = json.loads(my_json)
    except ValueError as e:
        return False
    return True


def dict_isset_or(obj, indice, default_value):

    if indice in obj:
        return obj[indice]
    else:
        obj[indice] = default_value
        return obj[indice]


def read_yaml(file_name):
    with open(file_name, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(file_name)
            print("Configuration file error! Exiting...")
            exit()
