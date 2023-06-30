import pandas as pd
from entity import Entity
class Map:
    def __init__(self):
        pass

    def load_map(self):
        df = pd.read_csv("map.csv")
        obj_list  = []
        for x, y, lx, ly, r, g, b in zip(df["x"], df["y"],df["lx"],df["ly"],df["r"],df["g"],df["b"]):
            obj_list.append(Entity(x, y, lx, ly, (r, g, b), "pic.jpg", False))
        return obj_list
    
    def map_from_list(self, map_list):
        return map_list
