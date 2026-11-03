
import pandas as pd
class DataMaxer:

    def __init__(self):
        self.df = pd.read_csv("stops.csv",encoding="utf-8")

    def filter(self):
        karlsrkrona = [] #lista att lägga filterade resultat
        
        for index, stop in self.df.iterrows():  #itererar över alla stop inlaggda i dataset
            result = self.is_in(stop["stop_lat"], stop["stop_lon"]) ##kallar is in funktionens
            if result == True: 
                karlsrkrona.append(stop)

        return pd.DataFrame(karlsrkrona, columns=list(self.df.columns)) #retunerar en ny dataframe med filtrerade resultat med samma columner som orginalet

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
    goon = dtamax.filter()
    goon.to_csv("stop_karlskrona.csv", encoding="utf-8")

main()