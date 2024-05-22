# Implementation of try-except block

## Implementation in class LocalData, method load_local_air_quality_data
```python
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
        except requests.exceptions.Timeout:
            print("Request timed out, maybe you're blocked from the site or your internet connection is slow.")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects, is the URL correct?")
        except requests.exceptions.RequestException as e:
            print(f"Something went really wrong: {e}")
            raise SystemExit(e) from e  # stop the execution of the program
        except pd.errors.ParserError as e:
            print(f"Something went wrong with the data source: {e}")
            raise SystemExit(e) from e
        except KeyError as e:
            print(f"Something went wrong with the data source: {e}")
            raise SystemExit(e) from e
```

Reasoning: 
- This function loads the local air quality data either from a pickle file, or if said file does not exist, it sets the dataframe attribute to None, so that in the subsequent function call ```update_local_air_quality_data()```, the data gets redownloaded from scratch, without trying to update the previous file. 
- Hence, the first exception block catches the FileNotFoundError, EmptyDataError, and ParserError, which are the most likely errors to occur when trying to read the pickle file.
- The second try-except block is nested in the finally block, as it is crucial to update the data, no matter if the data was loaded from the pickle file or not. If no data is previously loaded, we will simply get the most recent data. 
- Again, we set this into a try-except block, as the function ```update_local_air_quality_data()``` makes a request to the internet, and hence, we need to catch the most likely errors that can occur when making a request.
- The timeout exception is the most likely to occur, as the request to the internet can take a long time, and hence, we catch this exception first. A timeout can occur if the internet connection is slow, or if the server is slow to respond.
- A too many redirects exception can occur if the URL is incorrect, and hence, we catch this exception next.
- The next exception is a general exception, which catches all other exceptions that can occur when making a request. We print the error message and raise a SystemExit exception, which stops the execution of the program.
- Regarding the case when the data source could have been downloaded but may be corrupted, we check if there is a parser error or a key error, which can occur if the data source is not in the expected format. We print the error message and raise a SystemExit exception, which stops the execution of the program.

## Implementation in class WhoData, method get_who_air_quality_data
```python
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
```

Same reasoning as above, but without nested try-except blocks, as the function either loads the data from the pickle file or downloads it from the internet. The function ```download_who_air_quality_data()``` is called if the data file does not exist, is empty, or corrupted, and has its own try-except block to catch the most likely errors that can occur when making a request.

```python
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
```
Same pattern structure as above for the try-except block, but with a for loop to try to download the data three times, before raising a SystemError exception, which stops the execution of the program.
