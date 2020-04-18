import requests
from bs4 import BeautifulSoup
import re
from decimal import *
import smtplib

#Checking out for Nescafe Coffee because all other things that I want to check are not in essential items xD #COVID-19
url = 'https://www.amazon.in/dp/B00VK0FTP0/ref=s9_acsd_al_bw_c2_x_2_i?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=2Z9ZDW664RDSVE0GW4H7&pf_rd_t=101&pf_rd_p=a84dfd51-d074-42f8-b381-ae722f857ec5&pf_rd_i=21246959031'
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
price_limit = 285


def check_price():
    #requesting page
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())

    #accesing elements
    title = soup.find(id='productTitle').get_text().strip()
    price = soup.find(id='priceblock_ourprice').get_text()
    price = Decimal(re.sub(r'[^\d.]','',price))
    print(title)
    print(price)

    if price < price_limit:
        send_mail(title , price)


def send_mail(title, price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('divasjindal@gmail.com', 'khwvgqgwolfazsgp')

    subject = f'Price fell down - {title}!'
    body = f"Product Name: {title}  \nPrice: Rs {price} (Limit Fixed: Rs {price_limit})\nCheck the link and buy now!\n"
    link= f"Link: https://www.amazon.in/dp/B00VK0FTP0/ref=s9_acsd_al_bw_c2_x_2_i?pf_rd_m=A1K21FY43GMZF8" \
          f"&pf_rd_s=merchandised-search-3&pf_rd_r=2Z9ZDW664RDSVE0GW4H7&pf_rd_t=101&pf_rd_p=a84dfd51-d074-42f8-b381" \
          f"-ae722f857ec5&pf_rd_i=21246959031 "
    #print(body + link)

    msg = f"Subject: {subject}\n\n\n{body}{link}"

    server.sendmail(
        'divasjindal@gmail.com',
        'divasjindal@gmail.com',
        msg.encode("utf8"))
    print('Hey! Email has been sent.')


# Call the function
check_price()