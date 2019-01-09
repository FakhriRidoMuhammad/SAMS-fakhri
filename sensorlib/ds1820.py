class DS1820:
    def __init__(self, wire_id):
        self.id = wire_id

    def get_data(self):
        try:
            file = open('/sys/bus/w1/devices/{0}/w1_slave'.format(self.id))
            file_content = file.read()
            file.close()

            value = file_content.split("\n")[1].split(" ")[9]
            temperature = int(value[2:]) / 1000
            temp = int(round(temperature))

            return temp
        except Exception as e:
            print("Error: {0}".format(e))

