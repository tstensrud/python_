import re
import tkinter
from tkinter import messagebox
import requests
import sys
from tkinter import *
from bs4 import BeautifulSoup

def writeToFile(input):
    fileName = fldUrl.get()

    #filename is url without https://, e.g. "www.google.com.txt"
    try:
        file = open(fileName[8:] + ".txt", "x")
        file.write(input)
        file.close()
        messagebox.showinfo(title="File written", message="Written to file success!")
    except Exception as e:
        messagebox.showerror(title="File allready exist", message=e.__class__)


def scraper():
    txtResult.delete(1.0, tkinter.END)
    write = writeToFileValue.get()

    #check that URL starts with https://
    url = fldUrl.get()
    if ("https://" not in url):
        txtResult.insert(1.0, "URL \"" + url + "\" is not valid. Must start with https://")
        return

    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        for i in soup.find_all('a', attrs={'href': re.compile("^https://")}):
            txtResult.insert(END, "- " + i.get('href') + "\n")
    except Exception as e:
        txtResult.insert(1.0, e.__class__)
    
    #if write to file is checked
    if (write == 1):
        writeToFile(txtResult.get(1.0, tkinter.END))



frmMain = tkinter.Tk()
frmMain.title("Scrape")
frmMain.geometry("700x700")

#URL label
lblHeader = tkinter.Label(text="URL:")
lblHeader.place(x=20, y=20)

#field for URL-entry
fldUrl = tkinter.Entry(width="70")
fldUrl.place(x= 50, y = 20)

#button to initiate scrape
btnUrl = tkinter.Button(text="Go", width="10", height="1", command=scraper)
btnUrl.place(x=500, y=17)

#write to file checkbox
writeToFileValue = tkinter.IntVar()
chkWrite = tkinter.Checkbutton(frmMain, text="Write to file", variable=writeToFileValue)
chkWrite.place(x=20, y=60)

#scroolbar and text area for output
scrollbar = tkinter.Scrollbar(frmMain)
scrollbar.pack(side=RIGHT, fill=Y)
txtResult = tkinter.Text()
txtResult.place(x=20, y=160, width=650, height=500)
txtResult.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txtResult.yview)

frmMain.resizable(False, False)
frmMain.mainloop()