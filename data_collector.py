# Data
import pandas as pd

# Homepage request
import time
import requests

# Save
from datetime import datetime


def request_appid(lists=[0]):
    df = pd.DataFrame()
    for val in lists:
        html = requests.get(url="https://steamspy.com/api.php", params={"request" : "all", "page": val})
        data = html.json()

        df_small = pd.DataFrame.from_dict(data, orient='index')
        df = pd.concat([df, df_small], axis=0)  # 병합
    return df[['appid', 'name']].sort_values('appid').reset_index(drop=True)

def request_data(id):
    html = requests.get(url="https://steamspy.com/api.php", params={"request" : "appdetails", "appid" : id})
    data = html.json()

    df = pd.DataFrame.from_dict(data, orient='index')
    return df.transpose()

def save_data(DF):
    # ============== 주요 자료들 저장 ==============
    crawl_date = str(datetime.today())[:-7]

    f = open('date_info.txt', 'w')
    f.write("Crawled Date : " + crawl_date)
    DF.to_csv('steam_data.csv', index=False)
    f.close()
    print("Data saved!")


# ============== Main ==============

df_id = request_appid([0])  # 게임 아이디 추출
print(df_id.count())  # Data 개수 확인.
print(df_id.head())
print(df_id.tail())
input(' Checking Full data. ')

df_data = pd.DataFrame()  # 게임 정보 추출

for i, row in df_id.iterrows():  # 얻어낸 정보에 대한 id를 대입.
    df_small_data = request_data(row[0])  # 단일 게임에 대해 추출.
    df_data = pd.concat([df_data, df_small_data], axis=0)  # 병합
    print("Saved -", i, "]", df_small_data['name'][0])
    if i%100 == 99:
        print("For the traffic, wait 7 sec.")
        time.sleep(7)

save_data(df_data)