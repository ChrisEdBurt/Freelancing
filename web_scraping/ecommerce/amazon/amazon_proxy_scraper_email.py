import requests
from bs4 import BeautifulSoup
import smtplib
import time

url="https://www.amazon.in/BULLMER-Cotton-Printed-T-shirt-Multicolour/dp/B0892SZX7F/ref=sr_1_4?c=ts&dchild=1&keywords=Men%27s+T-Shirts&pf_rd_i=1968024031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=8b97601b-3643-402d-866f-95cc6c9f08d4&pf_rd_r=EPY70Y57HP1220DK033Y&pf_rd_s=merchandised-search-6&qid=1596817115&refinements=p_72%3A1318477031&s=apparel&sr=1-4&ts_id=1968123031"

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"}

http_proxy  = "http://10.10.1.10:3128"
https_proxy = "https://10.10.1.11:1080"
ftp_proxy   = "ftp://10.10.1.10:3128"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

def check_price():

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    title = soup.find(id = "productTitle")
    if title:
        title = title.get_text()
    else:
        title = "default_title"
    print(title.strip())

    price = soup.find(id="priceblock_ourprice")
    if price:
        price = price.get_text()
    else:
        price = "no price"
    print(price.strip())

    if title and price:
        send_mail()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo

    server.login('****', '****')

    subject = "Testing email"
    body = "Check this amazon link https://www.amazon.com/Crucial-MX500-NAND-SATA-Internal/dp/B078211KBB/ref=sr_1_1_sspa?dchild=1&keywords=SSD&qid=1623623879&refinements=p_n_feature_three_browse-bin%3A6797521011%2Cp_n_feature_keywords_five_browse-bin%3A7688215011%2Cp_n_feature_browse-bin%3A23487839011%2Cp_72%3A1248879011&rnid=1248877011&s=pc&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExQ1A4MjlCS080WEZZJmVuY3J5cHRlZElkPUEwNjczODMxMlI3UEEwVjczNVJPOSZlbmNyeXB0ZWRBZElkPUEwMzIxNDIxMTBNN1BGSTc4NEJYNyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU= "

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        '****',
        '****',
        msg
    )
    print("Email has been sent")

    server.quit()

while(True):
    check_price()
    time.sleep(60*60*12)