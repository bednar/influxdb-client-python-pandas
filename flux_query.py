def build_flux_query(bucket,measurement,tags,start,stop):
    from_range = 'from(bucket:"' + bucket + '")' \
    ' |> range(start:' + start + ', stop:' + stop +')'
    if len(measurement) == 1:
        measurement = ' |> filter(fn: (r) => r._measurement == "' + measurement[0] 
    else:
        m = []
        for i in range(1,len(measurement)):
            m.append(' or r._measurement == "' + measurement[i] + '"') 
        measurement = ' |> filter(fn: (r) => r._measurement == "' + measurement[0] + '"' + "".join(m) + ')' 
    if len((list(tags.keys()))) == 1:
           tags = ' |> filter(fn: (r) => r.' + list(tags.keys())[0] + ' == " ' + tags[list(tags.keys())[0]]
    else:
        t = []
        for i in range(0,len(list(tags.keys()))):
            for j in range(1,len(tags[list(tags.keys())[i]])):
                t.append(' or r.' + list(tags.keys())[i] + ' == "' + tags[list(tags.keys())[i]][j] + '"') 
        tags = ' |> filter(fn: (r) => r.' + list(tags.keys())[0] + ' == "' + tags[list(tags.keys())[0]][0] + '"' + "".join(t) + ')' 
    query = from_range + measurement + tags 
    return query


def dataframe(precision,query,org,tags):
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