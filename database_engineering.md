

```python
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, Column, Integer, Float, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from sqlalchemy import func
import pandas as pd
```


```python
# Use Pandas to read your cleaned measurements and stations CSV data.
meas_df = pd.read_csv("data/clean_measurements.csv")
sta_df = pd.read_csv("data/clean_stations.csv")
```


```python
meas_df["date"] = pd.to_datetime(meas_df["date"])
```


```python
engine = create_engine("sqlite:///hawaii.sqlite")
Base = declarative_base()
```


```python
# MEASUREMENTS
class Measure(Base):
    __tablename__ = "meas"
    index = Column(Integer, primary_key = True)
    station = Column(String(100))
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)
    
# STATIONS
class Stations(Base):
    __tablename__ = "sta"
    index = Column(Integer)
    station = Column(String(100), primary_key = True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
```


```python
# Create tables
Base.metadata.create_all(engine)
```


```python
# Check whether tables exist
engine.table_names()
```




    ['meas', 'sta']




```python
# Create session object
session = Session(bind = engine)
```


```python
# Connect to databse
conn = engine.connect()
```


```python
meas_orient = meas_df.to_dict(orient = "records")
sta_orient = sta_df.to_dict(orient = "records")
```


```python
conn.execute(Measure.__table__.insert(), meas_orient)
conn.execute(Stations.__table__.insert(), sta_orient)
```




    <sqlalchemy.engine.result.ResultProxy at 0x1c034cd8be0>




```python
engine.execute("select * from sta").fetchall()
```




    [(0, 'USC00519397', 'WAIKIKI 717.2, HI US', 21.2716, -157.8168, 3.0),
     (1, 'USC00513117', 'KANEOHE 838.1, HI US', 21.4234, -157.8015, 14.6),
     (2, 'USC00514830', 'KUALOA RANCH HEADQUARTERS 886.9, HI US', 21.5213, -157.8374, 7.0),
     (3, 'USC00517948', 'PEARL CITY, HI US', 21.3934, -157.9751, 11.9),
     (4, 'USC00518838', 'UPPER WAHIAWA 874.3, HI US', 21.4992, -158.0111, 306.6),
     (5, 'USC00519523', 'WAIMANALO EXPERIMENTAL FARM, HI US', 21.33556, -157.71139, 19.5),
     (6, 'USC00519281', 'WAIHEE 837.5, HI US', 21.45167, -157.84888999999995, 32.9),
     (7, 'USC00511918', 'HONOLULU OBSERVATORY 702.2, HI US', 21.3152, -157.9992, 0.9),
     (8, 'USC00516128', 'MANOA LYON ARBO 785.2, HI US', 21.3331, -157.8025, 152.4)]




```python
engine.execute("select * from meas limit 5").fetchall()
```




    [(0, 'USC00519397', '2010-01-01', 0.08, 65.0),
     (1, 'USC00519397', '2010-01-02', 0.0, 63.0),
     (2, 'USC00519397', '2010-01-03', 0.0, 74.0),
     (3, 'USC00519397', '2010-01-04', 0.0, 76.0),
     (4, 'USC00519397', '2010-01-06', None, 73.0)]


