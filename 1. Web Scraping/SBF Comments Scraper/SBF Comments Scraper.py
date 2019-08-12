
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
class TimeoutException(Exception): pass
import pandas as pd

###################################################   

# make chrome incognito and headless to run faster
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_argument('--headless')

# change the driver_path to wherever your webdriver is located
driver_path = "C:/Users/Quan Hao/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# go to SammyBoyForum
driver.get("https://www.sammyboy.com/#welcome-to-sams-alfresco-coffee-shop.1")

# #get a list of topics
topics_list = []
topic_link = driver.find_elements_by_xpath("//*[contains(@data-shortcut,'node-description')][contains(@id,'js-XFUniqueId')]")
for f in topic_link:
    topics_list.append(f.get_attribute("href"))
#print(topics_list)

###################################################  

#number of pages in a topic to crawl
pages = 2

threads_list = []
for r in topics_list:
    driver.get(r)
    # get a list of threads from each topic
    while True:
        try:
            # find the thread links
            thread_link = driver.find_elements_by_xpath("//*[contains(@data-xf-init, 'preview-tooltip')][contains(@id,'js-XFUniqueId')]")
            for k in thread_link:
                threads_list.append(k.get_attribute("href"))

            #keeps clicking the Next button till specified page limit
            count = 0
            while True:
                topic_next_button = driver.find_element_by_xpath("//*[contains(@class,'pageNav-jump--next')]")
                topic_next_button.send_keys(webdriver.common.keys.Keys.RETURN)
                count+=1
                if (count > page):
                    break
        except Exception:
            break
#print(threads_list)

###################################################  

posts_list =[]
wait_time = WebDriverWait(driver, 15)
for i in threads_list:
    driver.get(i)
    while True:
        try:
            #find the posts
            posts = driver.find_elements_by_xpath("//div[contains(@class,'bbWrapper')]")
            for j in posts:
                posts_list.append(j.text)

            #keeps clicking the Next button to the end
            thread_next_button = driver.find_element_by_xpath("//*[contains(@class,'pageNav-jump--next')]")
            thread_next_button.send_keys(webdriver.common.keys.Keys.RETURN)
        except Exception:
            break
#print(posts_list)
            
###################################################

df = pd.DataFrame(topics_list, columns=['Topic'])
#print(df)

df1 = pd.DataFrame(threads_list, columns=['Thread Title'])
#print(df1)

df2 = pd.DataFrame(posts_list, columns=['Posts'])
#print(df2)

df2.to_csv("Scraped_SBF_Comments.csv", index=False)
print("Scraped completed")

driver.close()

