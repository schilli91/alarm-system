#!/usr/bin/env python3
import configparser
import logging
import os.path
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for

from config.config import CONFIG_DIR

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder='tpl')
if not os.path.isfile(CONFIG_DIR):
    raise Exception("The config path is invalid!")

config = configparser.ConfigParser()

POLL_STATUS_GREEN = 'status-green'
POLL_STATUS_RED = 'status-red'


@app.route('/', methods=['GET'])
def index():
    poll_status = POLL_STATUS_RED
    try:
        with open('last_poll.txt', 'r') as poll_file:
            last_poll = poll_file.read()
        last_poll_date = datetime.strptime(last_poll, '%d.%m.%Y %H:%M:%S')
        poll_threshold_red = datetime.now() - timedelta(hours=6)

        if poll_threshold_red < last_poll_date:
            poll_status = POLL_STATUS_GREEN

    except OSError:
        last_poll = 'Keine Daten vorhanden.'

    config.read(CONFIG_DIR)
    info = {
        'to_number': config["DEFAULT"]["TO_NUMBER"],
        'sleep_after_call': config["DEFAULT"]["SLEEP_AFTER_CALL"],
        'from_number': config["TWILIO"]["FROM_NUMBER"],
        'last_poll': last_poll,
        'poll_status': poll_status,
    }

    return render_template('index.html', **info)


@app.route('/configs/', methods=['GET'])
def get_configs_page():
    config.read(CONFIG_DIR)
    info = {'to_number': config["DEFAULT"]["TO_NUMBER"],
            'sleep_after_call': config["DEFAULT"]["SLEEP_AFTER_CALL"], }

    return render_template('configs.html', **info)


@app.route('/configs/', methods=['POST'])
def set_configs():
    config.read(CONFIG_DIR)

    to_number = request.form['to_number']
    if to_number != "":
        if to_number[0] == '0':
            to_number = '49{}'.format(to_number[1:])
        config["DEFAULT"]["TO_NUMBER"] = '+{}'.format(int(to_number))

    if request.form['sleep_after_call'] != "":
        config["DEFAULT"]["SLEEP_AFTER_CALL"] = request.form['sleep_after_call']

    with open(CONFIG_DIR, 'w') as file:
        config.write(file)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
