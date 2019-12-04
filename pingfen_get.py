from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys
import re
import json
import requests
import csv
#from seleniumrequests import Chrome



class Browser():
    def __init__(self,acc,pwd):
        self.chrome_options = Options()
        # #self.chrome_options.add_argument('--headless')
        # #self.chrome_options.add_argument('--disable-gpu')
        # #'--window-size=1366,768'
        self.chrome_options.add_argument('--window-size=1920,540')
        print("正在设置浏览器无头参数...请等待...")
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        print("浏览器对象无头参数设置成功...")
        self.headers = {
        'Content-Type': "application/json;charset=UTF-8",
        'User-Agent': "PostmanRuntime/7.17.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "a629ddbf-308f-4808-9f7b-88b5dd6f0b7b,56560839-f81c-4644-87d4-4473793eead7",
        'Host': "ad.e.kuaishou.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "151",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

        #self.browser = Chrome()
        self.acc = acc
        self.pwd =pwd
        self.DATE_TODAY = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        self.DATE_TODAY_start = int(time.mktime(time.strptime(self.DATE_TODAY, '%Y-%m-%d')))
        self.DATE_TODAY_end = time.strftime("%Y-%m-%d", time.localtime(time.time()))


    def login(self):
        #等待传入账号验证码信息  若判断失败 执行点击 '登录账号密码选项'
        #try:
        #定位三个信息的输入框
        print("浏览器访问登录界面....")
        self.browser.get("https://ad.e.kuaishou.com/#/welcome?redirectUrl=https%3A%2F%2Fad.e.kuaishou.com%2F%23%2Findex")
        time.sleep(2)
        print ('定位账号信息输入框...')
        input_account = self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[1]/input[1]')
        input_passwd = self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[2]/input[1]')
        #input_cert = self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]')
        #填写对应的三个信息
        print('填写对应的账号个信息...')
        input_account.send_keys(self.acc)
        print('输入账号完成')
        input_passwd.send_keys(self.pwd)
        print('输入密码完成')
        print ('点击登录按钮,等待两秒钟...')
        login = self.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]')
        login.click()

        print('..登录成功沉睡3秒,打印Cookie信息.....')
        #print(self.browser.get_cookies())
        #print(json.dumps(self.browser.get_cookies()))
        time.sleep(3)
        cookie_str = 'clientid=3; client_key=65890b29; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1557042909,1557047899,1557047905,1557047967; cna=feJtFDMWBxYCAXtwR0e95to4; isg=BOrqQLLjQ7amvM9akuHKVrZvO1YgS27Xvg-XRnSjmz3Ip4phXOnMxTrWN5seV-ZN;'
        for i in self.browser.get_cookies():
            if i['name'] == "kuaishou.ad.dsp_ph":
                self.url_key = i['value']
            cookie_str = cookie_str+i['name']+"="+i['value']+';'
        #print(cookie_str)
        self.cookie_str = cookie_str
        self.headers['cookie']= self.cookie_str
        print('++++++++++++++++++++')
    
    
    #获取视频列表信息
    def get_videos_key(self,currentPage = 1):
        #print('开始访问:....')
        url = "https://ad.e.kuaishou.com/rest/dsp/control-panel/search?"
        querystring = {"kuaishou.ad.dsp_ph":"{}".format(self.url_key)}
        payload = payload = "{\"searchParam\":{\"name\":\"\",\"statusValue\":52,\"sortingColumn\":\"totalCharge\",\"order\":2,\"appId\":0,\"searchLevel\":3,\"reportStartDay\":1559059200000,\"reportEndDay\":1573228799999,\"campaignId\":null,\"unitId\":null},\"pageInfo\":{\"currentPage\":1,\"pageSize\":300,\"totalCount\":300}}"
        
        response = requests.request("POST", url, data=payload, headers=self.headers, params=querystring)
        xxx = response.text
        xxx= json.loads(xxx)
        data =xxx['data']
        #print(data)
        items = []
        for i in data:
            if float(i['level']) == 0:
                continue
            item ={}
            item['花费'] = i['totalCharge']
            item['行为数'] = i['actionbarClick']
            item['封面点击率'] = i['photoClickRatio']
            item['分享数'] = i['share']
            item['评论数'] = i['comment']
            item['点赞数'] = i['likes']
            item['新增关注数'] = i['follow']
            item['举报数'] = i['report']
            item['拉黑数'] = i['block']
            item['减少此类作品数'] = i['negative']
            item['安卓下载完成数'] = i['downloadCompleted']
            item['激活数'] = i['conversion']
            item['注册数'] = i['eventRegister']
            item['次日留存数'] = i['eventNextDayStay']
            item['质量分'] = i['level']
            item['用户兴趣'] = i['p3trLevel']
            item['用户体验'] = i['htrLevel']
            item['转化效果'] = i['ltrLevel']
            tem =[]
            for key in item:
                tem.append(item[key])
            items.append(tem)

        filename = self.acc+'.csv'
        with open(filename, 'w+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["花费", "行为数", "封面点击率", "分享数", "评论数","点赞数","新增关注数","举报数", "拉黑数","减少此类作品数","安卓下载完成数","激活数","注册数","次日留存数", "质量分","用户兴趣","用户体验","转化效果"])
            for i in items:
                writer.writerow(i)
       
        

    def close(self):
        self.browser.quit()




        
if __name__ == '__main__':
    acc_dict ={
        

    }
    for i in acc_dict:
        try:
            dri = Browser(i,acc_dict[i]) #实例化浏览器对象
            dri.login() #输入验证信息
            #dri.get_account_info() #获取账号信息(未完成)
            dri.get_videos_key() #获取账号信息 并写成文件
            dri.close() #关闭浏览器窗口
        except Exception as e: 
            print(e)
            continue
        


