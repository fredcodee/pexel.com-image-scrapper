from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
import requests
from time import sleep

CHROMEDRIVER_PATH = "C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver"
options = Options()
options.add_argument("--headless")  # Runs Chrome in headless mode.
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-gpu')  # applicable to windows os only
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

browser.get("https://www.pexels.com")
sleep(3)

#to search keyword
searchBar = browser.find_element_by_id("search")
searchBar.send_keys("cock") #<<<--------- WORD TO SEARCH
searchBar.send_keys(Keys.ENTER)
sleep(3)

#to get how many images found
hw_results = browser.find_elements_by_class_name("rd__tabs")[0].text
hw_results = "%s photos found " % (hw_results.split(" ")[0])
print(hw_results)

#load images
lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while(match == False):
  lastCount = lenOfPage
  sleep(3)
  lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
  if lastCount == lenOfPage:
    match = True

#get imgages
url_contents = soup(browser.page_source, "html.parser")
all_img = url_contents.find("div", class_="photos__column")
all_img = all_img.find_all("img", class_="photo-item__img")
links=[]
for images in all_img:
  links.append(images.get('src'))
downloadable_imgs = "%s photos can be downloaded"% (len(links))
print(downloadable_imgs)

#download
count = 0
for link in links:
  try:
    link=link.split("?")[0]
    filename = link.split("/")[-1].split(".")[0]
    r2 = requests.get(link)
    with open(filename + ".jpeg", 'wb') as imagefile:
      imagefile.write(r2.content)
    count += 1
  except:
    print("error, cant download this image...")    
print("Total images downloaded:", count)


browser.quit()



