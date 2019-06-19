import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import numpy as np
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
        if (str(div)).count(Msg2)>1:
            if Msg3 in str(div) or Msg4 in str(div):
                if (str(div).count(Msg3) > 1):
                    Status.append("BLUE")
                    Mammogram.append("BLUE")
                    with open(r'Status.csv', 'a') as f:
                        writer = csv.writer(f,lineterminator = '\n')
                        row =[ID,"Both Tests Not Approved"]
                        writer.writerow(row)
                        f.close
                elif (str(div).count(Msg4) > 1):
                    Status.append("ORANGE")
                    Mammogram.append("ORANGE")
                    with open(r'Status.csv', 'a') as f:
                        writer = csv.writer(f,lineterminator = '\n')
                        row =[ID,"Both Tests Not Approved"]
                        writer.writerow(row)
                        f.close
                else:
                    status2 = soup.find_all("div", class_="row no-gutters bg-light cbColumns sectiontableentry1 cbUserListRow")
                    patDesc = ""
                    patColor = ""
                    statusColor = ""
                    mammogramColor = ""
                    isStatus = False
                    isMammogram = False
                    if "cbUserListFieldLine cbUserListFL_cb_mammogramindicator" in str(status2):
                        if Msg in str(status2):
                            #Status.append("BLUE")
                            #Mammogram.append("GREEN")
                            patDesc = "PSEKOM"
                            patColor = "GREEN"
                            mammogramColor = "GREEN"
                            isMammogram = True
                        elif Msg3 in str(status2):
                            #Status.append("BLUE")
                            #Mammogram.append("BLUE")
                            patDesc = "PSEKOM"
                            patColor = "BLUE"
                            mammogramColor = "BLUE"
                            isMammogram = True
                        elif Msg4 in str(status2):
                            #Status.append("ORANGE")
                            #Mammogram.append("ORANGE")
                            patDesc = "PSEKOM"
                            patColor = "ORANGE"
                            mammogramColor = "ORANGE"
                            isMammogram = True
                    else:
                        if Msg in str(status2):
                            #Status.append("GREEN")
                            #Mammogram.append("N\A")
                            patDesc = "N\A"
                            patColor = "GREEN"
                            statusColor = "GREEN"
                            isStatus = True
                        elif Msg3 in str(status2):
                            #Status.append("BLUE")
                            #Mammogram.append("N\A")
                            patDesc = "N\A"
                            patColor = "BLUE"
                            statusColor = "BLUE"
                            isStatus = True
                        elif Msg4 in str(status2):
                            #Status.append("ORANGE")
                            #Mammogram.append("N\A")
                            patDesc = "N\A"
                            patColor = "ORANGE"
                            statusColor = "ORANGE"
                            isStatus = True
                    status2 = soup.find("div", class_="row no-gutters bg-light cbColumns sectiontableentry2 cbUserListRow")
                    if "cbUserListFieldLine cbUserListFL_cb_mammogramindicator" in str(status2):
                        if Msg in str(status2):
                            #Status.append("GREEN")
                            #Mammogram.append("GREEN")
                            patDesc = patDesc + "^PSEKOM"
                            patColor = patColor + "GREEN"
                            mammogramColor = "GREEN"
                            isMammogram = True
                        elif Msg3 in str(status2):
                            #Status.append("BLUE")
                            #Mammogram.append("BLUE")
                            patDesc = patDesc + "^PSEKOM"
                            patColor = patColor + "BLUE"
                            mammogramColor = "BLUE"
                            isMammogram = True
                        elif Msg4 in str(status2):
                            #Status.append("ORANGE")
                            #Mammogram.append("ORANGE")
                            patDesc = patDesc + "^PSEKOM"
                            patColor = patColor + "ORANGE"
                            mammogramColor = "ORANGE"
                            isMammogram = True
                    else:
                        if Msg in str(status2):
                            #Status.append("GREEN")
                            #Mammogram.append("N\A")
                            patDesc = patDesc + "^N\A"
                            patColor = patColor + "GREEN"
                            statusColor = "GREEN"
                            isStatus = True
                        elif Msg3 in str(status2):
                            #Status.append("BLUE")
                            #Mammogram.append("N\A")
                            patDesc = patDesc + "^N\A"
                            patColor = patColor + "BLUE"
                            statusColor = "BLUE"
                            isStatus = True
                        elif Msg4 in str(status2):
                            #Status.append("ORANGE")
                            #Mammogram.append("N\A")
                            patDesc = patDesc + "^N\A"
                            patColor = patColor + "ORANGE"
                            statusColor = "ORANGE"
                            isStatus = True
                    with open(r'Status.csv', 'a') as f:
                        writer = csv.writer(f,lineterminator = '\n')
                        row =[ID,patDesc,patColor]
                        writer.writerow(row)
                        f.close
                    if isStatus == True and isMammogram == False:
                        Status.append(statusColor)
                        Mammogram.append("N\A")
                    elif isStatus == False and isMammogram == True:
                        Status.append("N\A")
                        Mammogram.append(mammogramColor)
                    else:
                        Status.append(statusColor)
                        Mammogram.append(mammogramColor)
            else:
                Status.append("GREEN")
                Mammogram.append("GREEN")
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,"Both Tests Approved"]
                    writer.writerow(row)
                    f.close
        else:
            if Msg in str(div):
                Status.append("GREEN")
                Mammogram.append("N\A")
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg,"GREEN"]
                    writer.writerow(row)
                    f.close
                    print(Status)
            elif Msg5 in str(div):
                Status.append("Not Found")
                Mammogram.append("Not Found")
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg5]
                    writer.writerow(row)
                    f.close
            elif Msg3 in str(div):
                Status.append("BLUE")
                Mammogram.append("N\A")
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg3,"BLUE"]
                    writer.writerow(row)
                    f.close
            elif Msg4 in str(div):
                Status.append("ORANGE")
                Mammogram.append("N\A")
                with open(r'Status.csv', 'a') as f:
                    writer = csv.writer(f,lineterminator = '\n')
                    row =[ID,Msg4,"ORANGE"]
                    writer.writerow(row)
                    f.close

    driver.close()
    driver.quit()
    return Status,Mammogram
    
user = ''
pword= ''
UnfID = []
IDlist = []
Status= []
Mammogram= []


root = Tk()
root.geometry("300x130")
root.title("VoucherSort")
root.resizable(False, False)

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))


Label(root, text="Outlet Name").grid(row=0, column =0, padx= (0,100) ,pady=35)


e1=Entry(root)

e1.grid(row=0, padx = (130,0))

    
def login_dets(e2,e3):
    df = pd.read_csv(Branch + ".csv")
    for idx in range(0,len(df.index)):         
        row = df.iloc[idx]
        UnfID.append(row['ic_no'])
    for IDx in UnfID:
        IDlist.append(''.join(e for e in IDx if e.isalnum()))
    user = e2.get()
    pword = e3.get()
    login(IDlist,user,pword)
    df["Tests"] = pd.Series(Status)
    df["Mammogram"] = pd.Series(Mammogram)
    df.to_excel(Branch + ".xlsx")

  
def command():
    root2 = Tk()
    root2.geometry("300x150")
    root2.title("VoucherSort")
    root2.resizable(False, False)
    
    windowWidth = root2.winfo_reqwidth()
    windowHeight = root2.winfo_reqheight()
    positionRight = int(root2.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root2.winfo_screenheight()/2 - windowHeight/2)
    root2.geometry("+{}+{}".format(positionRight, positionDown))
    
    Label(root2, text="Outlet Username").grid(row=1, padx = (0,100), pady=15)
    Label(root2, text="Outlet Password").grid(row=2, padx = (0,100), pady=5)


    e2=Entry(root2)
    e3=Entry(root2)


    e2.grid(row=1,padx=(130,0))
    e3.grid(row=2,padx=(130,0))

    Button(root2,text="Generate", width=10, command = lambda: login_dets(e2,e3)).grid(row=5,column=0,sticky=W,padx = (50,0), pady=15)
    Button(root2,text="Close", width=10, command = root2.destroy).grid(row=5,sticky=W,padx=(170,0))
    mainloop()
    


def outlet_name(e1):
    global Branch
    Branch = e1.get()
    DFx = pd.read_csv("Perkeso2016.csv")
    ExtDF = DFx[DFx['branch']== Branch]
    ExtDF.to_csv(Branch + ".csv")

def branch_get():
    Button(root,text="Confirm", width=10, command = lambda: outlet_name(e1)).grid(sticky=W, padx=(50,0))
    Button(root,text="Next", width=10, command = lambda: command()).grid(row =1,sticky=W, padx=(170,0))
    mainloop()

branch_get()

def show_entry_fields():
    print("Username: %s\nPassword: %s" % (e1.get(), e2.get()))


