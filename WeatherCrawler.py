import requests
import re
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Host':'www.tianqihoubao.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Cookie': 'Hm_lvt_f48cedd6a69101030e93d4ef60f48fd0=1574492500; ASP.NET_SessionId=n0ljqp55g1k5yauc4pzfhx45; __tins__4560568=%7B%22sid%22%3A%201574518508687%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201574520308687%7D; __51cke__=; __51laig__=1'
}

urls = []
weathers = []
w_line = ['date,weather_day,weather_night,temperature_day,temperature_night,wind_day,wind_night']
for year in range(2011,2020):
    for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        if str(year) + str(month) != '201912':
            date_url = 'http://www.tianqihoubao.com/lishi/changchun/month/' + str(year) + str(month) + '.html'
            urls.append(date_url)
pattern1 = re.compile(r'<table(.*?)</table>', re.S)
pattern2 = re.compile(r'<tr>(.*?)</tr>', re.S)
pattern3 = re.compile(r'<td>(.*?)</td>', re.S)
pattern4 = re.compile(r'>(.*?)</a>', re.S)

for url in urls:
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    print(time_str, '  ', url)
    try:
        response = requests.get(url, headers=headers, verify = False)
        if response.status_code == 200:
            text = response.text
    except Exception as e:
        print(e)
    table_data = re.findall(pattern1, text)[0].replace('\r\n', '')
    day_data = re.findall(pattern2, table_data)
    for day in day_data:
        if '日期' not in day:
            day = day.replace(' ', '')
            day_infos = re.findall(pattern3, day)
            for i in range(len(day_infos)):
                if '</a>' in day_infos[i]:
                    day_infos[i] = re.findall(pattern4, day_infos[i])[0]
            weathers.append({'date': day_infos[0], 'weather': day_infos[1], 'temperature': day_infos[2], 'wind': day_infos[3]})
    for weather in weathers:
        a_line = weather['date']+','+weather['weather']+','+weather['temperature']+','+weather['wind']
        w_line.append(a_line.replace('/',','))
new_w_line = []
for ww in w_line:
    if ww not in new_w_line:
        new_w_line.append(ww)
new_info = '\n'.join(new_w_line)
with open('weather_by_day_night.csv', 'w') as f:
    f.write(new_info)
    f.close()
