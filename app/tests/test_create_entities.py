import json
import csv
from src.lib.entity_creator import EntityCreator


class TestCreateEntities:

    def test_create_vehicle_position(self):
        with open('./tests/test_data/test_vehicle_position.json', 'r') as f:
            json_data = json.load(f)
            entities = EntityCreator().create_vehicle_position(json_data)
            assert len(entities) == 35

    def test_create_trip_update(self):
        with open('./tests/test_data/test_trip_update.json', 'r') as f:
            json_data = json.load(f)
            entities = EntityCreator().create_trip_update(json_data)
            assert len(entities) == 677

    def test_create_agency(self):
        with open('./tests/test_data/test_static_data/agency.txt', 'r') as agency_f:
            with open('./tests/test_data/test_static_data/agency_jp.txt', 'r') as agency_jp_f:
                agency_dict = dict(list(csv.DictReader(agency_f))[0])
                agency_jp_dict = dict(list(csv.DictReader(agency_jp_f))[0])
                agency_dict.update(agency_jp_dict)
                entities = EntityCreator().create_static_entity([agency_dict],
                                                                'agency',
                                                                lambda x: x['agency_id'])
                assert len(entities) == 1
                assert len(entities[0]) == 15
                assert entities[0]['id'] == '6380001020359'
                assert entities[0]['type'] == 'agency'

    def test_create_stop(self):
        with open('./tests/test_data/test_static_data/stops.txt', 'r') as f:
            stop_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(stop_list,
                                                            'stop',
                                                            lambda x: x['stop_id'])

            assert len(entities) == 2002
            assert len(entities[0]) == 15
            assert entities[0]['id'] == 'S0702000001'
            assert entities[0]['type'] == 'stop'

    def test_create_route(self):
        with open('./tests/test_data/test_static_data/routes.txt', 'r') as f:
            route_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(route_list,
                                                            'route',
                                                            lambda x: x['route_id'])

            assert len(entities) == 147
            assert len(entities[0]) == 12
            assert entities[0]['id'] == 'R070200001000000'
            assert entities[0]['type'] == 'route'

    def test_create_trip(self):
        with open('./tests/test_data/test_static_data/trips.txt', 'r') as f:
            trip_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(trip_list,
                                                            'trip',
                                                            lambda x: x['trip_id'])

            assert len(entities) == 596
            assert len(entities[0]) == 15
            assert entities[0]['id'] == 'T0702000001'
            assert entities[0]['type'] == 'trip'

    def test_create_stop_time(self):
        with open('./tests/test_data/test_static_data/stop_times.txt', 'r') as f:
            stop_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(stop_list,
                                                            'stop_time',
                                                            lambda x: f"{x['trip_id']}_{x['stop_id']}")

            assert len(entities) == 20798
            assert len(entities[0]) == 12
            assert entities[0]['id'] == 'T0702000001_S070200000100400'
            assert entities[0]['type'] == 'stop_time'

    def test_create_calendar(self):
        with open('./tests/test_data/test_static_data/calendar.txt', 'r') as f:
            calendar_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(calendar_list,
                                                            'calendar',
                                                            lambda x: x['service_id'])

            assert len(entities) == 18
            assert len(entities[0]) == 12
            assert entities[0]['id'] == 'S000001'
            assert entities[0]['type'] == 'calendar'

    def test_create_calendar_date(self):
        with open('./tests/test_data/test_static_data/calendar_dates.txt', 'r') as f:
            calendar_date_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(calendar_date_list,
                                                            'calendar_date',
                                                            lambda x: f"{x['service_id']}_{x['date']}")

            assert len(entities) == 261
            assert len(entities[0]) == 5
            assert entities[0]['id'] == 'S000002_20190715'
            assert entities[0]['type'] == 'calendar_date'

    def test_create_shape(self):

        with open('./tests/test_data/test_static_data/shapes.txt', 'r') as f:
            shape_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(shape_list,
                                                            'shape',
                                                            lambda x: f"{x['shape_id']}_{x['shape_pt_sequence']}")

            assert len(entities) == 1572
            assert len(entities[0]) == 7
            assert entities[0]['id'] == 'SP000001_0'
            assert entities[0]['type'] == 'shape'

    def test_create_fare_attributes(self):
        with open('./tests/test_data/test_static_data/fare_attributes.txt', 'r') as f:
            fare_attribute_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(fare_attribute_list,
                                                            'fare_attribute',
                                                            lambda x: f"{x['fare_id']}")

            assert len(entities) == 226
            assert len(entities[0]) == 8
            assert entities[0]['id'] == 'F07020002100'
            assert entities[0]['type'] == 'fare_attribute'

    def test_create_fare_rules(self):
        with open('./tests/test_data/test_static_data/fare_rules.txt', 'r') as f:
            fare_rules_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(fare_rules_list,
                                                            'fare_attribute',
                                                            lambda x: f"{x['fare_id']}")

            assert len(entities) == 63454
            assert len(entities[0]) == 7
            assert entities[0]['id'] == 'F07020002100'
            assert entities[0]['type'] == 'fare_attribute'

    def test_create_pass_attributes(self):
        with open('./tests/test_data/test_static_data/pass_attributes.txt', 'r') as f:
            pass_attributes_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(pass_attributes_list,
                                                            'pass_attribute',
                                                            lambda x: f"{x['pass_id']}")

            assert len(entities) == 448
            assert len(entities[0]) == 6
            assert entities[0]['id'] == 'P070200882001'
            assert entities[0]['type'] == 'pass_attribute'

    def test_create_pass_rules(self):
        with open('./tests/test_data/test_static_data/pass_rules.txt', 'r') as f:
            pass_rules_list = list(csv.DictReader(f))
            entities = EntityCreator().create_static_entity(pass_rules_list,
                                                            'pass_rule',
                                                            lambda x: f"{x['pass_id']}_{x['route_id']}")

            assert len(entities) == 286244
            assert len(entities[0]) == 6
            assert entities[0]['id'] == 'P070200882001_R070200001000000'
            assert entities[0]['type'] == 'pass_rule'
