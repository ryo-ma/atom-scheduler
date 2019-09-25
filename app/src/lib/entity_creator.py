

class EntityCreator:

    def create_static_entity(self, dict_data, entity_type, id_rule):
        entities = []
        for x in dict_data:
            entity = {'id': id_rule(x),
                      'type': entity_type}
            for k, v in dict(x).items():
                entity[k] = self.create_attribute(v)
            entities.append(entity)
        return entities

    def create_vehicle_position(self, json_dict_data):
        entities = []
        for x in json_dict_data['entity']:
            vehicle_id = x['vehicle']['vehicle']['id']
            trip = x['vehicle']['trip']
            position = x['vehicle']['position']
            entity = {'id': vehicle_id,
                      'type': 'vehicle_position',
                      'schedule_relation_ship': self.create_attribute(trip['scheduleRelationship']),
                      'route_id': self.create_attribute(trip['routeId']),
                      'latitude': self.create_attribute(position['latitude'], 'Number'),
                      'longitude': self.create_attribute(position['longitude'], 'Number'),
                      'current_status': self.create_attribute(x['vehicle']['currentStatus']),
                      'timestamp': self.create_attribute(int(x['vehicle']['timestamp']), 'Number'),
                      'stop_id': self.create_attribute(x['vehicle']['stopId']),
                      }
            if 'bearing' in position:
                entity['bearing'] = self.create_attribute(position['bearing'])
            if 'tripId' in trip:
                entity['trip_id'] = self.create_attribute(trip['tripId'])
                entity['current_stop_sequence'] = self.create_attribute(x['vehicle']['currentStopSequence'])
            entities.append(entity)
        return entities

    def create_trip_update(self, json_dict_data):
        entities = []
        for x in json_dict_data['entity']:
            vehicle_id = x['tripUpdate']['vehicle']['id']
            trip = x['tripUpdate']['trip']
            for stop_time_update in x['tripUpdate']['stopTimeUpdate']:

                entity = {'id': f'{vehicle_id}_{stop_time_update["stopId"]}',
                          'type': 'trip_update',
                          'vehicle_id': self.create_attribute(vehicle_id),
                          'stop_id': self.create_attribute(stop_time_update['stopId']),
                          'route_id': self.create_attribute(trip['routeId']),
                          'arrival_time': self.create_attribute(int(stop_time_update['arrival']['time']), 'Number'),
                          'departure_time': self.create_attribute(int(stop_time_update['departure']['time']), 'Number'),
                          'schedule_relation_ship': self.create_attribute(stop_time_update['scheduleRelationship'])
                          }
                if 'delay' in stop_time_update['arrival']:
                    entity['arrival_delay'] = self.create_attribute(stop_time_update['arrival']['delay'], 'Number')
                if 'delay' in stop_time_update['departure']:
                    entity['departure_delay'] = self.create_attribute(stop_time_update['departure']['delay'], 'Number')
                if 'uncertainty' in stop_time_update['arrival']:
                    entity['arrival_uncertainty'] = self.create_attribute(stop_time_update['arrival']['uncertainty'],
                                                                          'Number')
                if 'uncertainty' in stop_time_update['departure']:
                    entity['departure_uncertainty'] = self.create_attribute(stop_time_update['departure']['uncertainty'],
                                                                            'Number')
                if 'stopSequence' in stop_time_update:
                    entity['stop_sequence'] = self.create_attribute(stop_time_update['stopSequence'])
                if 'tripId' in trip:
                    entity['trip_id'] = self.create_attribute(trip['tripId'])
                entities.append(entity)
        return entities

    @staticmethod
    def create_attribute(value, attribute_type='string'):
        return {'value': value, 'type': attribute_type}
