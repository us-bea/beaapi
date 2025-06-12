# beaapi
  `beaapi`: A Python library library to make it easier to retrieve and work with BEA data. For the parallel R-package, see [bea.R](https://github.com/us-bea/bea.R/).

To install the package, use `pip install beaapi`.

For help, see our [documentation](https://us-bea.github.io/beaapi/).

For development and building information, see [CONTRIBUTING.md](https://github.com/us-bea/beaapi/blob/main/CONTRIBUTING.md).

## To Get Started
Once you have installed the package, you can load it in your Python script as follows:


```python
import beaapi
```

To use the package, you must first  [register for an API key](https://apps.bea.gov/api/signup/) from BEA by providing your name and email address. The key will be emailed to you. 

Once you have received your BEA API key, you can save it to a variable to make it easier to use later: 


```python
beakey = 'YOUR 36-DIGIT API KEY'
```

For scripts, an even better method is to create an unversioned text file called `.env` with the contents `beakey=Your36DigitAPiKey` and then use the package `python-dotenv` to load it automatically.


```python
from dotenv import dotenv_values
beakey = dotenv_values()["beakey"]
```

## Get metadata
The BEA data is distributed across various datasets that each contain many tables. To get a list of the datasets available on the API, use `get_data_set_list()`:


```python
list_of_sets = beaapi.get_data_set_list(beakey)
display(list_of_sets)  # Note the last dataset is only for speeding up metadata queries
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DatasetName</th>
      <th>DatasetDescription</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NIPA</td>
      <td>Standard NIPA tables</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NIUnderlyingDetail</td>
      <td>Standard NI underlying detail tables</td>
    </tr>
    <tr>
      <th>2</th>
      <td>MNE</td>
      <td>Multinational Enterprises</td>
    </tr>
    <tr>
      <th>3</th>
      <td>FixedAssets</td>
      <td>Standard Fixed Assets tables</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ITA</td>
      <td>International Transactions Accounts</td>
    </tr>
    <tr>
      <th>5</th>
      <td>IIP</td>
      <td>International Investment Position</td>
    </tr>
    <tr>
      <th>6</th>
      <td>InputOutput</td>
      <td>Input-Output Data</td>
    </tr>
    <tr>
      <th>7</th>
      <td>IntlServTrade</td>
      <td>International Services Trade</td>
    </tr>
    <tr>
      <th>8</th>
      <td>IntlServSTA</td>
      <td>International Services Supplied Through Affili...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>GDPbyIndustry</td>
      <td>GDP by Industry</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Regional</td>
      <td>Regional data sets</td>
    </tr>
    <tr>
      <th>11</th>
      <td>UnderlyingGDPbyIndustry</td>
      <td>Underlying GDP by Industry</td>
    </tr>
    <tr>
      <th>12</th>
      <td>APIDatasetMetaData</td>
      <td>Metadata about other API datasets</td>
    </tr>
  </tbody>
</table>
</div>


Queries to the different datasets take different parameters. To get a list of the paramaters for a given dataset, use `get_parameter_list()`; for example, to get a list of the parameters for the NIPA dataset, use:


```python
list_of_params = beaapi.get_parameter_list(beakey, 'NIPA')
display(list_of_params)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ParameterName</th>
      <th>ParameterDataType</th>
      <th>ParameterDescription</th>
      <th>ParameterIsRequiredFlag</th>
      <th>ParameterDefaultValue</th>
      <th>MultipleAcceptedFlag</th>
      <th>AllValue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Frequency</td>
      <td>string</td>
      <td>A - Annual, Q-Quarterly, M-Monthly</td>
      <td>1</td>
      <td></td>
      <td>1</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>ShowMillions</td>
      <td>string</td>
      <td>A flag indicating that million-dollar data sho...</td>
      <td>0</td>
      <td>N</td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>TableID</td>
      <td>integer</td>
      <td>The standard NIPA table identifier</td>
      <td>0</td>
      <td>&lt;NA&gt;</td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>TableName</td>
      <td>string</td>
      <td>The new NIPA table identifier</td>
      <td>0</td>
      <td>&lt;NA&gt;</td>
      <td>0</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>Year</td>
      <td>integer</td>
      <td>List of year(s) of data to retrieve (X for All)</td>
      <td>1</td>
      <td></td>
      <td>1</td>
      <td>X</td>
    </tr>
  </tbody>
</table>
</div>


To get a list of the values for a given parameter, use `get_parameter_values()`; for example, to get a list of the parameter values for the Frequency parameter of the NIPA dataset, use:


```python
list_of_param_vals = beaapi.get_parameter_values(beakey, 'NIPA', 'Frequency')
display(list_of_param_vals)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>FrequencyID</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>Annual</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Q</td>
      <td>Quarterly</td>
    </tr>
    <tr>
      <th>2</th>
      <td>M</td>
      <td>Monthly</td>
    </tr>
  </tbody>
</table>
</div>


The [API documentation](https://apps.bea.gov/API/docs/index.htm) is a good place to also understand allowed values.

A few datasets (ITA, IIP, InputOutput, IntlServTrade, GDPbyIndustry, Regional, and UnderlyingGDPbyIndustry) allow you to filter the values based on what will be passed in for other parameters.


```python
tbl = beaapi.get_parameter_values_filtered(beakey, 'ITA', targetparameter='Indicator', AreaOrCountry="China",Frequency="A", Year="2011")
display(tbl.head())
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Key</th>
      <th>Desc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BalCapAcct</td>
      <td>Balance on capital account</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BalCurrAcct</td>
      <td>Balance on current account</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BalGds</td>
      <td>Balance on goods</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BalGdsServ</td>
      <td>Balance on goods and services</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BalPrimInc</td>
      <td>Balance on primary income</td>
    </tr>
  </tbody>
</table>
</div>


A few of the datasets publish metadata tables that can be queried for particular strings using `search_metadata()`. This method allows you to search for BEA data by keyword. For example, to find all datasets in which the term "personal consumption" appears, use the following:  


```python
search_data = beaapi.search_metadata('Gross domestic', beakey)
search_data.head(2)
```

    Created directory: beaapi_data
    Creating first-time local copy of metadata for all datasets - only done once in working directory.
    Datasets will be updated only if timestamps indicate metadata obsolete in future searches, and only obsolete metadata sets will be updated.
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SeriesCode</th>
      <th>RowNumber</th>
      <th>LineDescription</th>
      <th>LineNumber</th>
      <th>ParentLineNumber</th>
      <th>Tier</th>
      <th>Path</th>
      <th>TableId</th>
      <th>Datasetname</th>
      <th>TableName</th>
      <th>ReleaseDate</th>
      <th>NextReleaseDate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A191RL</td>
      <td>10</td>
      <td>Gross domestic product</td>
      <td>1</td>
      <td></td>
      <td>0</td>
      <td>1</td>
      <td>T10101</td>
      <td>NIPA</td>
      <td>Table 1.1.1. Percent Change From Preceding Per...</td>
      <td>Feb 28 2019  8:30AM</td>
      <td>Mar 28 2019  8:30AM</td>
    </tr>
    <tr>
      <th>26</th>
      <td>A191RP</td>
      <td>280</td>
      <td>Gross domestic product, current dollars</td>
      <td>27</td>
      <td></td>
      <td>0</td>
      <td>27</td>
      <td>T10101</td>
      <td>NIPA</td>
      <td>Table 1.1.1. Percent Change From Preceding Per...</td>
      <td>Feb 28 2019  8:30AM</td>
      <td>Mar 28 2019  8:30AM</td>
    </tr>
  </tbody>
</table>
</div>



Please note that that search_metadata currently searches only national data.

The contents of this function are automatically updated using a new metadata component of BEA's API; as such, we recommend that you use it with your API key, and the first use of this function requires that you use your key or it will be unable to extract the metadata.

If you do not wish to automatically update the metadata (e.g., you have conducted a study using the search function), simply searching for the term without also passing your key to the function will do a search only using your locally stored version.


## Get data 


Once you have identified the TableId number and other information, you can use `get_data()` to access the data. The following code, for example, returns the NIPA table with 2015 data for Table T20305. 


```python
bea_tbl = beaapi.get_data(beakey, datasetname='NIPA', TableName='T20305', Frequency='Q', Year='2015')
display(bea_tbl.head(2))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TableName</th>
      <th>SeriesCode</th>
      <th>LineNumber</th>
      <th>LineDescription</th>
      <th>TimePeriod</th>
      <th>METRIC_NAME</th>
      <th>CL_UNIT</th>
      <th>UNIT_MULT</th>
      <th>DataValue</th>
      <th>NoteRef</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T20305</td>
      <td>DPCERC</td>
      <td>1</td>
      <td>Personal consumption expenditures (PCE)</td>
      <td>2015Q1</td>
      <td>Current Dollars</td>
      <td>Level</td>
      <td>6</td>
      <td>12119763</td>
      <td>T20305</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T20305</td>
      <td>DPCERC</td>
      <td>1</td>
      <td>Personal consumption expenditures (PCE)</td>
      <td>2015Q2</td>
      <td>Current Dollars</td>
      <td>Level</td>
      <td>6</td>
      <td>12264140</td>
      <td>T20305</td>
    </tr>
  </tbody>
</table>
</div>


We store in the meta-data the index columns so that you can create a unique index on the data-frame.


```python
display(bea_tbl.set_index(bea_tbl.attrs['index_cols']).head(2))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>TableName</th>
      <th>SeriesCode</th>
      <th>LineDescription</th>
      <th>METRIC_NAME</th>
      <th>CL_UNIT</th>
      <th>UNIT_MULT</th>
      <th>DataValue</th>
      <th>NoteRef</th>
    </tr>
    <tr>
      <th>LineNumber</th>
      <th>TimePeriod</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">1</th>
      <th>2015Q1</th>
      <td>T20305</td>
      <td>DPCERC</td>
      <td>Personal consumption expenditures (PCE)</td>
      <td>Current Dollars</td>
      <td>Level</td>
      <td>6</td>
      <td>12119763</td>
      <td>T20305</td>
    </tr>
    <tr>
      <th>2015Q2</th>
      <td>T20305</td>
      <td>DPCERC</td>
      <td>Personal consumption expenditures (PCE)</td>
      <td>Current Dollars</td>
      <td>Level</td>
      <td>6</td>
      <td>12264140</td>
      <td>T20305</td>
    </tr>
  </tbody>
</table>
</div>


Extra meta-data from the API is returned in a dictionary in the attributes called `detail` and can vary based on the dataset.


```python
print('Extra detail keys:' + str(bea_tbl.attrs['detail'].keys()))
print("Let's look at some interesting ones.")
print('Statistic: ' + bea_tbl.attrs['detail']['Statistic'])
print('UTCProductionTime (to know the vintage): ' + bea_tbl.attrs['detail']['UTCProductionTime'])  # some datasets use 'TsLastUpdated'
print("Notes corresponding to NoteRef:")
display(bea_tbl.attrs['detail']['Notes'].head())
```

    Extra detail keys:dict_keys(['Statistic', 'UTCProductionTime', 'Dimensions', 'Notes'])
    Let's look at some interesting ones.
    Statistic: NIPA Table
    UTCProductionTime (to know the vintage): 2024-03-28T13:07:19.130
    Notes corresponding to NoteRef:
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NoteRef</th>
      <th>NoteText</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>T20305</td>
      <td>Table 2.3.5. Personal Consumption Expenditures...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>T20305.1</td>
      <td>1. Net expenses of NPISHs, defined as their gr...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>T20305.2</td>
      <td>2. Gross output is net of unrelated sales, sec...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T20305.3</td>
      <td>3. Excludes unrelated sales, secondary sales, ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>T20305.4</td>
      <td>4. Food consists of food and beverages purchas...</td>
    </tr>
  </tbody>
</table>
</div>


To retrieve a limited selection of multiple years, list all the years you want to retrieve. For example, to retrieve data for 2011-2015, use `Year="2011,2012,2013,2014,2015"`

The  [API documentation](http://www.bea.gov/API/bea_web_service_api_user_guide.htm) includes information about the specific parameters required by `get_data()`. 

If you would like to format the data in a wide format so that different variables (in this case LineNumbers) are different rows, you can use `to_wide_vars_to_cols()`.


```python
display(beaapi.to_wide_vars_in_cols(bea_tbl).head(3))
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>LineNumber</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>10</th>
      <th>...</th>
      <th>22</th>
      <th>23</th>
      <th>24</th>
      <th>25</th>
      <th>26</th>
      <th>27</th>
      <th>28</th>
      <th>29</th>
      <th>30</th>
      <th>31</th>
    </tr>
    <tr>
      <th>TimePeriod</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2015Q1</th>
      <td>12119763</td>
      <td>3896791</td>
      <td>1291044</td>
      <td>478782</td>
      <td>284726</td>
      <td>335481</td>
      <td>192055</td>
      <td>2605746</td>
      <td>935572</td>
      <td>376595</td>
      <td>...</td>
      <td>352308</td>
      <td>1360579</td>
      <td>1008271</td>
      <td>10625316</td>
      <td>8771780</td>
      <td>558876</td>
      <td>6123874</td>
      <td>1853536</td>
      <td>10600376</td>
      <td>9106564</td>
    </tr>
    <tr>
      <th>2015Q2</th>
      <td>12264140</td>
      <td>3958930</td>
      <td>1317766</td>
      <td>496967</td>
      <td>291226</td>
      <td>336325</td>
      <td>193249</td>
      <td>2641163</td>
      <td>937029</td>
      <td>379874</td>
      <td>...</td>
      <td>356465</td>
      <td>1369721</td>
      <td>1013256</td>
      <td>10769675</td>
      <td>8899946</td>
      <td>557436</td>
      <td>6211388</td>
      <td>1869729</td>
      <td>10718003</td>
      <td>9224176</td>
    </tr>
    <tr>
      <th>2015Q3</th>
      <td>12382494</td>
      <td>3993596</td>
      <td>1326900</td>
      <td>497705</td>
      <td>295659</td>
      <td>340178</td>
      <td>193359</td>
      <td>2666696</td>
      <td>946571</td>
      <td>383041</td>
      <td>...</td>
      <td>367356</td>
      <td>1380892</td>
      <td>1013536</td>
      <td>10881970</td>
      <td>8994136</td>
      <td>553953</td>
      <td>6278542</td>
      <td>1887834</td>
      <td>10821082</td>
      <td>9321182</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 31 columns</p>
</div>


## Advanced topics
Throttling: The BEA api limits requests to a maximum of 100/minute and 100MB/minute (as well as 30 errors/minute). If the user exceeds this, they will be denied access for 1 hour. This package will automatically self-throttle, so in general, the user does not have to worry about that.

See the docs for additional information on:
- How to construct API queries to pull data from existing iTables.


## Quick Links
* [CODE_OF_CONDUCT.md](https://github.com/us-bea/.github/blob/main/CODE_OF_CONDUCT.md)
* [SECURITY](https://github.com/us-bea/beaapi/security/policy)
* [LICENSE](https://github.com/us-bea/beaapi/blob/main/LICENSE)
* [CONTRIBUTORS.md](https://github.com/us-bea/beaapi/blob/main/CONTRIBUTORS.md)
* [CONTRIBUTING.md](https://github.com/us-bea/beaapi/blob/main/CONTRIBUTING.md)
* [SUPPORT.md](https://github.com/us-bea/beaapi/blob/main/SUPPORT.md)
* [CHANGELOG.md](https://github.com/us-bea/beaapi/blob/main/CHANGELOG.md)

## Disclaimer
The United States Department of Commerce (DOC) GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. DOC has relinquished control of the information and no longer has responsibility to protect the integrity, confidentiality, or availability of the information. Any claims against the Department of Commerce stemming from the use of its GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

Use of this library may result in data being stored on users' local machines. Specifically, local copies of BEA API metadata may be stored and automatically updated in the `beaapi_data` directory (unless otherwise changed) in order to improve performance of `search_metadata()`.

