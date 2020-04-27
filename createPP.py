
# coding: utf-8

# ## Next Steps
# 
# ## History
# - 27.04.20: dynamic axes
# - 20.11.19: replace missing 3YPerf-values by 3YPerf-mean
# - 20.11.19: add parameter for 3MPerf calculation by quantiles or absolute values
# - 19.11.19: removed missing values addition
# - 17.11.19: added Depot as bubble
# - 17.11.19: 3M Performance now in 20% quantiles
# - 16.11.19: initial version

# In[101]:


import datetime
import pandas as pd
import sys
from numpy import nan as NA
import math


# In[102]:


useQuantiles = True
if len(sys.argv) > 1:
    arg = sys.argv[1] 
else:
    arg=''
if 'absolut' in arg:
        useQuantiles = False


# In[103]:


def floatconv(val):
    try:
        if val.strip():
            return float(val.replace('.','').replace(',','.'))
        else:
            return 0
    except ValueError as ve:
        print("VALUE NOT USABLE for floatconv: #{}#".format(val))


# In[104]:


def percentconv(val):
    try:
        if '%' in val:
            return floatconv(val.replace('%', ''))
        else:
            return NA
    except ValueError as ve:
        print("VALUE NOT USABLE for percentconv: #{}#".format(val))


# In[105]:


intconv = lambda val: 0 if len(str(val)) < 2 else float(str(val).replace('.',''))
converter = {'Aktuell':floatconv, 'Wert in EUR':floatconv, 'Perf. 3 Monate':percentconv,              'Perf. 1 Jahr':percentconv, 'Perf. 3 Jahre':percentconv}


# In[106]:


wkn2short = pd.read_csv('wkn2names.csv', header=None, sep=':', index_col=0, squeeze=True).to_dict()

def shortname(longname):
    return wkn2short[longname]


# In[107]:


#filename = "musterdepot_Komplett_meineuebersicht_20191112_1043.csv"
filename = "musterdepot_Komplett_meineuebersicht.csv"
#data = pd.read_csv(filename, sep=";", header=2, encoding="iso-8859-1", converters = converter, usecols=[0,2,4,19,20,21])
data = pd.read_csv(filename, sep=";", header=2, encoding="iso-8859-1", converters = converter, usecols=["Stück","WKN","Aktuell","Perf. 3 Monate","Perf. 1 Jahr","Perf. 3 Jahre"])
data['Wert'] = data['Stück']*data['Aktuell']
data['Name'] = data['WKN'].apply(lambda x: shortname(x[0:23]))


# In[108]:


a='Amundi Index Solutions'
b=a.replace('Amundi Index Solutions','AIS')
b
data


# In[109]:


# add missing values: (better than adding missing values is selecting a better stock exchange)
#Nasdaq Performance
#data.loc[0,'Perf. 3 Jahre'] = 61
#TecDax Performance
#data.loc[2,'Perf. 3 Jahre'] = 75
#A2ANH0 Performance
#data.loc[9,'Perf. 3 Jahre'] = 55

# or simply replace by mean value:
data['Perf. 3 Jahre'].fillna(data['Perf. 3 Jahre'].mean(),inplace=True)


# In[110]:


data


# In[111]:


x_min = math.floor(data["Perf. 3 Jahre"].min()/10)*10
x_max = math.ceil(data["Perf. 3 Jahre"].max()/10)*10
y_min = math.floor(data["Perf. 1 Jahr"].min()/10)*10
y_max = math.ceil(data["Perf. 1 Jahr"].max()/10)*10


# In[112]:


def get_range_str(min,max):
    range_str = str(min)
    for i in range(min,max,10):
        range_str=range_str+","+str(i+10)
    return range_str


# In[113]:


def perf2String(val,quantiles):
    if val < quantiles[0.2]:
        return 'lowest'
    if val < quantiles[0.4]:
        return 'low'
    if val < quantiles[0.6]:
        return 'mid'
    if val < quantiles[0.8]:
        return 'high'
    return 'highest'

def perf2Stringabsolut(val):
    if val < -4:
        return 'lowest'
    if val < 0:
        return 'low'
    if val < 2:
        return 'mid'
    if val < 4:
        return 'high'
    return 'highest'


# In[114]:


if useQuantiles == True:
    quantiles = data['Perf. 3 Monate'].quantile([0.2,0.4,0.6,0.8])
    data['Perf3MString'] = data['Perf. 3 Monate'].apply(lambda x: perf2String(x,quantiles))
else:
    data['Perf3MString'] = data['Perf. 3 Monate'].apply(lambda x: perf2Stringabsolut(x))


# In[115]:


data['Value3MAgo'] = data['Wert']/(1+data['Perf. 3 Monate']/100)
data['Value1YAgo'] = data['Wert']/(1+data['Perf. 1 Jahr']/100)
data['Value3YAgo'] = data['Wert']/(1+data['Perf. 3 Jahre']/100)

valuetoday = data['Wert'].sum()
v3mago = data['Value3MAgo'].sum()
v1yago = data['Value1YAgo'].sum()
v3yago = data['Value3YAgo'].sum()
p3m = (valuetoday/v3mago-1)*100
p1y = (valuetoday/v1yago-1)*100
p3y = (valuetoday/v3yago-1)*100
print("Portfolio total value: {0:7.2f}, 3-month-performance: {1:3.2f}% , 1Y-perf: {2:3.2f}%, 3Y-perf: {3:3.2f}%"
      .format(valuetoday,p3m,p1y,p3y))


# In[116]:


def rd(val):
    return int(round(val))


# In[117]:


#['Name','3JPerf','1J Perf','3M Perf','EUR'],
#['Nasdaq',32,22,'high',3214],

#lines with values:
values=""
for i, (index, row) in enumerate(data.sort_values(by=['Perf. 3 Monate']).iterrows()):
    values += "['"+row['Name']+"',"     +str(rd(row['Perf. 3 Jahre']))+","     +str(rd(row['Perf. 1 Jahr']))+",'"     +row['Perf3MString']+"',"     +str(rd(row['Wert']))+"],"     +'\n'

#Depot line with 1y and 3y performance and 3m as part of the name (special color)    
values += "['Depot 3M:"+str(round(p3m,2))+"%'," +str(rd(p3y))+"," +str(rd(p1y))+"," +"'Depot','" +str(50000) +"']\n"


# In[118]:


# read template, replace placeholder and write output file:
with open('portfolioPerformance_in.html','rt') as fin, open('portfolioPerformance.html','wt') as fout:
    for line in fin:
        if '#$0' in line:
            line = line.replace('#$0',values) 
        if '#$1' in line:
            today = datetime.date.today()
            line = line.replace('#$1',today.strftime('%d.%m.%Y'))
        if '#$2' in line:
            if useQuantiles == True:
                line = line.replace('#$2',str(quantiles.values))
            else:
                line = line.replace('#$2','[-4;0;2;4[')
        if '#$3' in line:
            line = line.replace('#$3',get_range_str(x_min,x_max))
        if '#$4' in line:
            line = line.replace('#$4',get_range_str(y_min,y_max))
        fout.write(line)

