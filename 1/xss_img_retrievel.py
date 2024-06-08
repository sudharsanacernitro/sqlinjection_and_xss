#!/home/sudharsan/myenv/bin/python3
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome()
driver.get('https://www.kongu.ac.in/departments/cse.php')
driver.execute_script("ShowData('faculty')")
time.sleep(5)
html_content = driver.page_source
driver.quit()

soup = BeautifulSoup(html_content, 'html.parser')
divs = soup.find_all('div', id='deptinfo')

for div in divs:
    anchor_tags = div.find_all('a')
    for anchor_tag in anchor_tags:
        if 'pdf' not in anchor_tag['href']:
            try:
                response = requests.get(anchor_tag['href'])
                s = BeautifulSoup(response.content, 'html.parser')  
                src = s.find('img')['src']
                with open(f'./cse/{anchor_tag.text}.jpeg', 'wb') as f:
                    img_response = requests.get(src)
                    f.write(img_response.content)
                    print(f"Downloaded {anchor_tag.text}.jpeg")
            except Exception as e:
                print(f"Error downloading {anchor_tag.text}: {e}")
