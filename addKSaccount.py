import sys
import requests
import re
import hashlib

from selenium import webdriver
import selenium.webdriver.support as su
import selenium.webdriver.common as cm
import selenium.webdriver.common.by as By
import getOSpid as gop

class NewADViewer:

    loginUrl="https://ad.e.kuaishou.com//#/welcome?redirectUrl=https%3A%2F%2Fad.e.kuaishou.com%2F%23%2Findex"
    subAccUrl="https://uc.e.kuaishou.com/?sid=kuaishou.ad.dsp&followUrl=https%3A%2F%2Fad.e.kuaishou.com%2F#/index"


    adv= "427" 
    userid= "237" 
    account="1355***151"
    pwd="Dee***999"
    subname=""
    subid=""

    def login(self,browser):
      
        browser.get(self.loginUrl)
        #input account,pwd,code
        account = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[1]/input[1]')
        pwd     = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/form/div[2]/input[1]')
        login   = browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]')
        

        account.send_keys(self.account)
        pwd.send_keys(self.pwd)
        login.click() 
        
    #def logout(self,browser):



    def handleAccounts(self):
        # http://chromedriver.storage.googleapis.com/index.html  install chrome driver
        #self.reg()
        #disable info bar
        option=webdriver.ChromeOptions()
        option.add_argument('--start-maximized')
        option.add_argument('--disable-infobars')
        #option.add_argument('allow-running-insecure-content')

        browser1=webdriver.Chrome(options=option)
        self.login(browser1)
        #su.wait.time.sleep(7)

        if browser1.current_url==self.loginUrl:
            su.wait.time.sleep(40)
            if browser1.current_url==self.loginUrl:
                print("Time out on redirect")
                exit()
            elif browser1.current_url==self.subAccUrl:  #子账户中间页面
                self.handleSubchoice(browser1)
            else:
                self.getApproval(browser1)
        
        browser1.quit()

    def handleSubchoice(self,browser):
        #//*[@id="app"]/div/div[2]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/a
        #//*[@id="app"]/div/div[2]/div/div[2]/div/div/div/div/div/div/table/tbody/tr[3]/td[3]/a
        e=browser.find_elements(by=By.By.LINK_TEXT,value='进入')#xpath("//a[contains(text(), '进入')]"))
        count=len(e)
        succmap={}
        print("子账户数量为:",count)
        for i in range(1,count+1):
            hyper=browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[3]/a')
            hyper.click()
            su.wait.time.sleep(10)
            self.getApproval(browser)
            browser.back()
            browser.back()
            browser.back()
            su.wait.time.sleep(5)  
            succmap[self.subid]=self.subname

        for key,value in succmap.items():
            print("子账户",key,value,"添加成功")         




    def getApproval(self,browser):
        #step2 
        # copy accoutid and get text from <p>   # 用get_attribute("innerHTML") 会返回元素的内部 HTML， 包含所有的HTML标签。
        accout_id=browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div/div/p[3]').get_attribute('textContent')
        nickname=browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div[2]/div/div/p[2]').get_attribute('textContent')
        accout_id=accout_id.replace("账户ID：","").replace("复制","")
        nickname=nickname.replace("账户名：","").replace("修改","")

        print(accout_id,nickname)
        self.subid=accout_id
        self.subname=nickname

        #step3 
        # make redirect url and json
        RedicUrl="https://ad.e.kuaishou.com/#/openapi/oauth?app_id=16&scope=%5B%22report_service%22%2C%22ad_manage%22%2C%22ad_query%22%5D&redirect_uri=http://feedsapi.adwintech.com/bridge/code&state="
        Newjson='{"create_user_id":'+self.userid+',"account_name":"'+self.account+'","account_pass":"'+self.pwd+'"'
        Newjson=Newjson+',"test":"devp"'
        Newjson=Newjson+',"media":"kuaishou","adv_id":'+self.adv+',"account_nickname":"'+nickname+'"}'

        print(RedicUrl,Newjson)
        browser.get(RedicUrl+Newjson)
        su.wait.time.sleep(2)
        ConfirmButton= browser.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/div[2]/button')
        ConfirmButton.click()
        #action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()  # ctrl+a   

        su.wait.time.sleep(2)
        DoubConfirm=browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button[2]')
        DoubConfirm.click()

        su.wait.time.sleep(8)
        result=browser.find_element_by_xpath('/html/body/pre').get_attribute('textContent')
        
        #End the game
        if result.find("授权成功")>-1:
            print(self.subid+" added success")
        else:
            print(result)



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

    li=gop.get_pid_from_name("chromedriver.exe")
    if len(li) > 0:
        for a in li:
            gop.kill(a)

    a=NewADViewer()
    
    a.handleAccounts()
   

    pass