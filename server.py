#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
import os.path
import configparser
from config.config import CONFIG_DIR

app = Flask(__name__, template_folder='tpl')
if not os.path.isfile(CONFIG_DIR):
    raise Exception("The config path is invalid!")

config = configparser.ConfigParser()


@app.route('/', methods=['GET'])
def index():
    config.read(CONFIG_DIR)
    info = {'to_number': config["DEFAULT"]["TO_NUMBER"],
            'sleep_after_call': config["DEFAULT"]["SLEEP_AFTER_CALL"],
            'from_number': config["TWILIO"]["FROM_NUMBER"], }

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
    app.run(debug=True, port=5000, host='0.0.0.0')
