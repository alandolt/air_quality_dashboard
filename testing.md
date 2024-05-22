# Unit Testing
The coded ```unit_test.py``` allows to test the class LocalData. 
- The first two tests ```test_load_local_air_quality_data``` and ```test_update_local_air_quality_data``` test if after the execution of said functions, the resulting dataframe attribute in the the class is not ```None```, which would indicate an error in the loading process. 
```python 
def test_load_local_air_quality_data(self):
    localdata1 = LocalData()
    self.assertIsNotNone(localdata1.df)

def test_update_local_air_quality_data(self):
    localdata1 = LocalData()
    self.assertIsNotNone(localdata1.df)

```
- The next test function ```test_min_date``` tests if the calculation of the minimum date in the dataframe is correct. As the minimum date may change across executions (e.g. when not supplying a ```local_air_quality_data_Switzerland.xz``` file, a new one gets downloaded and hence the minimum date changes), we supply a custom local air quality dataset to compare against. Comparison for testing is then done by comparing the known minimum date of the custom dataset with the minimum date of the dataframe after loading the custom dataset and executing the ```min_date()``` function of the class.
```python
def test_min_date(self):
    localdata1 = LocalData()
    localdata1.df = pd.read_pickle(
        "data_for_unit_testing/local_air_quality_data_Switzerland.xz",
        compression="xz",
    )
    self.assertEqual(
        localdata1.min_date(),
        "2024-01-05 21:00",
        "Lowest data string should be 2024-01-05 21:00",
    )
```
- Last, we test the class initialisation method by supplying different combinations of valid/invalid parameters for the local data URL, as well as the local data file path. We then test, if the class initialisation raises the correct exceptions for invalid parameters, which is currently only implemented by a SystemExit assertion. Hence we test, if, when no correct parameters are supplied for the class, the program shuts down with a SystemExit exception.
```python
def test_init(self):
    # with this condition, we see if the programs exit, if no valid data source is supplied
    self.assertRaises(
        SystemExit,
        LocalData,
        "no_valid_url_supplied",
        "no_valid_local_data_pickle file",
    )
    # with this condition, we see if the programs exit, if no valid data source is supplied. Contrary to above,
    # we should get a Timeout error (but stillw with a SystemExit)
    self.assertRaises(
        SystemExit,
        LocalData,
        "http://www.no_valid_url_supplied.com",
        "no_valid_local_data_pickle file",
    )
    # valid data source is supplied, but no valid url for updating. The program should exit
    self.assertRaises(SystemExit, LocalData, "no_valid_url_supplied", "Switzerland")
```
