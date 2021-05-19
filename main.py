import configparser
import json

from os.path import realpath, dirname, expanduser
from time import sleep

from chia.client import MqttClient
from chia.status import ChiaStatus
from chia.helper import Helper

global mqtt


def publish_status(state, topic):

    global mqtt

    payload = json.dumps(state.attributes)
    mqtt.publish(topic, payload, qos=1, retain=True)


def main():

    global mqtt

    script_dir = dirname(realpath(__file__))
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read("{}/config.ini".format(script_dir))

    mqtt_host = config.get('MQTT', 'Host')
    mqtt_user = config.get('MQTT', 'User')
    mqtt_pass = config.get('MQTT', 'Pass')
    mqtt_port = int(config.get('MQTT', 'Port'))
    mqtt_topic = config.has_option("STATUS", 'MqttTopic') and config.get("STATUS", 'MqttTopic') or None

    logfile = expanduser(config.get("STATUS", 'Logfile'))
    loglevel = config.get('STATUS', 'Loglevel')

    interval = config.has_option("STATUS", 'Interval') and int(config.get("STATUS", 'Interval')) or None

    logger = Helper.init_logger(logfile, level=loglevel)
    mqtt = MqttClient(mqtt_user, mqtt_pass, mqtt_host, mqtt_port)
    mqtt.set_logger(logger)

    while True:

        chia = ChiaStatus()
        chia.set_logger(logger)

        # Publish Farm status
        farm = chia.farm()
        keys = chia.keys()
        topic = mqtt_topic.format(keys.farm_key)
        publish_status(farm, topic)

        # Go to sleep...
        sleep(interval)


if __name__ == '__main__':
    main()
