class Departure_fetcher:
    '''This class contains fuctions used to fetch departure data from trafiklabb for a specific stop'''
    import pandas as pnd
    import json as jsn
    import requests

    def __init__(self):
        self.data = self.pnd.read_csv("stop_karlskrona.csv", encoding="utf-8")

    def load_data(self, id):
        '''This function takes an id that it uses to fetch stop data from the trafiklabb stop lookup api'''
        dp = self.jsn.loads(self.requests.get(f'https://realtime-api.trafiklab.se/v1/departures/{id}?key=87f27410146c46db9278c92ee7b0ea28').text)
        df = self.pnd.json_normalize(dp["departures"])
        return df

    def search_stop_id(self, stop:str):
        '''Function that takes a string which it uses to search for a stop with a matching name in the stop_karlskrona.csv dataset'''
        for index, stops in self.data.iterrows(): #Loops through the rows in the stop_karlskrona.csv dataset
            if stop.lower() == stops["stop_name"].lower(): #Checks if provided string matches stop name
                get_id = self.jsn.loads(self.requests.get(f"https://realtime-api.trafiklab.se/v1/stops/name/{stop}/?key=87f27410146c46db9278c92ee7b0ea28").text)
                id = get_id["stop_groups"][0]["id"] #extracts stop id. (This can be modified to display multiple stops with a similar name to the provided string if needed)
                return id
        return None
    
    def print_data(self):
        '''Prints data in stop_karlskrona.csv'''
        print(self.data.to_string())
        return

    def departures(self, origin:str):
        '''This function forwards an id provided by the search_stop_id fuction to the load_data function in order to fetch departure data for a specific stop. Takes a string that gets forwarded to the search_stop_id fuction.'''
        id = self.search_stop_id(origin)
        if id is None:
            return print("Detta stopp ligger inte inom karlskrona kommun")

        departure_data = self.load_data(id) # Forwards id to load_data fucntion
           # for time in sussybaka["realtime"]:
            #    time = time.spl
        departure_time = departure_data[["route.direction", "realtime", "route.transport_mode"]] #Creates a new datafame which only contains relevant departure data
        return print(departure_time.to_string()) # Prints relevant departure data


def main():
    datahandler = Departure_fetcher()
    datahandler.departures(input("vart åker du ifrån? "))

main()