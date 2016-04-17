#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# author: mehmet@mkorkmaz.com
# last_updated: 2016-04-07

import os
from elasticsearch import Elasticsearch
from twython import TwythonStreamer
import myutils

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = myutils.read_yaml(BASE_DIR + '/config.ini')
additional_data = config['additional_data']
id_prefix = str(additional_data['id_prefix'])  # makes sure that id_prefix is a string
additional_data.pop("id_prefix", None)
es = Elasticsearch([
    {'host': config['data_store']['host']}
])


class MyStreamer(TwythonStreamer):

    def on_success(self, tweet_data):
        if 'text' in tweet_data:
            doc_id = id_prefix + '_' + tweet_data['id_str']
            response = es.get(index=config['data_store']['index'], doc_type=config['data_store']['type'], id=doc_id,
                              ignore=404)
            does_exist = myutils.dict_isset_or(response, 'found', False)
            if does_exist:
                print("Document Exists, skipping:" + doc_id)
            else:
                data = {**additional_data, **tweet_data}
                res = es.index(index=config['data_store']['index'], doc_type=config['data_store']['type'],
                               id=doc_id, body=data)
                print("Document indexed: " + str(res['created'])+doc_id)

    def on_error(self, status_code, data):
        #  @TODO: Handle 420 errors
        print(status_code)


def firehose():
    words = config['keywords']
    tw_config = config['twitter']
    stream = MyStreamer(tw_config['api_key'], tw_config['api_secret'], tw_config['access_token'],
                        tw_config['access_token_secret'])
    stream.statuses.filter(track=words)

if __name__ == '__main__':
    firehose()
