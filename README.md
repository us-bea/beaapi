
# beaapi
  beaapi: A Python library library to make it easier to retrieve and work with BEA data. 

For documentation online, see [here](https://us-bea.github.io/beaapi/).

For development and building information, see [CONTRIBUTING.md](https://github.com/us-bea/beaapi/blobl/main/CONTRIBUTING.md).

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
import os
from dotenv import load_dotenv
load_dotenv()
beakey = os.environ.get("beakey")
```

## Get metadata
The BEA data is distributed across various datasets that each contain many tables. To get a list of the datasets available on the API, use `get_data_set_list()`:


```python
list_of_sets = beaapi.get_data_set_list(beakey)
display(list_of_sets)  # Note the last dataset is only for speeding up metadata queries
```


<div>
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
      <td>GDPbyIndustry</td>
      <td>GDP by Industry</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Regional</td>
      <td>Regional data sets</td>
    </tr>
    <tr>
      <th>10</th>
      <td>UnderlyingGDPbyIndustry</td>
      <td>Underlying GDP by Industry</td>
    </tr>
    <tr>
      <th>11</th>
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




<div>
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
      <td>12083904</td>
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
      <td>12224707</td>
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
      <td>12083904</td>
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
      <td>12224707</td>
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
print("Notes corresponding to NoteRef:")
display(bea_tbl.attrs['detail']['Notes'].head())
```

    Extra detail keys:dict_keys(['Statistic', 'UTCProductionTime', 'Dimensions', 'Notes'])
    Let's look at some interesting ones.
    Statistic: NIPA Table
    Notes corresponding to NoteRef:
    


<div>
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
      <th>19</th>
      <th>20</th>
      <th>21</th>
      <th>22</th>
      <th>23</th>
      <th>24</th>
      <th>25</th>
      <th>26</th>
      <th>27</th>
      <th>28</th>
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
      <td>12083904</td>
      <td>3867908</td>
      <td>1283823</td>
      <td>465426</td>
      <td>285887</td>
      <td>332965</td>
      <td>199546</td>
      <td>2584085</td>
      <td>917371</td>
      <td>366171</td>
      <td>...</td>
      <td>814298</td>
      <td>960760</td>
      <td>992461</td>
      <td>362114</td>
      <td>1367850</td>
      <td>1005736</td>
      <td>10619844</td>
      <td>546689</td>
      <td>10570891</td>
      <td>9107467</td>
    </tr>
    <tr>
      <th>2015Q2</th>
      <td>12224707</td>
      <td>3927357</td>
      <td>1309627</td>
      <td>481820</td>
      <td>292631</td>
      <td>333600</td>
      <td>201577</td>
      <td>2617730</td>
      <td>916930</td>
      <td>368315</td>
      <td>...</td>
      <td>828712</td>
      <td>977198</td>
      <td>1003757</td>
      <td>363147</td>
      <td>1374002</td>
      <td>1010855</td>
      <td>10759482</td>
      <td>548295</td>
      <td>10693235</td>
      <td>9228648</td>
    </tr>
    <tr>
      <th>2015Q3</th>
      <td>12347752</td>
      <td>3960436</td>
      <td>1318493</td>
      <td>481620</td>
      <td>297306</td>
      <td>337083</td>
      <td>202483</td>
      <td>2641944</td>
      <td>924494</td>
      <td>370385</td>
      <td>...</td>
      <td>836130</td>
      <td>978430</td>
      <td>1012278</td>
      <td>373825</td>
      <td>1385653</td>
      <td>1011828</td>
      <td>10877903</td>
      <td>545354</td>
      <td>10802962</td>
      <td>9333737</td>
    </tr>
  </tbody>
</table>
<p>3 rows × 28 columns</p>
</div>


## Advanced topics
Throttling: The BEA api limits requests to a maximum of 100/minute and 100MB/minute (as well as 30 errors/minute). If the user exceeds this, they will be denied access for 1 hour. This package will automatically self-throttle, so in general, the user does not have to worry about that.

See the docs for additional information on:
- How to construct API queries to pull data from existing iTables.


## Quick Links
* [CODE_OF_CONDUCT.md](https://github.com/us-bea/.github/blob/main/CODE_OF_CONDUCT.md)
* [SECURITY](https://github.com/us-bea/beaapi/security/policy)
* [LICENSE](https://github.com/us-bea/beaapi/blobl/main/LICENSE)
* [CONTRIBUTING.md](https://github.com/us-bea/beaapi/blobl/main/CONTRIBUTING.md)
* [SUPPORT.md](https://github.com/us-bea/beaapi/blobl/main/SUPPORT.md)
* [CHANGELOG.md](https://github.com/us-bea/beaapi/blobl/main/CHANGELOG.md)

## Disclaimer
The United States Department of Commerce (DOC) GitHub project code is provided on an ‘as is’ basis and the user assumes responsibility for its use. DOC has relinquished control of the information and no longer has responsibility to protect the integrity, confidentiality, or availability of the information. Any claims against the Department of Commerce stemming from the use of its GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

Use of this library may result in data being stored on users' local machines. Specifically, local copies of BEA API metadata may be stored and automatically updated in the `beaapi_data` directory (unless otherwise changed) in order to improve performance of `search_metadata()`.

