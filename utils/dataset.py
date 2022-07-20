from dataclasses import dataclass
import pandas as pd
import numpy as np
from pydantic import validate_arguments

@validate_arguments
@dataclass
class Air_Quality_Metadata:
    country: str
    city: str
    city_ascii: str
    region: str
    region_ascii: str
    population: int
    latitude: float
    longitude: float
    time_zone: str

@validate_arguments
@dataclass
class Air_Quality:
    year: int
    month: int
    day: int
    utc_hr: int
    pm25: float
    pm10mask: float
    retrospective: int

metadata_parser = {
    "Country": "country",
    "City": "city",
    "City (ASCII)": "city_ascii",
    "Region": "region",
    "Region (ASCII)": "region_ascii",
    "Population": "population",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Time Zone": "time_zone"
}


class Air_Quality_Dataset():
    def __init__(self, filename: str):
        self.fp = filename
        self.get_air_quality()
    
    def get_air_quality(self):
        metadata = True
        metadata_dict = {}
        dataarray = []
        with open(self.fp, 'r', encoding='utf-8') as f:
            data = f.readlines()
            for line in data:
                line = line.replace("\n", "")
                line = line.replace("\t", " ")
                if ":" not in line and metadata:
                    metadata = False
                    continue
                if metadata:
                    key, value = line.split(": ")
                    key = metadata_parser[key[2:]]
                    metadata_dict[key] = value
                else:
                    air_quality = Air_Quality(*line.split(" "))
                    dataarray.append(air_quality)


        self.metadata = Air_Quality_Metadata(**metadata_dict)
        self.data = pd.DataFrame(dataarray)

