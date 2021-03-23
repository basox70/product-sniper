import os,requests
from bs4 import BeautifulSoup
import smtplib, time
from dotenv import load_dotenv

load_dotenv()
FROM_EMAIL=os.getenv('FROM_EMAIL')
TO_EMAIL=os.getenv('TO_EMAIL')
PASSWORD=os.getenv('PASSWORD')

EMAIL = False
if type(FROM_EMAIL) != 'NoneType' and type(TO_EMAIL) != 'NoneType' and type(PASSWORD) != 'NoneType':
    EMAIL = True
    
URL = 'https://www.amazon.co.uk/PlayStation-9395003-5-Console/dp/B08H95Y452/ref=sr_1_1?dchild=1&keywords=ps5&qid=1615488436&sr=8-1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}


def check_availability():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    TITLE = soup.find(id="productTitle").get_text()
    AVAILABILITY = soup.find(id="availability").get_text()

    if 'unavailable' not in AVAILABILITY:
        print(f"{TITLE.strip()} is back in stock.")
        if EMAIL:
            send_mail()
    else:
        print(f"{TITLE.strip()} is out of stock.")


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(FROM_EMAIL, PASSWORD)

    subject = "Item is back in stock!"
    body = f"Check the Amazon link:\n\n{URL}"


    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        FROM_EMAIL,
        TO_EMAIL,
        msg
    )
    print('EMAIL HAS BEEN SENT!')
    
    server.quit()

while True:
    check_availability()
    time.sleep(60)
