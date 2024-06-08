#!/home/sudharsan/myenv/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import logging
logging.basicConfig(filename='example.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

driver = webdriver.Chrome()

url = 'https://www.youtube.com/watch?v=SoFxxT_mIsA'

value_storage={}
variable_names=[]

def variable_retrievel():
    driver.get(url)
    script_elements = driver.find_elements(By.TAG_NAME, 'script')

    js_code = ""
    for script in script_elements:
        if script.get_attribute('src'):
            pass
        else:
            js_code += script.get_attribute('innerHTML') + "\n"

    variable_pattern = re.compile(r'\b(var|let|const)\s+(\w+)', re.MULTILINE)
    variables = variable_pattern.findall(js_code)

    global variable_names
    variable_names = [var[1] for var in variables]
    for var_name in variable_names:
        value_storage[var_name]=value_retrievel(var_name)

    logging.info(f'Variables found { value_storage}')
    print(f"Variables found { value_storage}")

def value_retrievel(var_name):
    try:
        return driver.execute_script(f'return {var_name};')
    except:
        return None

def check_change():
    for keys in value_storage.keys():
        var_change=value_retrievel(keys)
        if(var_change!=value_storage[keys] and var_change!=None):
            logging.info(f"value changed {keys} => {var_change}")
            value_storage[keys]=var_change

variable_retrievel()

while(True):
    time.sleep(5)
    check_change()

driver.quit()
