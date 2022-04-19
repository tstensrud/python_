import re
import tkinter
import requests

from tkinter import messagebox
from tkinter import *
from bs4 import BeautifulSoup

imagesList= []

def writeToFile(input, writeContent):
    fileName = fldUrl.get()
    fileNameContent = ""
    if (writeContent == 1):
        fileNameContent = "links"
    elif(writeContent == 2):
        fileNameContent = "emails"
    elif(writeContent == 3):
        fileNameContent = "images"

    #filename is url without https://, e.g. "www.google.com.txt"
    try:
        file = open(fileName[8:] + " - " + fileNameContent + ".txt", "x")
        file.write(input)
        file.close()
        messagebox.showinfo(title="File written", message="Written to file success!")
    except Exception as e:
        messagebox.showerror(title="File allready exist", message=e.__class__)

def downloadImages():
    try:
        for url in imagesList:
            imageName = ""
            imageUrl = requests.get(url) #this fails
            imageFile = imageUrl
            for i in reversed(url):
                if (i == "/"):
                    break
                imageName += imageName.join(i)
            file = open(imageName[::-1], "wb")
            file.write(imageFile.content)
            file.close()
    except Exception as e:
        messagebox.showerror(title="Could not download", message=e.__class__ )
    

def scraper():
    txtResult.delete(1.0, tkinter.END)
    write = writeToFileValue.get()
    downloadImagesChecked = downloadImagesValue.get()
    scrapeType = radioScrapeChoice.get()

    #check that URL starts with https://
    url = fldUrl.get()
    if ("https://" not in url):
        txtResult.insert(1.0, "URL \"" + url + "\" is not valid. Must start with https://")
        return
    
    #exception handling if URL connection fails
    try:
        data = requests.get(url)
        soup = BeautifulSoup(data.text, 'html.parser')
    except Exception as e:
        messagebox.showerror(title="Connection error", message=e.__class__)
        return

    #scrape and print to text area
    #scrapeType 1=links, 2=emails, 3=images
    
    if(scrapeType == 1):
        for i in soup.find_all('a', attrs={'href': re.compile("^http")}):
            txtResult.insert(END, i.get('href') + "\n")
    elif(scrapeType == 2):
        for i in soup.find_all('a', attrs={'href': re.compile("^mailto")}):
            txtResult.insert(END, i.get('href') + "\n") 
    elif(scrapeType == 3):
        imagesList.clear()
        for i in soup.find_all('img', attrs={'src': re.compile("^")}):
            imageUrl = i.get('src')
            txtResult.insert(END, imageUrl + "\n")
            imagesList.append(imageUrl)
        if (downloadImagesChecked == 1):
            downloadImages()
    else:
        messagebox.showinfo(title="Choose", message="Choose what to scrape")
    #if write to file is checked
    if (write == 1):
        writeToFile(txtResult.get(1.0, tkinter.END), scrapeType)



frmMain = tkinter.Tk()
frmMain.title("Scrape")
frmMain.geometry("700x700")

#URL label
lblHeader = tkinter.Label(text="URL:")
lblHeader.place(x=20, y=20)

#field for URL-entry
fldUrl = tkinter.Entry(width="70")
fldUrl.insert(0, "https://www.structor.no")
fldUrl.place(x= 50, y = 20)

#button to initiate scrape
btnUrl = tkinter.Button(text="Go", width="10", height="1", command=scraper)
btnUrl.place(x=500, y=17)

#radiobuttons
radioScrapeChoice = tkinter.IntVar()
radioBtnLinks = Radiobutton(frmMain, text="Get links", variable=radioScrapeChoice, value=1)
radioBtnLinks.place(x=20, y=80)
radioBtnEmails = Radiobutton(frmMain, text="Get emails", variable=radioScrapeChoice, value=2)
radioBtnEmails.place(x=20, y=100)
radioBtnImages = Radiobutton(frmMain, text="Get images", variable=radioScrapeChoice, value=3)
radioBtnImages.place(x=20, y=120)

#write to file checkbox
writeToFileValue = tkinter.IntVar()
chkWrite = tkinter.Checkbutton(frmMain, text="Write to file", variable=writeToFileValue)
chkWrite.place(x=20, y=60)

#download images
downloadImagesValue = tkinter.IntVar()
chkDownloadImages = tkinter.Checkbutton(frmMain, text="Download images", variable=downloadImagesValue)
chkDownloadImages.place(x=120, y=120)

#scroolbar and text area for output
scrollbar = tkinter.Scrollbar(frmMain)
scrollbar.pack(side=RIGHT, fill=Y)
txtResult = tkinter.Text()
txtResult.place(x=20, y=160, width=650, height=500)
txtResult.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txtResult.yview)

frmMain.resizable(False, False)
frmMain.mainloop()