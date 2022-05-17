import os


def write_message_to_file(file_name="lamp_config.txt", path="", text=""):
    if not os.path.exists(path):
        os.makedirs(path)

    file_handler = open(os.path.join(path, file_name), "w+")
    file_handler.write(text)
    file_handler.close()
