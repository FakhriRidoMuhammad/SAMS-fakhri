import requests


class Api:
    def __init__(self):
        self.url = "https://sams.science.itf.llu.lv/api/test/"

    def post_dataset(self, dataset):
            response = requests.post("{0}".format(self.url), data=dataset)
            if response.ok:
                return True
            else:
                return response.status_code
