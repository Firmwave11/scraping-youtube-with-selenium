from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome('D:\Chromedriver\chromedriver')
driver.get("https://www.youtube.com/results?search_query=corona")

user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
links = []

for i in user_data:
            links.append(i.get_attribute('href'))
print(len(links))
df = pd.DataFrame(columns = ['date','category','link', 'title', 'description','views', 'channel', 'comments','like','dislike'])
wait = WebDriverWait(driver, 10)
v_category = "Corona"
for x in links:
            driver.get(x)
            v_id = x.strip('https://www.youtube.com/watch?v=')
            v_published = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"div#date yt-formatted-string"))).text
            v_title = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
            v_description =  wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"div#description yt-formatted-string"))).text.replace("\n", "")
            v_views =  wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"div#count yt-view-count-renderer"))).text
            v_channel =  wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"div#upload-info yt-formatted-string"))).text
            driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
            v_comments = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"h2#count > yt-formatted-string"))).text
            v_like =  wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
            v_dislike =  wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2) "))).text
            df.loc[len(df)] = [v_published, v_category, v_id, v_title, v_description, v_views, v_channel, v_comments, v_like, v_dislike]
dict2 = df.to_dict(orient='records')
with open('corona.json', 'w') as fp:
    json.dump(dict2, fp, sort_keys=True, indent=4)
