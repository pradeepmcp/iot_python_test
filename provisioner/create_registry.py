import argparse
import io
import os
import sys
import time

from google.api_core.exceptions import AlreadyExists
from google.cloud import iot_v1
from google.cloud import pubsub
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

project_id = 'iot-python-test-project'
cloud_region = 'asia-east1'
pubsub_topic = 'cooker'
pubsub_topic_subfolder = 'water'
registry_id = 'iot-python-test-reg'


def create_registry(project_id, cloud_region, pubsub_topic, registry_id):
    client = iot_v1.DeviceManagerClient()
    parent = client.location_path(project_id, cloud_region)

    if not pubsub_topic.startswith('projects/'):
        pubsub_topic = 'projects/{}/topics/{}'.format(project_id, pubsub_topic)

    pubsub_topic_power = 'projects/{}/topics/power'.format(project_id)

    body = {
        'event_notification_configs': [{
            'pubsub_topic_name': pubsub_topic,
            'subfolder_matches': 'water',
            'subfolder_matches': 'rice' 
        },
        {
            'pubsub_topic_name': pubsub_topic_power,
        }],
        'id': registry_id
    }

    try:
        response = client.create_device_registry(parent, body)
        print('Created registry')
        return response
    except HttpError:
        print('Error, registry not created')
        raise
    except AlreadyExists:
        print('Error, registry already exists')
        raise
    # [END iot_create_registry]



if __name__ == '__main__':
    create_registry(project_id, cloud_region, pubsub_topic, registry_id)
