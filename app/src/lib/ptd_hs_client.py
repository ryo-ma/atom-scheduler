import requests
import glob
import zipfile
import os


class PTDHSClient:
    def __init__(self):
        self.uid = os.environ.get('PTD_HS_UID')
        self.endpoint = os.environ.get('PTD_HS_ENDPOINT')

    def get_agency_list(self):
        response = requests.get(f'{self.endpoint}/GetAgencyList')
        return response

    def get_agency_detail(self, agency_id):
        payload = {'agency_id': agency_id}
        response = requests.get(f'{self.endpoint}/GetAgencyDetail', params=payload)
        return response

    def get_vehicle_position(self, agency_id):
        payload = {'agency_id': agency_id,
                   'output': 'json',
                   'uid': self.uid}
        response = requests.get(f'{self.endpoint}/GetVehiclePosition', params=payload)
        return response

    def get_trip_update(self, agency_id):
        payload = {'agency_id': agency_id,
                   'output': 'json',
                   'uid': self.uid}
        response = requests.get(f'{self.endpoint}/GetTripUpdate', params=payload)
        return response

    def download_data(self, agency_id, version):
        payload = {'agency_id': agency_id,
                   'version': version,
                   'uid': self.uid}
        filename = f'{agency_id}_{version}'
        if not os.path.exists(f'output/{filename}'):
            response = requests.get(f'{self.endpoint}/GetData', params=payload, stream=True)
            with open(f'output/{filename}.zip', 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                filename = self.__zip_extract(filename)

        if self.__exists_dir(f'output/{filename}'):
            return glob.glob(f'output/{filename}/*')[0].replace('output/', '')
        return filename

    def __zip_extract(self, filename):
        target_directory = f'output/{filename}'
        zfile = zipfile.ZipFile(f'{target_directory}.zip')
        zfile.extractall(target_directory)
        return filename

    @staticmethod
    def __exists_dir(filename):
        return len(glob.glob(f'{filename}/*')) == 1 and os.path.isdir(filename)

