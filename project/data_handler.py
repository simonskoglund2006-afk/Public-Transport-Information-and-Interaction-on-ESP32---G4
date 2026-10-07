class Datahandler:
    import pandas as pnd
    import json as jsn
    import requests

    def __init__(self):
        self.data = None

    def load_data(self, id):
        dp = self.jsn.loads(self.requests.get(f'https://realtime-api.trafiklab.se/v1/departures/73602?key=87f27410146c46db9278c92ee7b0ea28').text)
        df = self.pnd.json_normalize(dp["departures"])
        return df

    def search_stop_id(self, stop):
        with open("stops karlskrona.json", "r", encoding="utf-8") as f:
            data = self.jsn.load(f)
        for groups in data["stop_groups"]:
            if groups["name"] == stop:
                print("nu är jag glad")
                return groups["id"]
        return None
    
    def print_data(self):
        print(self.data.to_string())
        return

    def departures(self, origin:str):
        id = self.search_stop_id(origin)
        print(id)

        departure_data = self.load_data(id)
           # for time in sussybaka["realtime"]:
            #    time = time.spl
        departure_time = departure_data[["route.direction", "realtime", "route.transport_mode"]]
        return print(departure_time.to_string())
        #return print("Detta stop är vid nuläget inte tillgängligt!")


def main():
    datahandler = Datahandler()
    datahandler.departures(input("vart åker du ifrån? "))

main()