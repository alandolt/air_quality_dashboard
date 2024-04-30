# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 18:14:51 2024

@author: yelts
"""
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import io
import os


local_default_data_url = r"https://www.bafu.admin.ch/bafu/en/home/topics/air/state/data/air-pollution--real-time-data/table-of-the-current-situation-nabel.html"

class LocalData():
    
    def __init__(self, air_quality_data_url:str = local_default_data_url) -> None:
        self.air_quality_data_url = air_quality_data_url
        self.df = self.get_local_air_quality_data()
        self.mean_sites = self.calculate_statistics()
        
    def get_local_air_quality_data(self):
        
        #get the local website
        local_website = requests.get(self.air_quality_data_url)
        
        #makes everything readable
        url_soup = BeautifulSoup(local_website.content, "html.parser")
        
        #finds table for dataframe
        url_table = url_soup.find("table")
        
        #creates dataframe with string values
        df = pd.read_html(str(url_table))[0]
        
        return df

        
    def calculate_statistics(self):
        
        #calculate mean value for each substance in function of the site
        mean_sites = self.df.groupby("Type of site").mean([["O₃", "O₃max", "NO₂", "NOₓ", "PM10"]])
        
        #calculate max value for each substance for the corresponding city
        #TODO
        return mean_sites
        
        
        
        
local_data = LocalData()

mean_sites = local_data.mean_sites