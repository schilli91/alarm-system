from twilio.rest import Client
from time import sleep
import configparser
import os.path
from config.config import CONFIG_DIR

if not os.path.isfile(CONFIG_DIR):
    raise Exception("The config path is invalid!")

config = configparser.ConfigParser()


def make_call(is_dev=False):
    config.read(CONFIG_DIR)
    account_sid = config["TWILIO"]["ACCOUNT_SID"]
    auth_token = config["TWILIO"]["AUTH_TOKEN"]
    to_number = config["DEFAULT"]["TO_NUMBER"]
    from_number = config["TWILIO"]["FROM_NUMBER"]
    call_url = config["TWILIO"]["CALL_URL"]

    if is_dev:
        print('making call...')
    client = Client(account_sid, auth_token)
    call = client.calls.create(to=to_number,
                               from_=from_number,
                               url=call_url)
    if is_dev:
        print(call.sid)
        print("now sleep for {} seconds...".format(int(config["DEFAULT"]["SLEEP_AFTER_CALL"])))
    sleep(int(config["DEFAULT"]["SLEEP_AFTER_CALL"]))
    if is_dev:
        print("wake up...")
