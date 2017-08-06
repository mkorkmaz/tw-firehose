#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# author: mehmet@mkorkmaz.com
# last_updated: 2016-04-07

import os
from twython import TwythonStreamer
import simplejson as json
import myutils

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = myutils.read_yaml(BASE_DIR + '/config.ini')
additional_data = config['additional_data']
id_prefix = str(additional_data['id_prefix'])  # makes sure that id_prefix is a string
additional_data.pop("id_prefix", None)


class MyStreamer(TwythonStreamer):

    def on_success(self, tweet_data):
        if 'text' in tweet_data:
            doc_id = id_prefix + '_' + tweet_data['id_str']
            data = {**additional_data, **tweet_data}
            json.dump(data, open('./data/' + tweet_data['id_str'] + '.json', 'w'))
            print("Document indexed: ", tweet_data['id_str'])

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
