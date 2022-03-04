# %%
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd


# %%
r = requests.get('https://escapefromtarkov.fandom.com/wiki/Crafts')
#r.text

# %%
soup = BeautifulSoup(r.text, 'html.parser')
tables = soup.findAll("table")
print(tables)

# %%
arr = []
for table in tables:
    for row in table.find_all("tr")[1:]:
    #print(type(row.find("th")))
    #print(type(row.find_all("th")[1]))
        for th in row.find_all("th"):
            str = ''
            for x in th:
                str+= x.text + ' '
            if th.text != '→\n':
                arr.append(str.strip().replace('\n',''))
arr = np.reshape(arr, (-1,3))
df = pd.DataFrame(data=arr, columns=['input', 'module and time', 'output'])   
        
        

# %%
#split module and time
modules = []
times = []
for row in df['module and time']:
    x = re.search(r"[1-9]", row)
    module = row[:x.start()+1]
    time = row[x.start()+1:]
    modules.append(module)
    times.append(time)

df['module'] = modules
df['time'] = times

# %%
df

# %%
#convert time to seconds
time=df['time']
totalSeconds = []
#inconsistant format. convert 'hour' to 'h' and 'minutes' to 'min'
time=[item.replace('hour','h') if 'hour' in item else item for item in time]
time=[item.replace('minutes','min') if 'minutes' in item else item for item in time]

#calculate total time in seconds
for row in time:
    hour=0
    minute=0
    second=0

    x = re.search(r"h", row)
    if x != None:
        hour = int(row[:x.start()].strip())
        row = row[x.start()+1:]
    x = re.search(r"min", row)
    if x != None:
        minute = int(row[:x.start()].strip())
        row = row[x.start()+3:]
    x = re.search(r"sec", row)
    if x != None:
        second = int(row[:x.start()].strip())
    
    totalSeconds.append((hour*3600)+minute*60+second)
#print(x)
df['totalSeconds'] = totalSeconds
df = df.drop('module and time', axis=1)
df

# %% [markdown]
# from pathlib import Path  
# filepath = Path('folder/subfolder/out.csv')  
# filepath.parent.mkdir(parents=True, exist_ok=True)  
# df.to_csv(filepath) 


