class Departure_fetcher:
    '''This class contains fuctions used to fetch departure data from trafiklabb for a specific stop'''
    import json as jsn
    import requests

    def __init__(self):
        with open("stops_karlskrona.json", encoding="utf-8") as f:
            self.data = self.jsn.load(f)
            f.close()

    def load_data(self, id):
        '''This function takes an id that it uses to fetch stop data from the trafiklabb stop lookup api'''
        dp = self.jsn.loads(self.requests.get(f'https://realtime-api.trafiklab.se/v1/departures/{id}?key=87f27410146c46db9278c92ee7b0ea28').text)
        return dp

    def search_stop_id(self, stop:str): # Omformaattera till json shit
        '''Function that takes a string which it uses to search for a stop with a matching name in the stop_karlskrona.csv dataset'''
        for index in self.data:
                for stops in self.data["stop_name"]:  #Loops through the rows in the stop_karlskrona.csv dataset
                    if stop.lower() == stops.lower(): #Checks if provided string matches stop name
                        get_id = self.jsn.loads(self.requests.get(f"https://realtime-api.trafiklab.se/v1/stops/name/{stop}/?key=87f27410146c46db9278c92ee7b0ea28").text)
                        id = get_id["stop_groups"][0]["id"] #extracts stop id. (This can be modified to display multiple stops with a similar name to the provided string if needed)
                        return id
        return None
    
    def print_data(self): # omformatera till json shit
        '''Prints data in stop_karlskrona.csv'''
        print(self.data)
        return

    def departures(self, origin:str): # omformatera till json shit
        '''This function forwards an id provided by the search_stop_id fuction to the load_data function in order to fetch departure data for a specific stop. Takes a string that gets forwarded to the search_stop_id fuction.'''
        id = self.search_stop_id(origin)
        if id is None:
            return print("Detta stopp ligger inte inom karlskrona kommun")

        departure_data = self.load_data(id) # Forwards id to load_data fucntion
        relevant_departure_data = []
        for index in departure_data["departures"]:
            direction = index["route"]["direction"]
            time = index["realtime"]
            transport = index["route"]["transport_mode"]
            relevant_departure_data.append({{"route_direction" : direction, "departure_time" : time, "transport_mode" : transport}})
        print(relevant_departure_data)
        return relevant_departure_data # returns relevant departure data


def main():
    datahandler = Departure_fetcher()
    #datahandler.print_data()
    #datahandler.departures(input("vart åker du ifrån? "))
    datahandler.departures("karlskrona centralstation")

main()