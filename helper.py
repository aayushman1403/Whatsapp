from urlextract import URLExtract
extractor = URLExtract()#object creation 
from wordcloud import WordCloud
import pandas as pd
from collections import Counter


def fetch_stats(selected_user,df):
    if selected_user=='overall':
        # fetch no of msgs
        num_messages=df.shape[0]
        # fetch no of words
        words= []
        for message in df['message']:
            words.extend(message.split())
        #fetch no of media files
        num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
        #fetch no of links
        links=[]
        for message in df['message']:
            links.extend(extractor.find_urls(message))

        return  num_messages,len(words),num_media_messages,len(links)
    else:
        new_df=df[df['user']==selected_user]
        num_messages=new_df.shape[0]

        words= []
        for message in new_df['message']:
            words.extend(message.split())
        
        #fetch no of media files
        num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

        #fetch no of links
        links=[]
        for message in new_df['message']:
            links.extend(extractor.find_urls(message))

        return  num_messages,len(words),num_media_messages,len(links)
        # 0 depicts rows 1 depicts columns

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(
        columns={'user':'name','index':'percent'})
    return x,df
    

def create_wordcloud(selected_user, df):
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    if selected_user == 'overall':
        text = df['message'].str.cat(sep=" ")  # Combine all messages
    else:
        new_df = df[df['user'] == selected_user]
        text = new_df['message'].str.cat(sep=" ")  # Combine messages for specific user

    wc.generate(text)  # Generate the word cloud with the appropriate text
    return wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []  
    if selected_user == 'overall':
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)
    else:
        new_df = temp[temp['user'] == selected_user]  
        for message in new_df['message']:
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):
    if selected_user == 'overall':
        timeline=df.groupby(['year', 'month']).count()['message'].reset_index()
        
        time=[]
        for i in range(len(timeline)):
            time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

        timeline['time']=time

    else:
        new_df = df[df['user'] == selected_user]
        timeline=new_df.groupby(['year', 'month']).count()['message'].reset_index()
        time=[]
        
        for i in range(len(timeline)):
            time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
        
        timeline['time']=time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user == 'overall': 
        daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    else:
        new_df = df[df['user'] == selected_user]
        daily_timeline=new_df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


def weekly_activity(selected_user,df):
    if selected_user == 'overall':
        return df['day_name'].value_counts()
    else:
        new_df = df[df['user'] == selected_user]  
        return new_df['day_name'].value_counts() 


def month_activity(selected_user,df):
    if selected_user == 'overall':
        return df['month'].value_counts()
    else:
        new_df = df[df['user'] == selected_user]  
        return new_df['month'].value_counts()

def heatmap(selected_user,df):
    if selected_user == 'overall':
        heatmap_activity=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    else:
        new_df = df[df['user'] == selected_user]
        heatmap_activity=new_df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return heatmap_activity