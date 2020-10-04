from oauth2client.service_account import ServiceAccountCredentials
import gspread
from pprint import pprint
import time
from datetime import datetime,date
import pytz
tz = pytz.timezone('Asia/Bangkok')
thai_now = datetime.now(tz)



scope = ["https://spreadsheets.google.com/feeds",
'https://www.googleapis.com/auth/spreadsheets',
"https://www.googleapis.com/auth/drive.file",
"https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('LaLinDB-e9dce464af7c.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('calendar')
Test_predict = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('Test_predict')
logs = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('logs_Chat')
data = sheet.get_all_records()

def connect_topic():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('intent_topic')
    data = sheet.get_all_records() 
    return data


def connect_time():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('intent_time')
    data = sheet.get_all_records() 
    return data


def connect_year():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('intent_year')
    data = sheet.get_all_records() 
    return data


def connect_calendar():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('calendar')
    data = sheet.get_all_records() 
    return data

def connect_student_grade():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('student_grade')
    data = sheet.get_all_records() 
    return data

def connect_logs_chat():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('logs_Chat')
    data = sheet.get_all_records() 
    return data


def connect_verify():
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1FpsAg_7Rs2u3yYeP39iduZ5P2ea_-72ONIs6Hw0dyl4/edit?usp=sharing").worksheet('verify')
    data = sheet.get_all_records() 
    return data


def connect_Test_data(intent,tokenizer,topic_predict,time_predict,year_predict):
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1UatZjy4Oeyqu-m12wUyLJwHjB8LkH2s2figRVmmrvvU/edit?usp=sharing").worksheet('result_test')
    insertRow = [intent,tokenizer,topic_predict,time_predict,year_predict]
    sheet.insert_row(insertRow,2)



def tranform_data_topic():
    data = connect_topic()
    dataList = []
    dataGS = {'tag':'','patterns':''}
    x = 'patterns'
    x += str(1)
    y = []
    n = 1
    for i in range(len(data)):
        while n<len(data[i]):
            y.append(data[i][x])
            x = 'patterns'
            x += str(n)
            if n > len(data[i]):
                break
            else:
                n+=1
        n = 1
        dataGS['tag'] = data[i]['tag']
        dataGS['patterns'] = y
        dataList.append(dataGS)
        dataGS = {'tag':'','patterns':''}
        y=[]
    return dataList

def tranform_data_topic_(topic):
    data = topic
    dataList = []
    dataGS = {'tag':'','patterns':''}
    x = 'patterns'
    x += str(1)
    y = []
    n = 1
    for i in range(len(data)):
        while n<len(data[i]):
            y.append(data[i][x])
            x = 'patterns'
            x += str(n)
            if n > len(data[i]):
                break
            else:
                n+=1
        n = 1
        dataGS['tag'] = data[i]['tag']
        dataGS['patterns'] = y
        dataList.append(dataGS)
        dataGS = {'tag':'','patterns':''}
        y=[]
    return dataList





def select_name_tag(name):
    data = connect_topic()
    result = (list(filter(lambda x:x["tag"]==name,data)))
    return result



# data = tranform_data_topic()
# for i in data:
#     print(i['patterns'])