from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

service = Service(r"C:\Users\Acer\Desktop\Code course\scrape-bot\user version\twitter-scrape-bot\chromedriver.exe") #path for chromedriver MUST HAVE FOR SCRIPT TO WORK

# Create the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

#////--------- PARAMETERS TO SEARCH ---------////
SCROLL_PAUSE_TIME = 3 #(very optional) better keep as default
TIME = 120 #TIME to search in seconds 
excel_name = "" #name for excel file MUST HAVE '.xlsx' extension
user_name = "" #bot account username
password = "" #password for account
post_link = "" #post to search


#////--------- LOGIN ---------////

driver.get("https://x.com")
print(driver.title)
time.sleep(5)
accept_cookies_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Accept all cookies')]")
accept_cookies_button.click()
time.sleep(5)
login_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Sign in')]")
login_button.click()
time.sleep(5)
input_field = driver.find_element(By.XPATH, "//input[@name='text']")
input_field.send_keys(user_name)
time.sleep(2)
next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
next_button.click()
time.sleep(2)
input_field = driver.find_element(By.XPATH, "//input[@name='password']")
input_field.send_keys(password)
time.sleep(1)
input_field.send_keys(Keys.RETURN)
time.sleep(7)
driver.get(post_link)
time.sleep(10)

#////--------- COPY COMMENT AND USER NAME ---------////


comments_list = []

start_time = time.time()

previous_height = driver.execute_script("return document.body.scrollHeight")

while True:

    elapsed_time = time.time() - start_time
    if elapsed_time > TIME:  
        break

    comments = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
    userline = driver.find_elements(By.XPATH, '//div[@data-testid="User-Name"]')
    timestamps = driver.find_elements(By.TAG_NAME, 'time')
    
    new_data = []
    # Skip the first post (main post) to save comments and usernames
    for i in range(1,len(comments)):
        lines = userline[i].text.splitlines()
        user = lines[0]
        handle = lines[1]
        timestamp = timestamps[i].text
        comment = comments[i].text
        new_data.append((user,handle,timestamp,comment))

    for entry in new_data:
        if entry not in comments_list:
            comments_list.append(entry)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    
    df = pd.DataFrame(comments_list, columns=["Username", "Handle","Timestamp","Comment"])
    df.to_excel(excel_name, index=False)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:
        break
    previous_height = new_height

# Close browser
driver.quit()

if elapsed_time > TIME:
    print("🚨", TIME/60 ,"minutes have passed. Stopping the script.")

print ("Finish scraping comments !!!")

