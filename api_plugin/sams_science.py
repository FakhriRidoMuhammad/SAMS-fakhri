import requests


class SamsApi:
    def __init__(self):
        self.url = "https://sams.science.itf.llu.lv/api/test/"

    def post_dataset(self, dataset):
        try:
            response = requests.post("{0}".format(self.url), data=dataset)
            if response.ok:
                return True
            else:
                return response.status_code
        except Exception as e:
            return False
