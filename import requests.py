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
from tkinter import messagebox
from pandas.io.excel import ExcelWriter
import os
import glob
from xlsxwriter.workbook import Workbook

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
flag = 0


root = Tk()
root.geometry("300x150")
root.title("VoucherSort")
root.resizable(False, False)

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry("+{}+{}".format(positionRight, positionDown))


Label(root, text="Outlet Name").grid(row=1, padx = (0,100), pady=15)
Label(root, text="File Name").grid(row=2, padx = (0,100), pady=5)


e1=Entry(root)
e2=Entry(root)

e1.grid(row=1,padx=(130,0))
e2.grid(row=2,padx=(130,0))


    
def login_dets(e3,e4):
    destroy_windows()
    df = pd.read_csv(Branch + ".csv")
    for idx in range(0,len(df.index)):         
        row = df.iloc[idx]
        UnfID.append(row['ic_no'])
    for IDx in UnfID:
        IDlist.append(''.join(e for e in IDx if e.isalnum()))
    user = e3.get()
    pword = e4.get()
    if user=='' or pword=='':
        messagebox.showerror('Error', 'Please fill in both Username and Password')
    else:
        login(IDlist,user,pword)
        df["Tests"] = pd.Series(Status)
        df["Mammogram"] = pd.Series(Mammogram)
        df.to_excel(Branch + ".xlsx")

def destroy_windows():
    root.destroy()
  
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


    e3=Entry(root2)
    e4=Entry(root2)

    e3.grid(row=1,padx=(130,0))
    e4.grid(row=2,padx=(130,0))

    Button(root2,text="Generate", width=10, command = lambda: login_dets(e3,e4)).grid(row=5,column=0,sticky=W,padx = (50,0), pady=15)
    Button(root2,text="Close", width=10, command = root2.destroy).grid(row=5,sticky=W,padx=(170,0))
    mainloop()
    


def outletFile_name(e1,e2):
    global Branch
    global File
    global flag
    Branch = e1.get()
    File = e2.get()
    FileFlag=0
    if Branch=='' or File=='':
        messagebox.showerror('Error', 'Please fill in both Branch name and File name')
    else:
        try:
            DFx = pd.read_csv(File + ".csv")
            FileFlag=1
        except:
            messagebox.showerror('Error', File + ' Not Found !!')
            branch_get()
        if FileFlag==1:
            ExtDF = DFx[DFx['branch']== Branch]
            ExtDF.to_csv(Branch + ".csv", index = False)
            flag = 1
            next()
        else:
            branch_get()

def branch_get():
    Button(root,text="Confirm", width=10, command = lambda: outletFile_name(e1,e2)).grid(row=5,column=0,sticky=W,padx = (50,0), pady=15)
    mainloop()

def next():
    print(flag)
    if (flag==1):
        Button(root,text="Next", width=10, command = lambda: command()).grid(row=5,sticky=W,padx=(170,0))
        mainloop()


branch_get()

def show_entry_fields():
    print("Username: %s\nPassword: %s" % (e1.get(), e2.get()))

def highlight(Branch):
    df = pd.read_excel(Branch + '.xlsx' , sheet_name = 'Sheet1')

    numberOfRows = len(df.index) + 1

    writer = pd.ExcelWriter(Branch + '.xlsx', engine = 'xlsxwriter')

    df.to_excel(writer, sheet_name = 'Sheet1', index = False)

    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']
    worksheet2 = workbook.add_worksheet('Sheet2')

    CT = workbook.add_format({'bg_color': '#FF0000'})
    Approved = workbook.add_format({'bg_color': '#00FF11'})
    Processing = workbook.add_format({'bg_color': '#FF9100'})
    yetToCertify = workbook.add_format({'bg_color': '#00F7FF'})
    notFound = workbook.add_format({'bg_color': '#D1CACA'})
    bold = workbook.add_format({'bold': True})

    worksheet2.write('B2', 'Legend', bold)
    worksheet2.write('B3', 'Colour', bold)
    worksheet2.write('C3', 'Rule', bold)
    worksheet2.write('B4', 'GREEN', Approved)
    worksheet2.write('C4', "Uploaded and Approved in PERKESO portal")
    worksheet2.write('B5', 'ORANGE', Processing)
    worksheet2.write('C5', "Uploaded and Processing in PERKESO portal")
    worksheet2.write('B6', 'BLUE', yetToCertify)
    worksheet2.write('C6', "Yet to certify test/voucher not confirmed")
    worksheet2.write('B7', 'RED', CT)
    worksheet2.write('C7', "Cancelled Test")
    worksheet2.write('B8', 'GREY', notFound)
    worksheet2.write('C8', "User not found in database")
    worksheet2.write('B9', 'Not Coloured')
    worksheet2.write('C9', "Not enough information to categorise.\nCheck manually")

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())="CT"',
                                  "format": CT
                                 }
    )

    #MAMMOGRAM CONDITIONALS WITH PRICE
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("V"&ROW())&INDIRECT("AG"&ROW())="110BLUE"',
                                  "format": yetToCertify
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("V"&ROW())&INDIRECT("AG"&ROW())="110GREEN"',
                                  "format": Approved
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("V"&ROW())&INDIRECT("AG"&ROW())="110ORANGE"',
                                  "format": Processing
                                 }
    )

    #MAMMOGRAM CONDITIONALS WITH REFERENCE
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AG"&ROW())="PKESOMBLUE"',
                                  "format": yetToCertify
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AG"&ROW())="PKESOMGREEN"',
                                  "format": Approved
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AG"&ROW())="PKESOMORANGE"',
                                  "format": Processing
                                 }
    )

    #NORMAL WITH REFERENCE GREEN
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOGREEN"',
                                  "format": Approved
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOPGREEN"',
                                  "format": Approved
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOCGREEN"',
                                  "format": Approved
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOEGREEN"',
                                  "format": Approved
                                 }
    )

    #NORMAL WITH REFERENCE ORANGE
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOORANGE"',
                                  "format": Processing
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOPORANGE"',
                                  "format": Processing
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOCORANGE"',
                                  "format": Processing
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOEORANGE"',
                                  "format": Processing
                                 }
    )

    #NORMAL WITH REFERENE BLUE
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOBLUE"',
                                  "format": yetToCertify
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOPBLUE"',
                                  "format": yetToCertify
                                 }
    )

    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOCBLUE"',
                                  "format": yetToCertify
                                 }
    )
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("S"&ROW())&INDIRECT("AF"&ROW())="PKESOEBLUE"',
                                  "format": yetToCertify
                                 }
    )

    #NOT APPROVED
    worksheet.conditional_format("$A$1:$AH$%d" % (numberOfRows),
                                 {"type": "formula",
                                  "criteria": '=INDIRECT("AF"&ROW())="Not Found"',
                                  "format": notFound
                                 }
    )

    workbook.close()

highlight(Branch)