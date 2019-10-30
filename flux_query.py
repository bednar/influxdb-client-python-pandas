import pandas as pd
import time
from datetime import datetime

def build_from(bucket):
    return f'from(bucket: "{bucket}")'

def build_range(start, stop):
    return f'|> range(start:{start}, stop:{stop})'

def build_equals(key, value, prefix="r"):
    return f'{prefix}.{key} == "{value}"'

def build_filters(filters):
    filters_queries = []

    for filter in filters:
        or_query = ' or '.join([build_equals(filter[0], value) for value in filter[1]])
        filters_queries.append(f'|> filter(fn: (r) => {or_query})')

    return "\n".join(filters_queries)

def build_flux_query(bucket, filters, start, stop):
    return build_from(bucket) + "\n" + build_range(start, stop) + "\n" + build_filters(filters)

def dataframe(client,precision,query,org,tags):
    result = client.query_api().query(org="Org", query=query)
    raw = []
    for table in result:
        for record in table.records:
            for t in tags:

                raw.append((record.get_measurement(), t, record.values.get(t), record.get_field(), record.get_value(), record.get_time()))
    df=pd.DataFrame(raw, columns=['measurement','tag_key','tag_value','field','value','datetime'], index=None)
    df['datetime'] = df['datetime'].values.astype('<M8'+ '[' + precision + ']')
    return df

def lp(df,measurement,tag_key,tag_value,field,value,datetime):
    lines= [str(df[measurement][d]) + "," 
            + str(df[tag_key][d]) + "=" + str(df[tag_value][d]) 
            + " " + str(df[field][d]) + "=" + str(df[value][d]) + "," 
            + " " + str(int(time.mktime(df[datetime][d].timetuple()))) + "000000000" for d in range(len(df))]
    return lines
