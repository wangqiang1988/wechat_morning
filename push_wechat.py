import time
import requests
import json
import os

class WeChat:
    def __init__(self):
        self.CORPID = os.environ.get('wechat_corpid')  #企业ID，在管理后台获取
        self.CORPSECRET = os.environ.get('wechat_corpsecret')#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = os.environ.get('wechat_agentid')  #应用ID，在后台应用中获取
        self.TOUSER = "WangQiang"  # 接收者用户名,多个用户用|分割
 
    def _get_access_token(self):
        url = os.environ.get('pusher_url')+'/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        print(req,'------------------------------------')
        data = json.loads(req.text)
        return data["access_token"]
 
    def get_access_token(self):
        try:
            with open('./access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('./access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('./access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token
 
    def send_data(self, message):
        send_url = os.environ.get('pusher_url')+'/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
                },
            "safe": ""
            }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  
        return respone["errmsg"]
 
if __name__ == '__main__':
    wx = WeChat()
    wx.send_data("这是一条测试消息")
    print()
