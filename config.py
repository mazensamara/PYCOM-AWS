
# wifi configuration
WIFI_SSID = 'YOUR_SSID'
WIFI_PASS = 'YOUR_SSID_PASSWORD'

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'YOUR_AWS_HOST' # Connect to aws from pycom
AWS_ROOT_CA = '/flash/cert/AmazonRootCA1.pem' # Root CA
AWS_CLIENT_CERT = '/flash/cert/certificate.pem.crt' # Client CA
AWS_PRIVATE_KEY = '/flash/cert/private.pem.key' # Private Key

################## Subscribe / Publish client #################
CLIENT_ID = 'Mazen_pyscan_1' # AWS created device name
TOPIC = 'Mazen_test' # Publish topic to AWS
TOPIC_1 = 'Mazen_test_1' # Subscribe topic from AWS
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
LAST_WILL_TOPIC = 'Mazen_test'
LAST_WILL_MSG = 'To All: Last will message'

####################### Shadow updater ########################
THING_NAME = "Mazen_pyscan_1"
CLIENT_ID = "ShadowUpdater"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5

####################### Delta Listener ########################
THING_NAME = "Mazen_pyscan_1"
CLIENT_ID = "DeltaListener"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5

####################### Shadow Echo ########################
THING_NAME = "Mazen_pyscan_1"
CLIENT_ID = "ShadowEcho"
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
