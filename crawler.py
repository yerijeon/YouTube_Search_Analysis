# Collect search results by keywords
# import modules
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import sys


keyword = [sys.argv[1]] # sys[1]:search keyword

# list: url, duration
url_list={'keyword':[],'url':[]}
duration_list={'keyword':[],'duration':[]}
rank={'keyword':[],'rank':[]}
driver = webdriver.Chrome('chromedriver.exe')

for word in keyword:
    url='https://www.youtube.com/results?search_query={}'.format(word)
    driver.get(url)
    time.sleep(4)
    html = BeautifulSoup(driver.page_source, 'html.parser')
    html=html.find_all('ytd-video-renderer')
    time.sleep(4)
    
    for i in range(0,10):


        # url
        x=html[i].find('a')['href']
        url=("https://www.youtube.com{}".format(x))
        url_list['url'].append(url)

        # duration
        duration=html[i].find('span').text.strip()
        duration_list['duration'].append(duration)

        rank['rank'].append(i)
        rank['keyword'].append(word)
        url_list['keyword'].append(word)
        duration_list['keyword'].append(word)
    
print("Done")
driver.close()

df1=pd.DataFrame(data=url_list['url'],index=url_list['keyword'])
df2=pd.DataFrame(data=duration_list['duration'],index=url_list['keyword'])
df3=pd.DataFrame(data=rank['rank'],index=rank['keyword'])
df4=pd.concat([df1,df2,df3],axis=1)
df4=df4.reset_index()
df4.columns=['category','url', 'time','rank']

print("First step: collect results by keywords DONE")

# attach video info
def get_youtube_info_third(url):
    
    # collect html
    driver.get(url)
    time.sleep(10)
    
    # scroll down to scrap information, load until source is ready to be collected
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
    time.sleep(5) 
    
    

    html=driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(3)
    

    # append ('NaN') if the information is not available or hidden
    
    # collect channel name
    name0=soup.find('yt-formatted-string',{'class':'ytd-channel-name'}).text
    name.append(name0)

    # number of subscribers
    try:
        subs0=soup.find(id="owner-sub-count").text.split(" ")[1]
        subs.append(subs0)
    except:
        subs.append('NaN')

    # Video title
    title0=soup.find('h1').text
    title.append(title0)

    # current view counts
    view0=soup.find('span',{'class':'view-count'}).text.split(" ")[1].strip()[:-1]
    view.append(view0)

    # number of likes and dislikes
    likeinfo=soup.find_all('yt-formatted-string',{'id':'text','class':"style-scope ytd-toggle-button-renderer style-text"})
    try:
        likenum=likeinfo[0].get("aria-label").split(" ")[1][:-1]
        like.append(likenum)
        disnum=likeinfo[1].get("aria-label").split(" ")[1][:-1]
        dislike.append(disnum)

    except:
        like.append('NaN')
        dislike.append('NaN')

    # date uploaded
    date0=soup.find_all('yt-formatted-string',{'class':'style-scope ytd-video-primary-info-renderer'})[1].text
    date.append(date0)
    
    #number of comments
    try:
        com=soup.find('h2',{'id':'count'}).find('yt-formatted-string').text.split(" ")[1].strip()[:-1]
        comments.append(com)
    except:
        comments.append('NaN')

    #hashtag  
    tmp_lst=[]
    a=soup.find('yt-formatted-string',{'class':'content'}).find_all('a')
    b=[a[i].text for i in range(len(a))]
    
    try:
        for i in range(len(b)):
            if b[i][0]=="#":
                tmp_lst.append(b[i])
    except:
        tmp_lst.append('NaN')
    hashtag.append(tmp_lst)
    
    # append information to Series
    result['name']=name
    result['subscribers']=subs
    result['title']=title
    result['view count']=view
    result['like']=like
    result['dislike']=dislike
    result['comments']=comments
    result['date']=date
    result['hashtag']=hashtag


            
    return pd.Series(result)

# create empty lists to collect information
name=[]
subs=[]
title=[]
view=[]
like=[]
dislike=[]
date=[]
hashtag=[]
comments=[]
result={}

# collection start

driver = webdriver.Chrome('/Users/jeon-yeli/Documents/Project/Youtube/chromedriver')
df4['url'].apply(get_youtube_info_third)
driver.close()
result=pd.DataFrame(result)

print("Second Step: collect video information DONE")

# attach today
today_date=sys.argv[2] # sys.argv[2]: manually input today's date
today=[]
for i in range (0,50):
    today.append(today_date) 

result['search date']=today

# concat two file
new_df=pd.concat([df4,result],axis=1)
new_df.to_csv(sys.argv[3]) # sys.argv[3]: save final dataframe to csv file

print("Third Step: Attach Today DONE")

