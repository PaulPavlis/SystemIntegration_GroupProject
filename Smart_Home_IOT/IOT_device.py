import time
import sys
import os
import stomp
import constants as keys
from file_handler import write_message_to_file
from activemq_publish_handler import send_message_2_queue
import json
import random
from argparse import ArgumentParser

# Disclaimer: It would have been better to create a file as subscribe
# handler and pass functions to it for better seperation of code.
# Since it does not matter for this student project I will not rewrite it


class MyIOTListener(stomp.ConnectionListener):

    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    def on_error(self, message):
        print(f"Received an error: {message}")

    def parse_json_to_text(self, json_dict):
        new_line = "\n"
        return f"Brightness: {json_dict['brightness']}{new_line}Colour: {json_dict['colour_hexadecimal']}{new_line}Special Effect: {json_dict['special_effect']}"

    def get_return_json(self):
        return {
            "message": f"IOT Device {self.name} updated."
        }

    def on_message(self, header, body):
        print(f"Received ActiveMQ message (Header): {header}")
        print(f"Received ActiveMQ message (Body): {body}")

        config_text = self.parse_json_to_text(json.loads(body))
        time.sleep(random.randint(1, 2))
        write_message_to_file("config.txt",
                              "Smart_Home_IOT\\" + str(self.name).replace(" ", ""), config_text)
        print(f"Changed IOT device according to message.")

        json_message = self.get_return_json()
        json_string = json.dumps(json_message)
        send_message_2_queue(keys.HOST, keys.PORT,
                             keys.USER, keys.PASSWORD, keys.PUBLISH_TOPIC, json_string)
        print(f"Sent ActiveMQ message to {keys.PUBLISH_TOPIC}: {json_string}")


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--my_name", required=True,
                        help="The name of the IOT Device")
    parser.add_argument("-stl", "--subscribe_topic_list", action="append", required=True,
                        help="The ActiveMQ topics on which to subscribe in the form of a list. Example: -stl /topic/topic_lamp1 -stl /topic/topic_all_lamps")

    args = parser.parse_args()

    conn = stomp.Connection(host_and_ports=[(keys.HOST, keys.PORT)])
    conn.set_listener(args.my_name, MyIOTListener(conn, args.my_name))
    conn.connect(login=keys.USER, passcode=keys.PASSWORD, wait=True)

    id_counter = 1
    for subscribe_topic in args.subscribe_topic_list:
        conn.subscribe(destination=subscribe_topic,
                       headers={}, id=id_counter, ack='auto')
        id_counter += 1

    print(f"IOT Device {args.my_name} (ActiveMQ Receiver) started ...")
    while 1:
        time.sleep(2)
