import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
import smtplib
from urllib.parse import urlparse
from csv import writer
class tracker():
    def __init__(self):
        self.db = []
        with open("db1.csv") as file_name:   # csv to arr
            file_read = csv.reader(file_name)
            for row in file_read:
                self.db.append(row)
        j=0
        for i in self.db:
            if i[0]=='':
                j+=1
        for k in range(j):
            self.db.pop()

        print(self.db)

    def add(self,url):  # add new product
        price,title=self.main(url)
        a=[url,title,price]
        self.db.append(a)
        pd.DataFrame(self.db).to_csv('db1.csv', header=None, index=None)



    def update(self,k=-1):  # updating price
        if k==-1:
            for i in range(0,len(self.db)):
                prev=float(self.db[i][2].replace(',', ''))
                self.db[i][2], self.db[i][1] = self.main(self.db[i][0])
                if prev>float(self.db[k][2].replace(',', '')):
                    self.send_mail(self.db[i][0])

        else:

            prev1 = float(self.db[k][2].replace(',', ''))
            self.db[k][2], self.db[k][1] = self.main(self.db[k][0])
            if prev1 > float(self.db[k][2].replace(',', '')):
                self.send_mail(self.db[k][0])
        #print(self.db)
        pd.DataFrame(self.db).to_csv('db1.csv', header=None,index=None)


    def main(self,URL):  # price tracking
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.83'}
        page = requests.get(URL, headers=headers)

        domain = urlparse(URL).netloc

        soup = BeautifulSoup(page.content, 'html.parser')

        if domain=='www.amazon.in':

            title = soup.find(id="productTitle").get_text()
            price = soup.find("span", {"class": "a-offscreen"}).get_text()
            price=price[1:]

        elif domain=="www.flipkart.com":
            price=soup.find("div", {"class": "_30jeq3 _16Jk6d"}).get_text()
            title= soup.find("span", {"class": "B_NuCI"}).get_text()
            price = price[1:]


        return price,title
    def send_mail(self,link):   #price alert mail
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('abc@gmail.com','password')
        subject='price drop alert!'
        msg=f"Subject: {subject}\n\n{link}"
        server.sendmail('abc@gmail.com','efg@gmail.com',msg)
        server.quit()
###########
