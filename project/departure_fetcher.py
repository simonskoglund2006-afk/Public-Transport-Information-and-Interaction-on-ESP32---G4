class Departure_fetcher:
    '''This class contains fuctions used to fetch departure data from trafiklabb for a specific stop'''
    import json as jsn
    import requests

    def __init__(self):
        with open("Karlskrona.json", encoding="utf-8") as f:
            self.data = self.jsn.load(f)
            f.close()

    def load_data(self, id):
        '''This function takes an id that it uses to fetch stop data from the trafiklabb stop lookup api'''
        dp = self.jsn.loads(self.requests.get(f'https://realtime-api.trafiklab.se/v1/departures/{id}?key=87f27410146c46db9278c92ee7b0ea28').text)
        return dp
    
    def print_data(self, texte): # omformatera till json shit
        '''Prints data in stop_karlskrona.csv'''
        print(self.data)
        return

    def departures(self, origin:str): # omformatera till json shit
        '''This function forwards an id provided by the search_stop_id fuction to the load_data function in order to fetch departure data for a specific stop. Takes a string that gets forwarded to the search_stop_id fuction.'''
        relevant_departure_data = []
        for index in self.data.values():
            if index["stop_name"].lower() == origin.lower():
                departure_data = self.load_data(index["stop_id"])
                for inde in departure_data["departures"]:
                    direction = inde["route"]["direction"]
                    time = inde["realtime"]
                    transport = inde["route"]["transport_mode"]
                    relevant_departure_data.append({"route_direction" : direction, "departure_time" : time, "transport_mode" : transport})
        return relevant_departure_data # returns relevant departure data