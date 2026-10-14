class Datahandler:
    import pandas as pnd
    import json as jsn
    import requests

    def __init__(self):
        self.data = self.pnd.read_csv("stop_karlskrona.csv", encoding="utf-8")

    def load_data(self, id):
        dp = self.jsn.loads(self.requests.get(f'https://realtime-api.trafiklab.se/v1/departures/{id}?key=87f27410146c46db9278c92ee7b0ea28').text)
        df = self.pnd.json_normalize(dp["departures"])
        return df

    def search_stop_id(self, stop:str):

        for index, stops in self.data.iterrows():
            if stop.lower() == stops["stop_name"].lower():
                get_id = self.jsn.loads(self.requests.get(f"https://realtime-api.trafiklab.se/v1/stops/name/{stop}/?key=87f27410146c46db9278c92ee7b0ea28").text)
                id = get_id["stop_groups"][0]["id"]
                return id
        return None
    
    def print_data(self):
        print(self.data.to_string())
        return

    def departures(self, origin:str):
        id = self.search_stop_id(origin)
        if id is None:
            return print("Detta stopp ligger inte inom karlskrona kommun")

        departure_data = self.load_data(id)
           # for time in sussybaka["realtime"]:
            #    time = time.spl
        departure_time = departure_data[["route.direction", "realtime", "route.transport_mode"]]
        return print(departure_time.to_string())


def main():
    datahandler = Datahandler()
    datahandler.departures(input("vart åker du ifrån? "))

main()