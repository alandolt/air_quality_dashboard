# Linting for local_data.py

## Output of Pylint for LocalData.py
```text
************* Module air_quality_dashboard.LocalData
LocalData.py:8:0: C0301: Line too long (160/100) (line-too-long)
LocalData.py:1:0: C0114: Missing module docstring (missing-module-docstring)
LocalData.py:1:0: C0103: Module name "LocalData" doesn't conform to snake_case naming style (invalid-name)
LocalData.py:8:0: C0103: Constant name "local_default_data_url" doesn't conform to UPPER_CASE naming style (invalid-name)
LocalData.py:11:0: C0115: Missing class docstring (missing-class-docstring)
LocalData.py:37:15: W0718: Catching too general exception Exception (broad-exception-caught)
LocalData.py:48:24: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
LocalData.py:93:12: W0201: Attribute 'df' defined outside __init__ (attribute-defined-outside-init)
LocalData.py:96:16: W0201: Attribute 'df' defined outside __init__ (attribute-defined-outside-init)
LocalData.py:4:0: C0411: standard import "io" should be placed before third party imports "pandas", "requests", "bs4.BeautifulSoup" (wrong-import-order)
LocalData.py:5:0: C0411: standard import "os" should be placed before third party imports "pandas", "requests", "bs4.BeautifulSoup" (wrong-import-order)

-----------------------------------
Your code has been rated at 7.66/10
```

## Explanation of Pylint Output and applied changes

### LocalData.py:8:0: C0301: Line too long (160/100) (line-too-long)
Can't really be changed as this line contains an URL which is longer than 100 characters.

### LocalData.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Adding a module docstring.

```python
"""
Module containing the LocalData class to load and update the local air quality data from the Swiss NABEL database.
"""
```

### LocalData.py:1:0: C0103: Module name "LocalData" doesn't conform to snake_case naming style (invalid-name)
Changed filename to local_data.py.

### LocalData.py:8:0: C0103: Constant name "local_default_data_url" doesn't conform to UPPER_CASE naming style (invalid-name)
Changed variable name to LOCAL_DEFAULT_DATA_URL.

### LocalData.py:11:0: C0115: Missing class docstring (missing-class-docstring)
Adding a class docstring. 

```python
"""
Class to load and update the local air quality data from the Swiss NABEL database.
"""
```

### LocalData.py:37:15: W0718: Catching too general exception Exception (broad-exception-caught)
Yes, a more specific exception should be caught. However, as we are dealing with a web request, it is not clear what exceptions can be raised. Therefore, we will keep the general exception for now.

### LocalData.py:48:24: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
Adding a timeout time of 5s
```python
local_website = requests.get(self.air_quality_data_url, timeout=5)
```

### LocalData.py:93:12: W0201: Attribute 'df' defined outside __init__ (attribute-defined-outside-init)
Adding a ```python self.df = None ```  to the class attributes.


### LocalData.py:4:0: C0411: standard import "io" should be placed before third party imports "pandas", "requests", "bs4.BeautifulSoup" (wrong-import-order)

Change order of imports to 
```python
import io
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
```

## Output after changes
```text
************* Module air_quality_dashboard.local_data
local_data.py:12:0: C0301: Line too long (160/100) (line-too-long)
local_data.py:51:15: W0718: Catching too general exception Exception (broad-exception-caught)

------------------------------------------------------------------
Your code has been rated at 9.58/10 (previous run: 9.38/10, +0.21)
```

# Linting for WHOData.py

## Output of Pylint for WHOData.py
```text
************* Module air_quality_dashboard.WHOData
WHOData.py:6:0: C0301: Line too long (172/100) (line-too-long)
WHOData.py:72:0: C0301: Line too long (105/100) (line-too-long)
WHOData.py:1:0: C0114: Missing module docstring (missing-module-docstring)
WHOData.py:1:0: C0103: Module name "WHOData" doesn't conform to snake_case naming style (invalid-name)
WHOData.py:9:0: C0115: Missing class docstring (missing-class-docstring)
WHOData.py:23:27: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
WHOData.py:32:12: W0719: Raising too general exception: Exception (broad-exception-raised)
WHOData.py:82:4: C0116: Missing function or method docstring (missing-function-docstring)
WHOData.py:3:0: C0411: standard import "io" should be placed before third party imports "pandas", "requests" (wrong-import-order)
WHOData.py:4:0: C0411: standard import "os" should be placed before third party imports "pandas", "requests" (wrong-import-order)

-----------------------------------
Your code has been rated at 7.44/10
```

## Explanation of Pylint Output and applied changes
### WHOData.py:6:0: C0301: Line too long (172/100) (line-too-long)
Can't be changed, as URL

### WHOData.py:72:0: C0301: Line too long (105/100) (line-too-long)
Line splited. 

### WHOData.py:1:0: C0114: Missing module docstring (missing-module-docstring)
Adding a module docstring.

```python
"""
Module containing WHOData class to load and update the WHO air quality data.
"""
```

### WHOData.py:1:0: C0103: Module name "WHOData" doesn't conform to snake_case naming style (invalid-name)
Changed filename to who_data.py.

### WHOData.py:9:0: C0115: Missing class docstring (missing-class-docstring)
Adding a class docstring. 

```python
"""
Class to load and update the WHO air quality data.
"""
```

### WHOData.py:23:27: W3101: Missing timeout argument for method 'requests.get' can cause your program to hang indefinitely (missing-timeout)
Adding a timeout time of 15s
```python
air_quality_data = requests.get(self.air_quality_data_url, timeout=15)
```

### WHOData.py:32:12: W0719: Raising too general exception: Exception (broad-exception-raised)
Yes, a more specific exception should be raised. However, as we are dealing with a web request, it is not clear what exceptions can be raised. Therefore, we will keep the general exception for now.

### WHOData.py:82:4: C0116: Missing function or method docstring (missing-function-docstring)
Adding a docstring. 

```python
"""
Calculates some statistics for the WHO air quality data.

Returns:
None
"""
```

### WHOData.py:3:0: C0411: standard import "io" should be placed before third party imports "pandas", "requests" (wrong-import-order)
Change order of imports to 
```python
import io
import os
import pandas as pd
import requests
```

## Output after changes
```text
************* Module air_quality_dashboard.who_data
who_data.py:10:0: C0301: Line too long (172/100) (line-too-long)
who_data.py:38:12: W0719: Raising too general exception: Exception (broad-exception-raised)

-----------------------------------
Your code has been rated at 9.49/10
```