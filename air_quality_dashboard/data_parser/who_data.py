"""
Module containing WHOData class to load and update the WHO air quality data.
"""

import io
import os
import pandas as pd
import requests


DEFAULT_DATA_URL = r"https://cdn.who.int/media/docs/default-source/air-pollution-documents/air-quality-and-health/who_ambient_air_quality_database_version_2024_(v6.1).xlsx"


class WHOData:
    """
    Class to load and update the WHO air quality data.
    """

    def __init__(self, air_quality_data_url: str = DEFAULT_DATA_URL) -> None:
        self.air_quality_data_url = air_quality_data_url
        self.df = self.get_who_air_quality_data()
        self.calculate_statistics()

    def download_who_air_quality_data(self):
        """
        Downloads the WHO air quality data from the WHO website and saves it as a pickle file.

        Returns:
        pd.DataFrame: the WHO air quality data
        """
        for _attempt in range(3):
            if _attempt == 2:
                print("We tried to download the data 3 times, but failed.")
                raise SystemError("We tried to download the data 3 times, but failed.")
            try:
                air_quality_data = requests.get(self.air_quality_data_url, timeout=15)
                if air_quality_data.status_code == 200:
                    pd_air_quality_data = pd.read_excel(
                        io.BytesIO(air_quality_data.content), "Update 2024 (V6.1)"
                    )
            except requests.exceptions.Timeout:
                print("The request timed out, try again.")
                continue
            except requests.exceptions.TooManyRedirects:
                print("Too many redirects, try again.")
                continue
            except pd.errors.ParserError:
                print("The data file is corrupted, retry.")
                continue
            except Exception as e:
                print(
                    f"An error occured and we can't continue, as we don't have the WHO data: {e}"
                )
                ## stop the execution of the programm
                raise SystemError(e) from e
            else:
                break

        # set the correct datatypes
        pd_air_quality_data["who_ms"] = pd_air_quality_data["who_ms"].astype(bool)
        pd_air_quality_data["who_region"] = pd_air_quality_data["who_region"].astype(
            pd.CategoricalDtype()
        )
        pd_air_quality_data["iso3"] = pd_air_quality_data["iso3"].astype(str)
        pd_air_quality_data["city"] = pd_air_quality_data["city"].astype(str)
        pd_air_quality_data["country_name"] = pd_air_quality_data[
            "country_name"
        ].astype(str)
        pd_air_quality_data["version"] = pd_air_quality_data["version"].astype(str)
        pd_air_quality_data = pd_air_quality_data.dropna(
            subset=["year"]
        )  # cleanup rows with missing year, i.e. pointless data
        pd_air_quality_data["year"] = pd.to_datetime(
            pd_air_quality_data["year"], format="%Y"
        )
        pd_air_quality_data["year_int"] = pd_air_quality_data["year"].dt.strftime(
            "%Y"
        )  # have a year as integer for the data table
        pd_air_quality_data["year_int"] = pd_air_quality_data["year_int"].astype(float)
        # save the data
        pd_air_quality_data.to_pickle(
            os.path.join("data", "air_quality_data.xz"), compression="xz"
        )
        return pd_air_quality_data

    def load_who_air_quality_data(self):
        """
        Loads the WHO air quality data from the pickle file.

        Returns:
        pd.DataFrame: the WHO air quality data
        """
        return pd.read_pickle(os.path.join("data", "air_quality_data.xz"))

    def get_who_air_quality_data(self):
        """
        Downloads the WHO air quality data if it does not exist, \
            otherwise loads it from the pickle file.

        Returns:
        pd.DataFrame: the WHO air quality data
        """
        try:
            return self.load_who_air_quality_data()
        except FileNotFoundError:
            return self.download_who_air_quality_data()
        except pd.errors.EmptyDataError:
            print("The data file is empty, start from scratch.")
            return self.download_who_air_quality_data()
        except pd.errors.ParserError:
            print("The data file is corrupted, start from scratch.")
            return self.download_who_air_quality_data()

    def calculate_statistics(self):
        """
        Calculates some statistics for the WHO air quality data.

        Returns:
        None
        """
        self.years = self.df["year"].unique().tolist()
        self.years.sort()
        self.n_countries = self.df["country_name"].nunique()
