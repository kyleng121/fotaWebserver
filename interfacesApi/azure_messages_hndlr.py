import json
import sys
from azure.iot.hub import IoTHubRegistryManager

CONNECTION_STRING = "HostName=fotadevices.azure-devices.net;DeviceId=fotamaster;SharedAccessKey=RbmlOfiXgz6tuW4IxERLsMmviJYu+AIzVPG6gP0v1qQ="
DEVICE_ID = "fotamaster"

def send_request_messagses(data,messageType):
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        props={}
        # optional: assign system properties
        props.update(messageId = messageType)

        props.update(contentType = "application/json")

        registry_manager.send_c2d_message(DEVICE_ID, data, properties=props)

    except Exception as ex:
        print ( "Unexpected error" )
        return



