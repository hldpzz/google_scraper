from logging import exception
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from db_client import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import time



options = Options()
options.add_argument("--headless")
options.binary_location = ()
driver = webdriver.Firefox(executable_path="./geckodriver", options=options)






## REGEXES
phone_expression = re.compile(r'\([0-9]{2}\)\s9')
is_phone = re.compile(r'\([0-9]{2}.*[0-9]')
resto = re.compile(r'.*\(')
##                
link = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=restaurante+curitiba+telefone&rflfq=1&num=10&sa=X&ved=2ahUKEwi9gfeK1o35AhXjrpUCHazaDgcQjGp6BAgJEAE&biw=1350&bih=651&dpr=1#rlfi=hd:;si:;mv:[[-25.39312008396254,-49.19421861870116],[-25.470013561689463,-49.35386369926756],null,[-25.43157295658017,-49.27404115898436],13]'
ramo = 'lanchonete'
cidade = 'são paulo'

##XPATH RECORRENTE:
zoom_xpath = "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[@id='rhs']/div/div[@id='lu_pinned_rhs']/div[@class='zU3xpf zOnk9d']/div/div[@class='QIp1Rc aEm15c']/div[@class='widget-zoom']/button[@class='CZShK ulSkxc']"
blocks_xpath = "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[@id='center_col']/div[@class='wzRn3d']/div[@id='res']/div[@id='search']/div/div[@id='rso']/div/div[@class='rl_full-list']/div/div[@id='rl_ist0']/div[@id='rl_ist0']/div/div[@class='rl_tile-group']/div[@class='rlfl__tls rl_tls']/div"
next_xpath = "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[@id='center_col']/div[@class='wzRn3d']/div[@id='res']/div[@id='search']/div/div[@id='rso']/div/div[@class='rl_full-list']/div/div[@id='rl_ist0']/div[@id='rl_ist0']/div/div[2]/div[@class='std']/table[@class='AaVjTc']/tbody/tr/td[@class='d6cvqb BBwThe'][2]/a[@id='pnnext']"
close_xpath ="/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[@id='rhs']/div/div[@class='h2yBfgNjGpc__inline-item-view']/div[@class='QU77pf']/span[@class='z1asCe rzyADb']/svg[@class='[object SVGAnimatedString]']"
map_xpath = "/html/body[@id='gsr']/div[@id='main']/div[@id='cnt']/div[@id='rcnt']/div[@id='rhs']/div/div[@id='lu_pinned_rhs']/div[@class='zU3xpf zOnk9d']/div/div[1]/div/div[@class='gm-style']/div[2]/div[2]"
##------------------------------------------


def getFirstPage(link):
    
    try:
        driver.get(link)
    except:
        print('error getting first page')
        
    
    
    
def sendSearch(ramo,cidade):
    search_bar = driver.find_element(By.NAME,"q")
    search_btn = driver.find_element(By.NAME,"btnG")
    search_string = f"{ramo} em {cidade} telefone"
    search_bar.clear()
    search_bar.send_keys(search_string)
    search_btn.click()
    time.sleep(4)
    zoom = driver.find_element(By.CLASS_NAME,'widget-zoom')
    zoom_btn = zoom.find_element(By.TAG_NAME,'button')
    zoom_btn.click()
    
    
    
    
def isNext():
    
    current_source = driver.page_source
    soup = BeautifulSoup(current_source, 'lxml')
    spans = soup.find_all('span')
    for span in spans:
        if span.text == 'Next' or span.text == 'Mais':
            return True
    return False

def getNextPage():
    first_element = driver.find_element(By.CLASS_NAME,'rllt__details')
    first_element.click()
    close_btn = driver.find_element(By.XPATH,close_xpath)
    close_btn.click()
    actions = ActionChains(driver)
    for n in range(30):
        actions.key_down(Keys.PAGE_DOWN).perform()
    next_element = driver.find_element(By.XPATH,next_xpath)
    
    actions.move_to_element(next_element).click(next_element).perform()
        
        
    


    

def criterion(tag):
    return tag.has_attr('div') and re.search(phone_expression, tag.text)
        
def hasPhone(tag):
    search = re.search(phone_expression,tag)
    if search:
        return True
    else:
        return False
    
def process_phone(text):
    current_phone = re.search(is_phone,text).group()
    current_phone = ''.join(re.findall('\d+',current_phone))
    return current_phone

def process_resto(text):
    current_resto = re.search(resto,text).group()
    return current_resto
    
def getBlocks():
    

    current_source = driver.page_source
    soup = BeautifulSoup(current_source, 'lxml')
    blocks = []
    block_selector = soup.find_all('div',class_='rllt__details')
    for block in block_selector:
        name=block.find('span',class_='OSrXXb').text
        divs = block.find_all('div')
        for div in divs:
            div_text = div.text
            if hasPhone(div_text):
                phone = process_phone(div_text)
                end = process_resto(div_text)
                return_object = {'name':name,'phone':phone,'end':end,'stage':'novo'}
                tryInsert(return_object)
                
##--------------------------------- MAIN
def main():
    getFirstPage(link)
    while True:
        current_obj = getRandom()
        sendSearch(current_obj['negocio'],current_obj['nome'])
        getBlocks()
        while True:
            time.sleep(10)
            try:
                getNextPage()
                time.sleep(3)
                getBlocks()
            except:
                break


## -----------------------------------------------------




#roda infinitamente
print('rodando')
while True:
  try:
    main()
  except:
    print('exception')

                
                
        

    