# Changes to reformat code

## 0.0.2
- Reorder air_quality_dashboard module by moving `local_data.py` and `who_data.py` module in a parser submodule. 
- Moving code for data table filtering into ```module folder -> dashboard -> helper_funcitons.py```, so that they can be reused. 
- ~~ Move code for dashboard to a separate module dashboard subfolder in the air_quality_dashboard package.~~ 
- ~~ Divide the code for the dashboards into separate modules for each dashboard page.~~ 
- ~~ Hence make the code more modular so that all required code is in the air_quality_dashboard package and the main.py only serves as an entry point to the application.~~ 
- With Dash it seems not to be possible to either have the code in a separate module or even class, as the call-back function requires access to the Dash app object, which can't be passed as an argument to the call-back function. Neither can self be passed efficiently to the call-back function itself, as the call-back function is called by Dash and not by the user (good old static function attribute seems not to work).
- Hence, we divided the code into pages, as supported by dash. Each page is then loaded automatically in the main.py file. However this solutions requires the loading of the dataframe in each subpage which is not 100% efficient. 
- There is a solution to this problem, using a dash storage object, which stores the data via JSON in the browser, however, this does not work for large dataframes. 
- Hence, no further changes, except the subdivision into pages were made. 
- In the next revision, we may try to dissolve the currently used air quality dashboard module and instead integrate the code more directly in the current dash structure using ```pages``` and ```assets``` subfolders, so that instead of having a module with a central entry point (main.py), a compact dash folder structure, which in its entirety is required to run the dashboard, will be created. 