import flux_query as f

def test_build_from():
    assert f.build_from(bucket="my_bucket") == 'from(bucket: "my_bucket")'

def test_build_range():
    assert f.build_range(start="-1h", stop="-10m") == '|> range(start:-1h, stop:-10m)'

def test_build_equals():
    assert f.build_equals(key="key",
                        value="value") == 'r.key == "value"'
    assert f.build_equals(key="key", value="value",
                        prefix="x",) == 'x.key == "value"'

def test_build_filters():
    assert f.build_filters(filters=[("_measurement", ["abc"])]) == '|> filter(fn: (r) => r._measurement == "abc")'
    assert f.build_filters(filters=[("_measurement", ["abc"]),("key", ["value"])]) == '|> filter(fn: (r) => r._measurement == "abc")\n|> filter(fn: (r) => r.key == "value")'

    assert f.build_filters(filters=[("_measurement", ["abc", "def"]), ("key", ["value"])]
                     ) == '|> filter(fn: (r) => r._measurement == "abc" or r._measurement == "def")\n|> filter(fn: (r) => r.key == "value")'

def test_build_flux_query():
    assert f.build_flux_query(bucket="my_bucket", start="-1h", stop="2h", filters=[("_measurement",["abc"]),("key",["1","2"])]) == """from(bucket: "my_bucket")\n|> range(start:-1h, stop:2h)\n|> filter(fn: (r) => r._measurement == "abc")\n|> filter(fn: (r) => r.key == "1" or r.key == "2")"""