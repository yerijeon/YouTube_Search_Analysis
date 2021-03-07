import pandas as pd
import sys

today_date= sys.argv[1] # sys[1]:manually input date
def date_cleaner(x):
    
    tmp_date=[]
    
    for x in df['date']:
        
        if x[-2].isnumeric() == False: # 당일 최초 공개 또는 당일 스트리밍 시작==today
            tmp_date.append(today_date)
            
        elif x[0].isnumeric()==False: # 이전 최초공개, 이전 스트리밍==해당날짜
            tmp_x=x.split(":")[1].strip()
            tmp_date.append(tmp_x)
            
        else:
            tmp_date.append(x)
            
    df['date']=tmp_date
    
    return df['date']


def time_cleaner(x):
    
    time=x.split(":") # ":" 기준으로 나눔
    
    
    if len(time) == 2: # 분,초
        return int(time[0])*60 + int(time[1]) # 분*60+초
    else: # 시간단위면
        return int(time[0])*3600 + int(time[1])*60 + int(time[2])


def subs_cleaner(x):
    
    sub=x[:-2]
    
    try:
        if x[-2] == '만':
            return (round(float(sub)*10000))
        elif x[-2] == '천':
            return (round(float(sub)*1000))
        elif x[-2].isnumeric() == True:
            return int(x[:-1])
        else:
            return x
    except:
        return x

# import data and apply function
df=pd.read_csv(sys.argv[2],index_col=0) # sys[2]: import file

df.apply(date_cleaner,axis=1)
df['date']=pd.to_datetime(df['date'])
df['search date']=pd.to_datetime(df['search date'])
df['time']=df['time'].apply(lambda x: '0:00' if not x[0].isnumeric() else x)
df['time_sec']=df['time'].apply(time_cleaner)
df=df.drop('time',axis=1)
df['subscribers']=df['subscribers'].fillna('0만명')
df['subscribers']=df['subscribers'].apply(subs_cleaner)

# other numeric columns(view counts, like, dislike, comments)
target_col=['view count','like','dislike','comments']
df[target_col]=df[target_col].fillna('0,0')
# dislike
df['dislike']=df['dislike'].apply(lambda x: '0,0' if x=='없' else x)
for col in target_col:
    df[col]=df[col].apply(lambda x: str(x).replace(",",""))
    df[col]=pd.to_numeric(df[col], downcast='integer')

df.to_csv(sys.argv[3]) # sys[3]: save file

