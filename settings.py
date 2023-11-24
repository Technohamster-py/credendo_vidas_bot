import configparser as cp
import os


def create_config(path="settings.ini"):
    """
    Creating a config file
    :param path:
    :return:
    """
    config = cp.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "token", "0")

    with open(path, 'w') as config_write:
        config.write(config_write)


def load_config(path="settings.ini"):
    """
    Loading settings from config file
    :param path: path of settings file
    :return:
    """
    if not os.path.exists(path):
        create_config(path)

    config = cp.ConfigParser()
    config.read(path)

    return config
