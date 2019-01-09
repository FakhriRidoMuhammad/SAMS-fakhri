import json
import os


class Log:
    def __init__(self):
        self.path = '/home/pi/log/'

    def insert(self, json_data):
        files = os.listdir(self.path)
        file = max(files)
        file = int(file[:-5]) + 1
        try:
            with open(self.path + str(file) + ".json", 'w') as f:
                json.dump(json_data, f)
                f.close()
        except Exception as e:
            print(e)

    def post_logfiles(self):
        files = os.listdir(self.path)
        # Falls Dateien vorhanden
        # Dateien nacheinander auslesen, EINEN Datensatz versuchen zu schicken.
        # Wenn das nicht funktioniert, neuen Datensatz speichern
        # Und so lange wieder versuchen bis Raspi aus geht
