from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib import request
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Xuexi():

    def __catch_web0(self):
        driver=webdriver.PhantomJS()
        driver.get("https://www.xuexi.cn/")
        html_01=driver.page_source
        html_01=BeautifulSoup(html_01,"html.parser")
        html_01=html_01.find_all('a',{'target':'_blank'})
        html_0=[]    #该变量为首页地址，第一个为文汇，第二个为学习电视台
        html_0.append(html_01[1]['href'])
        html_0.append(html_01[3]['href'])
        driver.quit()
        return html_0

    def __catch_wenhuiweb1(self,html_0):    #爬取文汇类前5个链接，每个链接下还有链接
        driver=webdriver.PhantomJS()
        driver.get(html_0[0])
        elements=driver.find_elements_by_class_name('word-item')
        html_1=[]
        for i in range(5,9):
            driver.switch_to_window(driver.window_handles[0])
            elements[i].click()
            driver.switch_to_window(driver.window_handles[1])
            html_111=driver.current_url
            driver.close()
            html_1.append(html_111)
        driver.quit()
        return html_1
    
    # def __catch_wenhuiweb2(self,html_11):    #爬取文汇类前5个链接的末级链接
    #     html_1=[]
    #     for abc in html_11:
    #         driver=webdriver.PhantomJS()
    #         driver.get(abc)
    #         elements=driver.find_elements_by_class_name('word-item')
    #         for i in range(5):
    #             driver.switch_to_window(driver.window_handles[0])
    #             elements[i].click()
    #             driver.switch_to_window(driver.window_handles[1])
    #             html_111=driver.current_url
    #             driver.close()
    #             html_1.append(html_111)
    #         driver.quit()
    #     return html_1




    def __videoweb(self,html_0):
        driver=webdriver.PhantomJS()
        driver.get(html_0[1])
        element=driver.find_element_by_xpath("//div[contains(text(),'重要活动视频专辑')]")
        element.click()
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        html_2=driver.current_url      
        driver.quit()
        return html_2

    def __readwenhui(self,html_1,driver):
        for url in html_1:
            driver.get(url)
            elements=driver.find_elements_by_class_name('word-item')
            for x in elements:
                x.click()
                driver.switch_to_window(driver.window_handles[1])
                element=driver.find_element_by_class_name('dyxx-rich-content')
                size1=element.size
                print(size1)
                height=size1['height']
                for i in range(height+100):
                    driver.execute_script('window.scrollTo(0,'+str(i)+')')
                    time.sleep(120/height)
                    element.click()
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
        return

    def __watchvideo(self, html_2, driver):
        driver.get(html_2)
        element=driver.find_element_by_xpath("//label[contains(text(),'重要活动视频专辑')]")
        element.click()
        elements = driver.find_elements_by_class_name('word-item')
        url_chongfu = []
        for i in elements:
            i.click()
            driver.switch_to_window(driver.window_handles[1])
            time.sleep(3)
            url_hongfu1 = driver.current_url
            if url_hongfu1 in url_chongfu:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
            else:
                html = driver.page_source
                html = BeautifulSoup(html, "html.parser")
                video_time = html.find_all('span', {'class': 'duration'})
                driver.execute_script('window.scrollTo(0,500)')
                if video_time is None:
                    video_time='03:01'
                else:
                    video_time = video_time[0].get_text()
                element=driver.find_element_by_class_name('prism-player')
                element.click()
                # element=driver.find_element_by_class_name('outter')
                # element.click()
                stop_time = int(video_time[0:2])*60+int(video_time[-2:])+5
                time.sleep(stop_time)
                url_chongfu.append(url_hongfu1)
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
        element = driver.find_element_by_xpath("//li[contains(text(),'2')]")
        element.click()
        elements = driver.find_elements_by_class_name('word-item')
        for i in elements:
            i.click()
            driver.switch_to_window(driver.window_handles[1])
            url_hongfu1 = driver.current_url
            if url_hongfu1 in url_chongfu:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
            else:
                html = driver.page_source
                html = BeautifulSoup(html, "html.parser")
                video_time = html.find_all('span', {'class': 'duration'})
                driver.execute_script('window.scrollTo(0,500)')
                if video_time is None:
                    video_time='03:01'
                else:
                    video_time = video_time[0].get_text()
                element=driver.find_element_by_class_name('prism-player')
                element.click()
                # element=driver.find_element_by_class_name('outter')
                # element.click()
                stop_time = int(video_time[0:2])*60+int(video_time[-2:])+5
                time.sleep(stop_time)
                url_chongfu.append(url_hongfu1)
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
        return

    def __login(self,driver):
        isExists=os.path.exists('./pythonlogin')
        if not isExists:
            os.makedirs('./pythonlogin') 
        driver.get('https://pc.xuexi.cn/points/login.html')
        driver.execute_script('window.scrollTo(0,1000)')
        driver.save_screenshot('./pythonlogin/erweima.png')   #截图
        # img=Image.open('/pythonlogin/erweima.png')  #打开截图
        # img.show()
        return


    def __send(self):
        sender = '28@qq.com'
        receivers = '2@qq.com'
        message =  MIMEMultipart('related')
        subject = '终于能发图片了'
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receivers
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
        message.attach(content)

        file=open("/pythonlogin/erweima.png", "rb")
        img_data = file.read()
        file.close()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)

        try:
            server=smtplib.SMTP_SSL("smtp.qq.com",465)
            server.login(sender,"2")
            server.sendmail(sender,receivers,message.as_string())
            server.quit()
            print ("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
        
        return

    def go(self): 
        driver=webdriver.Chrome()
        self.__login(driver)
        # self.__send()   #发送二维码邮件
        time.sleep(5)
        html_0=self.__catch_web0()
        html_2=self.__videoweb(html_0)    #视频类链接完成
        self.__watchvideo(html_2,driver)
        html_1=self.__catch_wenhuiweb1(html_0)  #文汇类链接完成
        self.__readwenhui(html_1,driver)
       
        
       
        
        driver.quit()



       
        




xuexi=Xuexi()
xuexi.go()
