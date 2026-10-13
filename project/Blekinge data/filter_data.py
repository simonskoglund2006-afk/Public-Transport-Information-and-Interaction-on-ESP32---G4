
class DataMaxer:
    import numpy as np
    import json as js
    import pandas as pd

    def __init__(self):
        self.df = self.pd.read_csv("stops.csv")

    def filter(self):
        karlsrkona = self.pd.DataFrame(columns=list(self.df.columns))
        
        for lat,lon in self.df.loc[["stop_lat", "stop_lon"]]:
            result = self.is_in(lat, lon)
            if result == True:
                karlsrkrona


    def is_in(self, lat, lon):
        set_a = (lon<16.09)&(lat>56)&(lat<56.528)&(lat<(0.742804*lon + 44.67389))
        set_b = (lat < (-0.850135*lon+69.33733))&(lat<(0.547745*lon+48.02817))&(lon<16.09)&(lat<56.528)&(lat>56) 

        if set_a|set_b:
            return True
        else:
            return False        
        


#x_data = get_lat("sigma")

#x < 16.09
#y > -0.850135*x + 69.33733
#set_a = {y>56, y<56.528, y<0.742804*x+44.67389}
#set_b = {y<0.547745*x+48.02817, x<16.09, y<56.528, y>56}

print(df.to_string())