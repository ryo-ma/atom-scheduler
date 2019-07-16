import os
import time
import json
from src.lib.ptd_hs_client import PTDHSClient
from src.utils import const
from src.lib.entity_creator import EntityCreator
from src.lib.orion import update_entities
from logging import getLogger
import logging.config


try:
    with open(const.LOGGING_JSON, 'r') as f:
        logging.config.dictConfig(json.load(f))
        if (const.LOG_LEVEL in os.environ and
                os.environ[const.LOG_LEVEL].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            for handler in getLogger().handlers:
                if handler.get_name() in const.TARGET_HANDLERS:
                    handler.setLevel(getattr(logging, os.environ[const.LOG_LEVEL].upper()))
except FileNotFoundError:
    print(f'can not open {const.LOGGING_JSON}')
    pass

sleep_time = os.environ.get(const.SLEEP_TIME, 10)
client = PTDHSClient()


def update_vehicle_position(agency_id):
    vehicle_position_json = client.get_vehicle_position(agency_id).json()
    if 'entity' in vehicle_position_json:
        entities = EntityCreator().create_vehicle_position(vehicle_position_json)
        data = {'actionType': 'APPEND',
                'entities': entities}
        static_agency_id = const.AGENCY_ID_TABLE[agency_id]
        update_entities(f'/agencies/{static_agency_id}', json.dumps(data))


def update_trip_update(agency_id):
    trip_update_json = client.get_trip_update(agency_id).json()
    if 'entity' in trip_update_json:
        id_list = [x['vehicle']['vehicle']['id'] for x in trip_update_json['entity']]
        # TODO: This method will run update_entities.


def run_scheduler(agency_id_list):
    for agency_id in agency_id_list:
        update_vehicle_position(agency_id)
        time.sleep(int(sleep_time))


if __name__ == '__main__':
    agency_list = client.get_agency_list().json()['Agency']
    agency_id_list = [x['agency_id'] for x in agency_list]
    while True:
        run_scheduler(agency_id_list)
