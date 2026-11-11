
import pandas as pd
import requests as rq
import json
import time
class DataMaxer:

    def __init__(self):
        self.df = pd.read_csv("stops.csv",encoding="utf-8")

    def search_stop_id(self, stop): # Omformaattera till json shit
        '''Function that takes a string which it uses to search for a stop with a matching name in the stop_karlskrona.csv dataset'''
        time.sleep(2.5)
        #result = rq.get(f"https://realtime-api.trafiklab.se/v1/stops/name/{stop}/?key=").json()   
        try: 
            for stopgroup in result["stop_groups"]:
                for sto in stopgroup["stops"]:
                    if self.is_in(sto["lat"], sto["lon"]):
                        return stopgroup["id"]
        except KeyError:
            return None

    def filter(self):
        karlsrkrona = [] #lista att lägga filterade resultat
        
        for index, stop in self.df.iterrows():  #itererar över alla stop inlaggda i dataset
            result = self.is_in(stop["stop_lat"], stop["stop_lon"]) ##kallar is in funktionens
            if result == True: 
                id = self.search_stop_id(stop["stop_name"])
                if id is not None:
                    modified_stop = stop.copy()
                    modified_stop["stop_id"] = id
                    karlsrkrona.append(modified_stop)

        return pd.DataFrame(karlsrkrona, columns=list(self.df.columns)) #retunerar en ny dataframe med filtrerade resultat med samma columner som orginalet

    def remove_irrelevant_data(self, data):
        relevant_data = []
        with open(data, encoding="utf-8") as f:
            file = json.load(f)
        for index in file.values():
            relevant_data.append([index["stop_id"], index["stop_name"]])
        return pd.DataFrame(relevant_data, columns=["stop_id", "stop_name"])

    def is_in(self, lat, lon):
        set_a = (lon<16.09)&(lat>56)&(lat<56.528)&(lat<(0.742804*lon + 44.67389))
        set_b = (lat < (-0.850135*lon+69.33733))&(lat<(0.547745*lon+48.02817))&(lon<16.09)&(lat<56.528)&(lat>56) 
        # Gör 2 sets som innehåller området

        if set_a|set_b: #Kollar om det finns i någon av områdena
            return True
        else:
            return False

def main():
    dtamax = DataMaxer()
    goon1 = dtamax.remove_irrelevant_data("Karlskrona.json")
    #goon = dtamax.filter()
    #goon = goon.reset_index(drop=True)
    goon1.to_json(path_or_buf="karlskrona.json", orient="index")

main()