from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, urllib.request
import os

#input data
profile_to_scrap = input("Name of profile to scraping: ")
your_login = input("Your login: ")
your_password = input("Your password: ")

#driver - replace executable_path on your own
driver = webdriver.Chrome(executable_path=r"C:\Users\beses\Desktop\chromedriver_win32\chromedriver.exe")
driver.get("https://www.instagram.com/")

#login
time.sleep(3.5)
username = driver.find_element_by_css_selector("input[name='username']")
password = driver.find_element_by_css_selector("input[name='password']")
username.clear()
password.clear()
username.send_keys(your_login)
password.send_keys(your_password)

#Cookies accept?
#replace - 'Akceptuję wszystko' - depends from your language for example in English - 'Accept all'
accept = driver.find_element_by_xpath("//button[contains(text(), 'Akceptuję wszystko')]").click()
time.sleep(3)
login = driver.find_element_by_css_selector("button[type='submit']").click()

#save your login info?
time.sleep(3.5)
#replace - 'Nie teraz' - depends from your language for example in English - 'Not now'
notnow = driver.find_element_by_xpath("//button[contains(text(), 'Nie teraz')]").click()

#searchbox
time.sleep(3)
#replace - 'Szukaj' - depends from your language for example in English - 'Search'
searchbox = driver.find_element_by_css_selector("input[placeholder='Szukaj']")
searchbox.clear()
searchbox.send_keys(profile_to_scrap)
time.sleep(3)
searchbox.send_keys(Keys.ENTER)
time.sleep(3)
searchbox.send_keys(Keys.ENTER)


#get videos and images
def get_links():
    time.sleep(2.5)
    links = driver.find_elements_by_tag_name('a')
    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post and post not in posts:
            posts.append(post)
posts = []
get_links()
match=False
scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")

while(match==False):
    get_links()
    last_count = scrolldown
    scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    if last_count==scrolldown:
        match=True



print("Found: {} posts".format(len(posts)))
download_url = ''
counter = 1
for post in posts:
    driver.get(post)
    shortcode = driver.current_url.split("/")[-2]
    print("Downloading {}/{} of posts".format(counter, len(posts)))
    time.sleep(3)
    if driver.find_element_by_css_selector("img[style='object-fit: cover;']") is not None:
        download_url = driver.find_element_by_css_selector("img[style='object-fit: cover;']").get_attribute('src')
        dir = 'photos/{}'.format(profile_to_scrap)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        urllib.request.urlretrieve( download_url, 'photos/{}/{}-{}.jpg'.format(profile_to_scrap, counter, shortcode))
    else:
        download_url = driver.find_element_by_css_selector("video[type='video/mp4']").get_attribute('src')
        dir = 'videos/{}'.format(profile_to_scrap)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        urllib.request.urlretrieve( download_url, 'videos/{}/{}-{}.jpg'.format(profile_to_scrap, counter, shortcode))
        time.sleep(6)
    counter += 1

