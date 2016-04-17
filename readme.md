# Twitter Firehose Service

A simple [Twitter Firehose  Filter Service](https://dev.twitter.com/streaming/overview) script writter in Python.
It simply collects filtered tweets and stores them on Elasticsearch.

###Tags
\#python, #python3, #twiter, #streamingapi, #firehose, #elasticsearch

### Installation
Install the latest versions of required packages
```
$ pip3 install -r pip.install
```
Don't forget to create a new twitter app at (https://apps.twitter.com/) If you haven't yet.

You will need Twitter api_key, api_secret, access_token and access_token_secret.
You can find and/or create them at "Keys and Access Tokens" tab of your Twitter app details page.

### Configuration
Copy config.sample.ini to same folder with firehose.py as config.ini and change variables.

One firehose service can serve for up to [400 keywords](https://dev.twitter.com/streaming/reference/post/statuses/filter).
But I don't recommend to use more than 9-10 keywords.
If you chose a common keyword as a filter, use one dedicated service for it.

### Server Configuration Recommendation
I personally use mostly Ubuntu Server.
For the firehose service I recommend you to use any VPS server has 1 CPU and 512MB RAM or 1 CPU and 1GB RAM.
Since this service does not support multithreading more than 2 CPU core would be useless.

Twitter allows one firehose connection per IP address. This means you can use only one firehose service for one server. [CitationNeeded].

Use more than one servers has small resources than one server has more resources if you need.

Read more details on Twitter's Streaming Documentation's [connection page](https://dev.twitter.com/streaming/overview/connecting).

### Usage

```
$ python3 ./firehose.py
```

### Ubuntu Upstart Service

Create a configuration file at **/etc/init/tw_firehose.conf** with following contents. Change the file path according to your setup.

```
description "Twitter Firehose Filter Service"
author "mehmet@mkorkmaz.com"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid nobody
setgid nogroup

exec python3 /home/userhome/firehose.py
```

**Service management**

```
sudo service tw_firehose start|stop|restart
```