import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
from tkinter import *


def login(IDlist,user,pword):
    Msg = "Approved"
    Msg2 = "Mammogram"
    Msg3 = "You have yet to certify that the report is completed,"
    Msg4 = "Processing"
    Msg5 = "No users in this list"
    driver = webdriver.Chrome()
    driver.get ("https://sehat.perkeso.gov.my/v2/")
    driver.find_element_by_id("modlgn-username").send_keys(user)
    driver.find_element_by_id ("modlgn-passwd").send_keys(pword)
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
        if Msg in str(div):
            with open(r'Status.csv', 'a') as f:
                writer = csv.writer(f,lineterminator = '\n')
                row =["\'" + ID + "\'",Msg,"GREEN"]
                writer.writerow(row)
                f.close
        elif Msg5 in str(div):
            with open(r'Status.csv', 'a') as f:
                writer = csv.writer(f,lineterminator = '\n')
                row =["\'" + ID + "\'",Msg5]
                writer.writerow(row)
                f.close
        elif Msg3 in str(div):
            with open(r'Status.csv', 'a') as f:
                writer = csv.writer(f,lineterminator = '\n')
                row =["\'" + ID + "\'",Msg3,"BLUE"]
                writer.writerow(row)
                f.close
        elif Msg4 in str(div):
            with open(r'Status.csv', 'a') as f:
                writer = csv.writer(f,lineterminator = '\n')
                row =["\'" + ID + "\'",Msg4,"ORANGE"]
                writer.writerow(row)
                f.close
        else:
            with open(r'Status.csv', 'a') as f:
                writer = csv.writer(f,lineterminator = '\n')
                row =["\'" + ID + "\'","Not Approved"]
                writer.writerow(row)
                f.close
        if (str(div)).count(Msg2)>1:
            if Msg3 in str(div) or Msg4 in str(div):
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =["\'" + ID + "\'","One Test Not Approved"]
                    writer.writerow(row)
                    f.close
            else:
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =["\'" + ID + "\'","Both Tests Approved"]
                    writer.writerow(row)
                    f.close       
    driver.close()
    driver.quit()
    
user = ''
pword= ''

UnfID = []
IDlist = []
df = pd.read_csv("ICs.csv")
for idx in range(0,len(df.index)):         
    row = df.iloc[idx]
    UnfID.append(row['IDs'])
for IDx in UnfID:
    IDlist.append(''.join(e for e in IDx if e.isalnum()))
    
def show_entry_fields():
    print("Username: %s\nPassword: %s" % (e1.get(), e2.get()))

          
root = Tk()
Label(root, text="Outlet Username").grid(row=0)
Label(root, text="Outlet Password").grid(row=1)

e1=Entry(root)
e2=Entry(root)

e1.grid(row=0,column=1)
e2.grid(row=1,column=1)

def data(e1,e2):
    user = e1.get()
    pword = e2.get()
    print(user)
    print(pword)
    
    login(IDlist,user,pword)
    
Button(root,text="Generate", command = lambda: data(e1,e2)).grid(row=3,column=0,sticky=W,pady=4)
mainloop()
