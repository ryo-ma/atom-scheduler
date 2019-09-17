import csv
import json
import os
from src.lib.ptd_hs_client import PTDHSClient
from src.lib.entity_creator import EntityCreator
from src.lib import orion
from src.utils.split_list import split_list
from src.utils import const


def download_current_all_data():
    client = PTDHSClient()
    agency_list = client.get_agency_list().json()['Agency']
    download_info_list = []
    for agency in agency_list:
        version = agency['current_version'].replace(' ', '').replace('/', '').replace(':', '')
        filename = client.download_data(agency['agency_id'], version)
        download_info_list.append({'filename': filename, 'agency_id': agency['agency_id']})
    return download_info_list


def update_entity(download_info):
    path = download_info['filename']
    agency_id = download_info['agency_id']
    entity_param_list = [
        {
            'filename': 'stops.txt',
            'type': 'stop',
            'id_rule': lambda x: x['stop_id']
        },
        {
            'filename': 'routes.txt',
            'type': 'route',
            'id_rule': lambda x: x['route_id']
        },
        {
            'filename': 'trips.txt',
            'type': 'trip',
            'id_rule': lambda x: x['trip_id']
        },
        {
            'filename': 'stop_times.txt',
            'type': 'stop_time',
            'id_rule': lambda x: f"{x['trip_id']}_{x['stop_id']}"
        },
        {
            'filename': 'calendar.txt',
            'type': 'calendar',
            'id_rule': lambda x: x['service_id']
        },
        {
            'filename': 'calendar_dates.txt',
            'type': 'calendar_date',
            'id_rule': lambda x: f"{x['service_id']}_{x['date']}"
        },
        {
            'filename': 'fare_attributes.txt',
            'type': 'fare_attribute',
            'id_rule': lambda x: f"{x['fare_id']}"
        },
        {
            'filename': 'fare_rules.txt',
            'type': 'fare_rule',
            'id_rule': lambda x: f"{x['fare_id']}_{x['route_id']}"
        },
        {
            'filename': 'pass_attributes.txt',
            'type': 'pass_attribute',
            'id_rule': lambda x: f"{x['pass_id']}"
        },
        # {
        #     'filename': 'pass_rules.txt',
        #     'type': 'calendar_date',
        #     'id_rule': lambda x: f"{x['pass_id']}_{x['route_id']}"
        # },
        # {
        #     'filename': 'shapes.txt',
        #     'type': 'shape',
        #     'id_rule': lambda x: f"{x['shape_id']}_{x['shape_pt_sequence']}"
        # }
    ]
    entity_creator = EntityCreator()

    # Update the agency entity with the agency_jp.
    agency_filename = f'output/{path}/agency.txt'
    agency_jp_filename = f'output/{path}/agency_jp.txt'
    with open(agency_filename, 'r', encoding='utf-8-sig') as agency_f:
        with open(agency_jp_filename, 'r', encoding='utf-8-sig') as agency_jp_f:
            agency_dict = dict(list(csv.DictReader(agency_f))[0])
            agency_jp_list = list(csv.DictReader(agency_jp_f))
            if len(agency_jp_list) != 0:
                agency_jp_dict = dict(agency_jp_list[0])
                agency_dict.update(agency_jp_dict)
            entities = entity_creator.create_static_entity([agency_dict],
                                                           'agency',
                                                           lambda x: x['agency_id'])
            data = {'actionType': 'APPEND',
                    'entities': entities}
            orion.update_entities(f'/agencies/{agency_id}', json.dumps(data))

    # Update the other entities.
    post_entities_length = os.environ.get(const.POST_ENTITIES_LENGTH, 3)
    for entity_param in entity_param_list:
        file_path = f'output/{path}/{entity_param["filename"]}'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                data_list = list(csv.DictReader(f))
                entities = entity_creator.create_static_entity(data_list,
                                                               entity_param['type'],
                                                               entity_param['id_rule'])
                # Split entities data, Because requests can't post too many entities.
                for splited_entities in split_list(entities, int(post_entities_length)):
                    data = {'actionType': 'APPEND',
                            'entities': splited_entities}
                    orion.update_entities(f'/agencies/{agency_id}', json.dumps(data))


if __name__ == '__main__':
    for download_info in download_current_all_data():
        update_entity(download_info)
