import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


UnfID = []

def login(UnfID):
    Msg = "Approved"
    ID = ''.join(e for e in UnfID if e.isalnum())
    driver = webdriver.Chrome()
    driver.get ("https://sehat.perkeso.gov.my/v2/")
    driver.find_element_by_id("modlgn-username").send_keys("DCSEREMBAN1")
    driver.find_element_by_id ("modlgn-passwd").send_keys("BPSEREMBAN2019")
    driver.find_element_by_name("Submit").click()
    driver.find_element_by_class_name("item-711").click()
    driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/table/tbody/tr[2]/td[5]/a").click()
    driver.find_element_by_id("cb_ic").send_keys(ID)
    driver.find_element_by_xpath("//*[@id='adminForm']/div[3]/div[2]/div[2]/div/input").click()
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    status = soup.find("div",id="cbUserTable")
    div = soup.prettify("utf-8")
    if Msg in str(div):
        f= open("Parkeso.txt","a")
        f.write(ID + "   " + Msg + "\n")
        f.close
    else:
        f= open("Parkeso.txt","a")
        f.write(ID + "   " + "Not Approved" + "\n")
        f.close
    driver.close()
    driver.quit()

df = pd.read_csv("ICs.csv")
for idx in range(0,len(df.index)):         
    row = df.iloc[idx]
    UnfID = row['IDs'] 
    login(UnfID)
    
#def webcrawler():                  
    # autologin = {
    #      "username": "BPDCKLANG",
    #      "passwd": "BPDCKLANG1",
    #      "csrfmiddlewaretoken": "08b7407193dd9bff2c7d4f7850c6338a"
    #     }
    # session_requests = requests.session()
    # login_url = "https://sehat.perkeso.gov.my/v2/"
    # result = session_requests.get(login_url)
    # tree = html.fromstring(result.text)
    # authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    # result = session_requests.post(
    # login_url, 
    # data = autologin, 
    # headers = dict(referer=login_url)
    # )

    # for limit in range(0,120):
    #     url = "https://sehat.perkeso.gov.my/v2/list-all-patients.html?limitstart=" + str(limit)  
    #     time.sleep(random.randint(2,5))
    #     page = requests.get(url)                     
    #     soup = BeautifulSoup(page.text,"html.parser")
    #     tables = soup.findAll("table", class_='row no-gutters bg-light cbColumns sectiontableentry1 cbUserListRow')
    #     table=soup.prettify("utf-8")
    #     f= open("Parkeso.txt","a")
    #     f.write(table.decode('utf-8') + "\n\n\n\n")
    #     f.write(str(limit))
    #     f.close
    #     limit = limit+30    
#webcrawler()
