
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
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

# consider automating for it to scroll through yahoo singapore and skip sponsored post and select news link
# use this element to differentiate out news from sponsored
# --> <div class="Fz(12px) Fw(b) Tt(c) D(ib) Mb(6px) C($c-fuji-news) Mend(9px) Mt(-2px)" data-test-locator="catlabel" data-reactid="11">News</div>

websites = ["https://sg.news.yahoo.com/e-scooter-rider-jailed-bedok-accident-consuming-drugs-bail-091840268.html",
            "https://sg.news.yahoo.com/four-drivers-fined-providing-illegal-chauffeured-services-unlicensed-vehicles-071542451.html",
            "https://sg.news.yahoo.com/hiv-data-leak-affected-patients-can-sue-moh-loss-data-says-gan-kim-yong-090625320.html",
            "https://sg.news.yahoo.com/american-behind-hiv-data-leak-pathological-liar-made-baseless-allegations-singapore-authorities-130957980.html",
            "https://sg.news.yahoo.com/prosecution-seeks-preventive-detention-recalcitrant-paedophile-57-sexually-assaulted-boy-122307488.html",
            "https://sg.news.yahoo.com/73-year-old-driver-jailed-assaulting-trying-bribe-traffic-cop-132421761.html",
            "https://sg.news.yahoo.com/cannabis-stay-illegal-proven-cannabinoid-medical-products-may-allowed-mha-moh-075514549.html",
            "https://sg.news.yahoo.com/jailed-accountant-embezzled-2-million-bought-two-homes-074249110.html",
            "https://sg.news.yahoo.com/ava-review-rules-governing-pet-boarding-businesses-sun-xueling-072603250.html",
            "https://sg.news.yahoo.com/record-high-visitor-arrivals-modest-increase-tourism-spending-singapore-2018-065117991.html",
            "https://sg.news.yahoo.com/islandwide-siren-sound-15-feb-commemorate-total-defence-day-044136885.html",
            "https://sg.news.yahoo.com/muhammad-jaris-goh-leads-accolades-singapore-mens-bowling-team-annual-awards-021447862.html",
            "https://sg.news.yahoo.com/yahoo-poll-enforcement-indiscriminate-burning-hdb-flats-230132255.html",
            "https://sg.news.yahoo.com/man-found-unconscious-drugs-near-crotch-acquitted-appeal-121247684.html",
            "https://sg.news.yahoo.com/comment-e-cigarettes-harm-reduction-not-elimination-aim-public-health-policy-111956884.html",
            "https://sg.news.yahoo.com/cyberattacks-cost-large-asia-pacific-healthcare-groups-average-32-million-study-100129697.html",
            "https://sg.news.yahoo.com/man-jailed-cheating-girlfriend-mother-nearly-180000-gamble-093652802.html",
            "https://sg.news.yahoo.com/hiv-data-leak-affected-patients-reportedly-feeling-suicidal-gan-kim-yong-082316256.html",
            "https://sg.news.yahoo.com/hiv-data-leak-agc-not-charge-brochez-osa-2016-faced-light-sentence-081539862.html",
            "https://sg.news.yahoo.com/hdb-launches-first-2019-sales-exercise-3739-flats-070237119.html",
            "https://sg.news.yahoo.com/jailed-man-posted-ex-lovers-contact-information-fake-online-sex-ad-035031208.html",
            "https://sg.news.yahoo.com/erp-charges-three-gantries-removed-peak-morning-hours-125315512.html",
            "https://sg.news.yahoo.com/singaporean-man-jailed-7-weeks-evading-ns-3-years-121420970.html",
            "https://sg.news.yahoo.com/proposal-decriminalise-attempted-suicide-tabled-parliament-part-penal-code-changes-115816274.html",
            "https://sg.news.yahoo.com/singaporeans-enjoy-automated-immigration-clearance-new-zealand-110947897.html",
            "https://sg.news.yahoo.com/singpost-received-91-complaints-misdelivered-lost-mail-2018-sim-ann-100946217.html",
            "https://sg.news.yahoo.com/couple-abused-maid-made-drink-tainted-water-jailed-090017797.html",
            "https://sg.news.yahoo.com/moe-increase-examinations-using-electronic-devices-ong-ye-kung-073158540.html",
            "https://sg.news.yahoo.com/parliament-new-saf-safety-measures-include-rear-view-cameras-bionix-vehicles-070546098.html",
            "https://sg.news.yahoo.com/nsf-liu-kais-death-bionix-driver-not-hear-commands-stop-060336184.html",
            "https://sg.news.yahoo.com/death-aloysius-pang-two-saf-personnel-vehicle-time-incident-similarly-qualified-045405681.html",
            "https://sg.news.yahoo.com/malaysian-government-vessel-greek-carrier-collide-within-singapore-waters-045603597.html",
            "https://sg.news.yahoo.com/burning-smell-eastern-part-singapore-not-caused-local-sources-no-haze-detected-nea-130031817.html",
            "https://sg.news.yahoo.com/conman-jailed-14-months-multiple-scams-involving-55000-105558452.html",
            "https://sg.news.yahoo.com/questions-saf-training-deaths-dominate-parliament-sitting-monday-082434673.html",
            "https://sg.news.yahoo.com/tea-good-heres-experts-say-064739635.html",
            "https://sg.news.yahoo.com/singpost-improve-service-standards-fined-100k-lapses-011717663.html",
            "https://sg.news.yahoo.com/yahoo-poll-feel-trump-kim-summit-held-vietnam-230034819.html"]

###################################################   

comments_list =[]

wait_time = WebDriverWait(driver, 20)

for i in websites:
    driver.get(i)
    
    # click View Reaction button
    #viewreact_button = driver.find_element_by_xpath("//button[@class='comments-title D(ib) Td(n) Bd(0) P(0) Fw(b) Fz(16px) Cur(p) C(#000)']").click()
    viewreact_button = wait_time.until(EC.visibility_of_element_located((By.XPATH,"//button[@class='comments-title D(ib) Td(n) Bd(0) P(0) Fw(b) Fz(16px) Cur(p) C(#000)']")))
    viewreact_button.click()
    
    # keep clicking the Show More button to the end
    # tries to ignore StaleElementReferenceException and TimeOutException
    while True:
        try: 
            more_button = wait_time.until(EC.visibility_of_element_located((By.XPATH,"//button[@class='Ff(ss) Fz(14px) Fw(b) Bdw(2px) Ta(c) Cur(p) Va(m) Bdrs(4px) O(n)! Lh(n) Bgc(#fff) C($c-fuji-blue-1-a) Bdc($c-fuji-blue-1-a) Bd C(#fff):h Bgc($c-fuji-blue-1-a):h Mt(20px) Mb(20px) Px(30px) Py(10px) showNext D(b) Mx(a) Pos(r)']")))
            more_button.click()
        except Exception:
            break

    # find the comments
    comments = wait_time.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)']")))
    for j in comments:
        comments_list.append(j.text)
    print(i + " completed")

###################################################        

#print(comments_list)

df2 = pd.DataFrame(comments_list, columns=['Comments'])
#print(df2)

df2.to_csv("Scraped_Yahoo_Comments.csv", index=False)
print("Scraped completed")
    
driver.close()

