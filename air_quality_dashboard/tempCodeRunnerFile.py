import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import io
import os


local_default_data_url = r"https://www.bafu.admin.ch/bafu/en/home/topics/air/state/data/air-pollution--real-time-data/table-of-the-current-situation-nabel.html"


class LocalData:

    def __init__(
        self,
        air_quality_data_url: str = local_default_data_url,
        data_source_name: str = "Switzerland",
    ) -> None:
        self.air_quality_data_url = air_quality_data_url
        self.data_source_name = data_source_name
        self.data_location = os.path.join(
            "data", f"local_air_quality_data_{data_source_name}.xz"
        )
        self.df = None
        self.load_local_air_quality_data()
        self.mean_sites = self.calculate_statistics()

    def load_local_air_quality_data(self):
        """
        Loads the local air quality data from the pickle file
        """

        data_location = os.path.join("data", "local_air_quality_data_switzerland.xz")
        try:
            if os.path.exists(data_location):
                self.df = pd.read_pickle(data_location)
            else:
                self.update_local_air_quality_data()
        except Exception as e:
            print(f"Failed to load local air quality data: {e}")

    def update_local_air_quality_data(self):
        """
        Updates the local air quality data from the local website
        """

        # check if the file exists
        data_location = os.path.join("data", "local_air_quality_data_switzerland.xz")

        os.path.exists(os.path.join())

        # get the local website
        local_website = requests.get(self.air_quality_data_url)

        # makes everything readable
        url_soup = BeautifulSoup(local_website.content, "html.parser")

        # finds table for dataframe
        url_table = url_soup.find("table")

        # creates dataframe with string values
        df = pd.read_html(io.StringIO(url_table.prettify()))

        # rename columns to not have
        df = df.rename(
            columns={
                "O₃": "O3",
                "O₃max": "O3max",
                "NO₂": "No2",
                "NOₓ": "NOX",
                "SO₂": "SO2",
            }
        )

        # convert the entries to float / NAN
        df["O3"] = df["O3"].apply(pd.to_numeric, errors="coerce")
        df["O3max"] = df["O3max"].apply(pd.to_numeric, errors="coerce")
        df["NO2"] = df["NO2"].apply(pd.to_numeric, errors="coerce")
        df["NOX"] = df["NOX"].apply(pd.to_numeric, errors="coerce")
        df["SO2"] = df["SO2"].apply(pd.to_numeric, errors="coerce")

        date = url_table.find("caption").get_text(strips="True")
        date = pd.to_datetime(date.lstrip("Date from: "))
        df["timestamp"] = date

        # if no previous data exist, save the new data directly in the class,
        # otherwise append the new data to the existing data
        if self.df is None:
            self.df = df
        else:
            self.df = pd.concat(self.df, df)

        self.df.to_pickle(data_location, compression="xz")

    def calculate_statistics(self):

        # calculate mean value for each substance in function of the site
        mean_sites = self.df.groupby("Type of site").mean(
            [["O₃", "O₃max", "NO₂", "NOₓ", "PM10"]]
        )

        # calculate max value for each substance for the corresponding city
        # TODO
        return mean_sites

