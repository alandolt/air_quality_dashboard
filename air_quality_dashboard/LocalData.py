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
        self.load_local_air_quality_data()

    def load_local_air_quality_data(self):
        """
        Loads the local air quality data from the pickle file
        """

        try:
            if os.path.exists(self.data_location):
                self.df = pd.read_pickle(self.data_location)
            else:
                self.df = None

            self.update_local_air_quality_data()
        except Exception as e:
            print(f"Failed to load air quality data: {e}")

    def update_local_air_quality_data(self):
        """
        Updates the local air quality data from the local website
        (NABEL database with Swiss air quality data in real-time),
        the data is updated hourly on the website, but there is no archive,
        so we create our own here by saving the data in a pickle file.
        """
        # get the local website
        local_website = requests.get(self.air_quality_data_url)

        # makes everything readable
        url_soup = BeautifulSoup(local_website.content, "html.parser")

        # finds table for dataframe
        url_table = url_soup.find("table")

        # creates dataframe with string values
        df = pd.read_html(io.StringIO(url_table.prettify()))[0]

        # rename columns to not have
        df = df.rename(
            columns={
                "O₃": "O3",
                "O₃max": "O3max",
                "NO₂": "NO2",
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

        # convert type of site to category
        df["Type of site"] = df["Type of site"].astype("category")

        date = url_table.find("caption").get_text(strip=True)
        date = pd.to_datetime(date.lstrip("Date from: "))
        df["timestamp"] = date

        df = df.loc[
            df["Type of site"] != "Ambient air quality standard [µg/m³]"
        ]  # remove the critical values

        # if no previous data exist, save the new data directly in the class,
        # otherwise append the new data to the existing data, but first check if the
        # data is not already in the dataframe by checking if the timestamp already
        # exists in the dataframe
        if self.df is None:
            self.df = df
        else:
            if date not in self.df["timestamp"].unique():
                self.df = pd.concat([self.df, df])

        self.df.to_pickle(self.data_location, compression="xz")

    def min_date(self, format="%Y-%m-%d %H:%M") -> str:
        """
        Returns the first timestamp of the stored data (from the pickle file)
        """
        return self.df["timestamp"].min().strftime(format)

    def max_date(self, format="%Y-%m-%d %H:%M") -> str:
        """
        Returns the last timestamp of the stored data (from the pickle file)
        """
        return self.df["timestamp"].max().strftime(format)

    def caclulate_mean_per_site(self) -> pd.DataFrame:
        """
        Calculates the mean values of the air quality data per site
        """
        return self.df.groupby("Type of site").mean(
            ["O3", "O3max", "NO2", "NOX", "SO2", "PM10", "SO2"]
        )
