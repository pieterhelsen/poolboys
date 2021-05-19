
import json

import paho.mqtt.client as mqtt


class MqttClient:

    def __init__(self, username, password, host, port, topic='', autodiscovery=True):

        # set method vars
        self.state_topic = topic
        self._autodiscovery = autodiscovery
        self._user = username
        self._pass = password
        self._host = host
        self._port = port

        # init vars
        self.discovery_topic = ''
        self.sensors = None
        self._logger = None

        # init client
        self._init_mqtt()

    def _init_mqtt(self):

        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.username_pw_set(self._user, self._pass)
        self.client.connect(self._host, self._port)
        self.client.reconnect_delay_set()
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):

        if self._logger:
            self._logger.info("Connected to mqtt")

    def _on_disconnect(self, client, userdata, rc):

        if self._logger:
            self._logger.error("Disconnected from mqtt: {}".format(rc))

        self.client.loop_stop()

    def publish(self, topic, payload=None, qos=0, retain=False, properties=None, logging=True):

        if self._logger and logging:
            self._logger.debug("Message sent - {0} - {1}".format(topic, str(payload)))

        self.client.publish(topic, payload, qos, retain, properties)

    def subscribe(self, topic, qos=0, options=None, properties=None, logging=True):

        if self._logger and logging:
            self._logger.info("Subscribed to topic - {0}".format(topic))

        self.client.subscribe(topic, qos, options, properties)

    def discover(self, state_topic, unit, template, name, sensor_type='sensor', friendly_name='',
                 attributes_topic=None, attributes_template=None):

        # raise RuntimeWarning('Auto Discovery is turned off')

        raw_data = {
            "state_topic": state_topic,
            "value_template": template,
            "name": name
        }

        if unit:
            raw_data["unit_of_measurement"] = unit

        if attributes_topic:
            raw_data["json_attributes_topic"] = attributes_topic

        if attributes_template:
            if not attributes_topic:
                raise ValueError('attributes_template is defined, but attributes_topic is missing.')

            raw_data["json_attributes_template"] = attributes_template

        payload = json.dumps(raw_data)

        self.discovery_topic = "homeassistant/" + sensor_type + "/" + name + "/config"
        self.publish(self.discovery_topic, payload)

    def discover_all(self, sensors):

        # raise RuntimeWarning('Auto Discovery is turned off')

        self.sensors = sensors

        for sensor in self.sensors:
            if 'topic' not in sensor.keys():
                sensor["topic"] = self.state_topic
            if 'type' not in sensor.keys():
                sensor["type"] = 'sensor'
            if 'unit' not in sensor.keys():
                sensor["unit"] = None
            if 'friendly_name' not in sensor.keys():
                sensor["friendly_name"] = sensor["name"]
            if 'attributes_topic' not in sensor.keys():
                sensor["attributes_topic"] = None

            self.discover(sensor["topic"], sensor["unit"], sensor["template"], sensor["name"],
                          sensor_type=sensor["type"], friendly_name=sensor["friendly_name"],
                          attributes_topic=sensor["attributes_topic"])

    def set_logger(self, logger):

        self._logger = logger
