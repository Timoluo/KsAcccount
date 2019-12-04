import sys
import requests
import re
import hashlib

from selenium import webdriver
import selenium.webdriver.support as su
import selenium.webdriver.common as cm
import getOSpid as gop

class NewADViewer:

    adv= "528" 
    userid= "144" 
    account="13585717023"
    pwd="Zw2019"
    

    def inputAccount(self):
        # http://chromedriver.storage.googleapis.com/index.html  install chrome driver
        #self.reg()
        #disable info bar
        option=webdriver.ChromeOptions()
        option.add_argument('--start-maximized')
        option.add_argument('--disable-infobars')
        #option.add_argument('allow-running-insecure-content')

        browser=webdriver.Chrome(options=option)
        loginUrl="https://ad.e.kuaishou.com//#/welcome?redirectUrl=https%3A%2F%2Fad.e.kuaishou.com%2F%23%2Findex"
        print(loginUrl)
        browser.get(loginUrl)
        #input account,pwd,code
        account = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[1]/input[1]')
        pwd     = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[2]/input[1]')
        login   = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]')
        

        account.send_keys(self.account)
        pwd.send_keys(self.pwd)
        login.click() 

        su.wait.time.sleep(3)

        if browser.current_url==loginUrl:
            su.wait.time.sleep(40)
            if browser.current_url==loginUrl:
                exit()
        
        #step2 
        # copy accoutid and get text from <p>   # 用get_attribute("innerHTML") 会返回元素的内部 HTML， 包含所有的HTML标签。
        accout_id=browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div/div/p[3]').get_attribute('textContent')
        nickname=browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div/div/p[2]').get_attribute('textContent')
        accout_id=accout_id.replace("账户ID：","").replace("复制","")
        nickname=nickname.replace("账户名：","").replace("修改","")

        print(accout_id,nickname)

        #step3 
        # make redirect url and json
        RedicUrl="https://ad.e.kuaishou.com/#/openapi/oauth?app_id=16&scope=%5B%22report_service%22%2C%22ad_manage%22%2C%22ad_query%22%5D&redirect_uri=http://feedsapi.adwintech.com/bridge/code&state="
        Newjson='{"create_user_id":'+self.userid+',"account_name":"'+self.account+'","account_pass":"'+self.pwd
        # Newjson=Newjson+',"test":"devp"'
        Newjson=Newjson+'","media":"kuaishou","adv_id":'+self.adv+',"account_nickname":"'+nickname+'"}'

        print(RedicUrl,Newjson)
        browser.get(RedicUrl+Newjson)
        su.wait.time.sleep(2)
        ConfirmButton= browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div[2]/button')
        ConfirmButton.click()

        su.wait.time.sleep(2)
        DoubConfirm=browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button[2]')
        DoubConfirm.click()

        su.wait.time.sleep(8)
        result=browser.find_element_by_xpath('/html/body/pre').get_attribute('textContent')
        
        #End the game
        if result.find("授权成功")>-1:
            print("success")
        else:
            print(result)

        browser.quit()



    def reg(self):
        jAd=str(sys.argv[2])
        ju=str(sys.argv[3])
        j1= str(sys.argv[4])
        j2= str(sys.argv[5])
        

        adv_reg= re.compile(':\d+,')
        user_reg= re.compile(':\d+,')
        phone_reg = re.compile('\d{11}')

        self.adv=re.search(adv_reg,jAd).group().replace(":","").replace(",","")
        self.userid=re.search(user_reg,ju).group().replace(":","").replace(",","")
        self.account = re.search(phone_reg,j1).group()
        self.pwd=j2
        print(self.adv,self.userid,self.account,self.pwd)
        pass



if __name__ == "__main__":

    a=NewADViewer()
    #a.reg()
    
    a.inputAccount()
    #a.ViewADWithNewViewer()
    li=gop.get_pid_from_name("chromedriver.exe")
    if len(li) > 0:
        for a in li:
            gop.kill(a)

    pass