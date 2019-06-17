import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv



def login(IDlist):
    Msg = "Approved"
    Msg2 = "Mammogram"
    Msg3 = "You have yet to certify that the report is completed,"
    Msg4 = "Processing"
    Msg5 = "No users in this list"
    driver = webdriver.Chrome()
    driver.get ("https://sehat.perkeso.gov.my/v2/")
    driver.find_element_by_id("modlgn-username").send_keys("DCSJ")
    driver.find_element_by_id ("modlgn-passwd").send_keys("BPDCSUBANGJAYA")
    driver.find_element_by_name("Submit").click()
    driver.find_element_by_class_name("item-711").click()
    driver.find_element_by_xpath("//*[@id='content']/div[2]/div[2]/table/tbody/tr[2]/td[5]/a").click()
    for ID in IDlist:
        driver.get ("https://sehat.perkeso.gov.my/v2/component/comprofiler/userslist/9-my-patients-search-patients/search.html")
        driver.find_element_by_id("cb_ic").send_keys(ID)
        driver.find_element_by_xpath("//*[@id='adminForm']/div[3]/div[2]/div[2]/div/input").click()
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        status = soup.find("div",id="cbUserTable")
        div = soup.prettify("utf-8")
        print((str(div)).count(Msg2))
        if (str(div)).count(Msg2)>1:
            if Msg3 in str(div) or Msg4 in str(div):
                if (str(div).count(Msg3) > 1) or (str(div).count(Msg4) > 1):
                    with open(r'Status.csv', 'a') as f:
                        writer = csv.writer(f,lineterminator = '\n')
                        row =[ID,"Both Tests Not Approved"]
                        writer.writerow(row)
                        f.close
                else:
                    status2 = soup.find_all("div", class_="row no-gutters bg-light cbColumns sectiontableentry1 cbUserListRow")
                    if "cbUserListFieldLine cbUserListFL_cb_mammogramindicator" in str(status2):
                        if Msg in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg,"GREEN"]
                                writer.writerow(row)
                                f.close
                        elif Msg3 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg3,"BLUE"]
                                writer.writerow(row)
                                f.close
                        elif Msg4 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg4,"ORANGE"]
                                writer.writerow(row)
                                f.close
                    else:
                        if Msg in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg,"GREEN"]
                                writer.writerow(row)
                                f.close
                        elif Msg3 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg3,"BLUE"]
                                writer.writerow(row)
                                f.close
                        elif Msg4 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg4,"ORANGE"]
                                writer.writerow(row)
                                f.close
                    status2 = soup.find("div", class_="row no-gutters bg-light cbColumns sectiontableentry2 cbUserListRow")
                    if "cbUserListFieldLine cbUserListFL_cb_mammogramindicator" in str(status2):
                        if Msg in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg,"GREEN"]
                                writer.writerow(row)
                                f.close
                        elif Msg3 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg3,"BLUE"]
                                writer.writerow(row)
                                f.close
                        elif Msg4 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,"PKESOM",Msg4,"ORANGE"]
                                writer.writerow(row)
                                f.close
                    else:
                        if Msg in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg,"GREEN"]
                                writer.writerow(row)
                                f.close
                        elif Msg3 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg3,"BLUE"]
                                writer.writerow(row)
                                f.close
                        elif Msg4 in str(status2):
                            with open(r'Status.csv', 'a') as f:
                                writer = csv.writer(f,lineterminator = '\n')
                                row =[ID,Msg4,"ORANGE"]
                                writer.writerow(row)
                                f.close
            else:
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,"Both Tests Approved"]
                    writer.writerow(row)
                    f.close
        else:
            if Msg in str(div):
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg,"GREEN"]
                    writer.writerow(row)
                    f.close
            elif Msg5 in str(div):
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg5]
                    writer.writerow(row)
                    f.close
            elif Msg3 in str(div):
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg3,"BLUE"]
                    writer.writerow(row)
                    f.close
            elif Msg4 in str(div):
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg4,"ORANGE"]
                    writer.writerow(row)
                    f.close
               
    driver.close()
    driver.quit()

UnfID = []
IDlist = []
df = pd.read_csv("ICs.csv")
for idx in range(0,len(df.index)):         
    row = df.iloc[idx]
    UnfID.append(row['IDs'])
for IDx in UnfID:
    IDlist.append(''.join(e for e in IDx if e.isalnum()))
login(IDlist)
    
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
