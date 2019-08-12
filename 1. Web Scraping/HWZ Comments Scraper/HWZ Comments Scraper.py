
# coding: utf-8

# In[95]:


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
options.add_argument('--headless')

# change the driver_path to wherever your webdriver is located
driver_path = "C:/Users/Quan Hao/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# go to HardWareZone website
driver.get("https://forums.hardwarezone.com.sg/eat-drink-man-woman-16/")

threads_list = []

# get a list of threads
while True:
    try:
        # find the thread links
        thread_link = driver.find_elements_by_xpath("//*[contains(@id,'thread_title_')]")
        for k in thread_link:
            threads_list.append(k.get_attribute("href"))
            
        #keeps clicking the Next button to the end
        count = 0
        while count < 4:
            next_button = wait_time.until(EC.visibility_of_element_located((By.XPATH,"//*[contains(@title,'Next Page - Results')]")))
            next_button.send_keys(webdriver.common.keys.Keys.RETURN)
            count+=1
    except Exception:
        break

# websites = ['https://forums.hardwarezone.com.sg/eat-drink-man-woman-16/sinkie-aunty-buy-2nd-hand-expect-customer-service-tio-suan-5992451.html',
#             'https://forums.hardwarezone.com.sg/eat-drink-man-woman-16/do-you-remove-your-ring-when-you-going-eat-cheekon-5992476.html']

###################################################   

posts_list =[]

wait_time = WebDriverWait(driver, 15)

for i in threads_list:
    driver.get(i)
    
    while True:
        try:
            #find the comments
            #posts = driver.find_elements_by_xpath("//*[contains(@id,'post_message_')]")
            posts = driver.find_elements_by_xpath("//div[contains(@class,'post_message')]")
            #posts = wait_time.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id,'post_message_')]")))
            for j in posts:
                posts_list.append(j.text)

            #keeps clicking the Next button to the end
            next_button = wait_time.until(EC.visibility_of_element_located((By.XPATH,"//*[contains(@title,'Next Page - Results')]")))
            next_button.send_keys(webdriver.common.keys.Keys.RETURN)
        except Exception:
            break

###################################################        

posts_list2 =[]
for i in posts_list:
    t = i.replace('\n','')
    posts_list2.append(t)
#print(posts_list2)

df = pd.DataFrame(posts_list2, columns=['Thread Title'])
#print(df)

df.to_csv("Scraped_HWZ_Comments.csv", index=False)
print("Scraped completed")

driver.close()

