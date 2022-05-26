import os


def write_message_to_file(file_name="lamp_config.txt", path="", text=""):
    if not os.path.exists(path):
        os.makedirs(path)

    file_handler = open(os.path.join(path, file_name), "w+")
    file_handler.write(str(text))
    file_handler.close()


def read_message_from_file(file_name, path):
    if not os.path.exists(path):
        return "Path does not exist."

    file_handler = open(os.path.join(path, file_name), "r")
    current_chat_id = file_handler.read()
    file_handler.close()
    return current_chat_id
