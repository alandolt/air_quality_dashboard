"""
Module containing the LocalData class to load and update the 
local air quality data from the Swiss NABEL database.
"""

import io
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup


LOCAL_DEFAULT_DATA_URL = r"https://www.bafu.admin.ch/bafu/en/home/topics/air/state/data/air-pollution--real-time-data/table-of-the-current-situation-nabel.html"


class LocalData:
    """
    Class to load and update the local air quality data from the Swiss NABEL database.
    """

    def __init__(
        self,
        air_quality_data_url: str = LOCAL_DEFAULT_DATA_URL,
        data_source_name: str = "Switzerland",
    ) -> None:
        """
        Initializes the LocalData class with the air quality data URL and the data source name.

        Args:
        air_quality_data_url (str): the URL of the air quality data
        data_source_name (str): the name of the data source
        """
        self.air_quality_data_url = air_quality_data_url
        self.data_source_name = data_source_name
        self.df = None
        self.data_location = os.path.join(
            "data", f"local_air_quality_data_{data_source_name}.xz"
        )
        self.load_local_air_quality_data()

    def load_local_air_quality_data(self):
        """
        Loads the local air quality data from the pickle file
        """

        try:
            self.df = pd.read_pickle(self.data_location)
        except FileNotFoundError:
            print("The data file does not exist, create a new data file.")
            self.df = None
        except pd.errors.EmptyDataError:
            print("The data file is empty, start from scratch.")
            self.df = None
        except pd.errors.ParserError:
            print("The data file is corrupted, start from scratch.")
            self.df = None
        finally:
            try:
                self.update_local_air_quality_data()
            except requests.exceptions.Timeout as e:
                print("Request timed out, maybe you're blocked from the site")
                raise SystemExit(e) from e  # stop the execution of the program
            except requests.exceptions.TooManyRedirects as e:
                print("Too many redirects, is the URL correct?")
                raise SystemExit(e) from e  # stop the execution of the program
            except requests.exceptions.RequestException as e:
                print(f"Something went really wrong: {e}")
                raise SystemExit(e) from e  # stop the execution of the program
            except pd.errors.ParserError as e:
                print(f"Something went wrong with the data source: {e}")
                raise SystemExit(e) from e
            except KeyError as e:
                print(f"Something went wrong with the data source: {e}")
                raise SystemExit(e) from e

    def update_local_air_quality_data(self):
        """
        Updates the local air quality data from the local website
        (NABEL database with Swiss air quality data in real-time),
        the data is updated hourly on the website, but there is no archive,
        so we create our own here by saving the data in a pickle file.
        """
        # get the local website
        local_website = requests.get(self.air_quality_data_url, timeout=5)

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
        date = pd.to_datetime(date.lstrip("Date from: "), dayfirst=True)
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

    def min_date(self, timeformat="%Y-%m-%d %H:%M") -> str:
        """
        Returns the first timestamp of the stored data (from the pickle file)
        """
        return self.df["timestamp"].min().strftime(timeformat)

    def max_date(self, timeformat="%Y-%m-%d %H:%M") -> str:
        """
        Returns the last timestamp of the stored data (from the pickle file)
        """
        return self.df["timestamp"].max().strftime(timeformat)

    def caclulate_mean_per_site(self) -> pd.DataFrame:
        """
        Calculates the mean values of the air quality data per site
        """
        return self.df.groupby("Type of site").mean(
            ["O3", "O3max", "NO2", "NOX", "SO2", "PM10", "SO2"]
        )
