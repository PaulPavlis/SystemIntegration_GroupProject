import time
import sys
import os
import stomp
import constants as keys
import json


class MyIOTListener(object):

    def __init__(self, conn, func):
        self.conn = conn
        self.func = func

    def on_error(self, message):
        print(f"Received an error: {message}")

    def parse_json_to_text(self, json_dict):
        return f"Return Message: {json_dict['message']}"

    def on_message(self, header, body):
        print(f"Received ActiveMQ message: {body}")
        return_text = self.parse_json_to_text(json.loads(body))
        self.func(return_text)


def get_activemq_subscriber(func):
    conn = stomp.Connection(host_and_ports=[(keys.HOST, keys.PORT)])
    conn.set_listener('', MyIOTListener(conn, func))
    conn.connect(login=keys.USER, passcode=keys.PASSWORD)

    id_counter = 1
    for subscribe_topic in keys.SUBSCRIBE_TOPICS:
        conn.subscribe(destination=subscribe_topic, id=id_counter, ack='auto')
        id_counter += 1

    return conn
