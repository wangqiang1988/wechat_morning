import push_wechat
import datetime
import requests
import os
def get_time():
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return current_time

def get_weather():
    counter = 0
    headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
}

    params = (
    ('city', '110105'), #city id
    ('key', os.environ.get('amap_key')), #key
    ('extensions','all'),
)

    while counter < 3:
        try:
            response = requests.get('https://restapi.amap.com/v3/weather/weatherInfo', headers=headers, params=params,timeout=3)
            weather = response.json()['forecasts'][0]['casts'][0]
            message ="星期"+weather['week']+"\n"+"白天:"+weather['dayweather']+" 温度:"+weather['daytemp']+" 风力:"+weather['daypower']+'\n'+"夜间:"+weather['nightweather']+" 温度:"+weather['nighttemp']+" 风力:"+weather['nightpower']
            break
        except:
            counter+=1
    return message



if __name__ == '__main__':
    wx=push_wechat.WeChat()
    current_time = get_time()
    print(current_time)
    weather_message = get_weather()
    print(weather_message)
    wx.send_data('起床时间:%s'%current_time+'\n'+weather_message)