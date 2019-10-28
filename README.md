InfluxDB 2.0 python-pandas library. The library covers InfluxDB 2.0. Built on top of the [InfluxDB 2.0 python client library](..influxdb-client-python)

## influxdb-client-python-pandas allation

***Querying data***

- Using Pandas to generate a simple Flux query for you
- Into Pandas DataFrame 

***Writing data using*** 

- Converting Pandas DataFrame into  [Line Protocol](https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial)

## Installation

InfluxDB python library uses [RxPY](https://github.com/ReactiveX/RxPY) - The Reactive Extensions for Python (RxPY).

### Requirements

**Python 3.6** or later is required.

**Pandas 0.25** or later is required.

### pip install

The influxdb-client-python package is hosted on Github, you can install latest version directly:

```
pip3 install git+https://github.com/influxdata/influxdb-client-python.git
```

Then import the package:

```
import influxdb_client
```

## Getting Started

Please follow the [Installation](../influxdb-client-python#installation) and then run the following:

```
#import dependencies 
import pandas as pd
import time
from datetime import datetime
from fbprophet import Prophet
from influxdb-client-python-pandas import build_flux_query
from influxdb-client-python-pandas import get_dataframe
from influxdb-client-python-pandas import lp 


from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
bucket = "my-bucket"
client = InfluxDBClient(url="http://localhost:9999", token="my-token", org="my-org")
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

```



## How to use

### How to build a simple flux query wi

```
query = build_flux_query("pandas ",["activity","weather","test"],{"location":["eur","us"],"season":["fall","summer"]},"-5d","-1h")
```

The output looks like: 

```
'from(bucket:"pandas ") |> range(start:-5d, stop:-1h) |> filter(fn: (r) => r._measurement == "activity" or r._measurement == "weather" or r._measurement == "test") |> filter(fn: (r) => r.location == "eur" or r.location == "us" or r.season == "summer")'
```

### Query 

Query your influxdb instance and return the data in a Dataframe with: 

```
my_df=get_dataframe('ns',query,"Org",["type","location"])
my_df.head()
```

```
measurement	| tag_key	 | tag_value | field     | value | datetime
----------- | -------  | --------- | -----     | ----- | --------
activity	| type     | ballet	   | fun_level | 6.0	 | 2019-10-24 18:10:17.529757
activity	| location | us	       | fun_level | 6.0	 | 2019-10-24 18:10:17.529757
activity	| type	   | tennis	   | fun_level | 8.0	 | 2019-10-24 18:10:17.529757
activity	| location | eur	   | fun_level | 8.0	 | 2019-10-24 18:10:17.529757
activity	| type	   | soccer	   | fun_level | 9.0	 | 2019-10-24 18:10:17.529757
```

### Writes

The [WriteApi](https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/write_api.py) supports synchronous, asynchronous and batching writes into InfluxDB 2.0. The data should be passed as a [InfluxDB Line Protocol](https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/), [Data Point](https://github.com/influxdata/influxdb-client-python/blob/master/influxdb_client/client/write/point.py) or Observable stream.

*The default instance of WriteApi use batching.*

For more information on the various write options please take a look at the  [InfluxDB 2.0 python client library](..influxdb-client-python)

To convert from DataFrame to line protocol specify the Dataframe and the column names corresponding to measurement, tag_key, tag_value, field, value, and datetime.  

```
my-lp = lp(my-df,"measurement","tag_key","tag_value","field","value","datetime")
```

Finally you can write the points with: 

```
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

_write_client = client.write_api(write_options=WriteOptions(batch_size=1000, 
                                                            flush_interval=10_000,
                                                            jitter_interval=2_000,
                                                            retry_interval=5_000))

_write_client.write("my-bucket", "my-org", my-lp)

```