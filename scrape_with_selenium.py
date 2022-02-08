from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os
import requests
import shutil
import pickle



# make a webfriver object   -   chrome driver path for my system --> C:/Users/stan.kazovsky/Python_stuff/chromedriver

driver = webdriver.Chrome('/Users/stan.kazovsky/Python_stuff/chromedriver')


class App:
    def __init__(self, username='what3verFr33', password='asdfgh123', target_username='navigare_necesse_est_i_huj', path='C:/Users/stan.kazovsky/downloads/scrape1'):
        
        #print(os.path.exists(path))
        #if not os.path.exists(path):
          #  os.mkdir(path)
        #input('stop for now')
        
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = driver
        self.error = False
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)
        self.counter = 0
        self.picture_source = []
        sleep(2)
        self.soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_images = self.soup.find_all('img')
        
        
        file_exists = os.path.isfile("cookies.pkl")
        if file_exists:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
                
        driver.get(self.main_url)
        sleep(3)
        
        #log in function goes here
        
        # self.log_in()
        # if self.error is False:
        #     self.close_save_box()
        #     sleep(5)
        #     self.close_save_box()
        #     sleep(3)
        self.open_target_profile()
        self.getting_captions(all_images)
        
        if self.error is False:
            self.scroll_down()
            sleep(5)
            print("very good job Stan, you are a star!")
            
        # if self.error is False:
            # if not os.path.exists(path):
            #     os.mkdir(path)
            # self.downloading_images()
            # sleep(1)
            
        print('well done Stan')
        
        # pickle.dump(self.driver.get_cookies(), open("cookies.pkl","wb"))
        self.getting_captions(all_images)
        self.driver.close()
        
        # self.downloading_images()
        
    def getting_captions(self, images):
        
        
        captions_folder_path = os.path.join(self.path, 'captions')
        if not os.path.exists(captions_folder_path):
            os.mkdir(captions_folder_path)
        
        for image in images:
            try:
                #caption = image['alt']
                print(image['alt'])
            except KeyError:
                print('No caption for this picture')
        
        
    def pull_image_links(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.picture_source += [i['src'] for i in soup.find_all('img')]
            
        
        
    def downloading_images(self):
        self.picture_source = list(set(self.picture_source))
        
        try:
            print('Length of all images', len(self.picture_source))
            # for index, image in enumerate(all_images):
            #     filename = 'image_' + str(index) + '.jpg'
            for link in self.picture_source:
                filename = f'image_{self.counter}.jpg'
                # image_path = self.path + '/' + filename
                # that way it will adjust to system requirements:
                image_path = os.path.join(self.path, filename)
                print(link)
                print('Downloading image ', self.counter)
                
                if not "http" in link:
                    continue
                    
                response = requests.get(link, stream=True)
                    
                try:
                    with open(image_path, 'wb') as file:
                        shutil.copyfileobj(response.raw, file)
                        
                except Exception as e:
                    print(e)
                    print('Could not download image number ', self.counter)
                    print('Image Link == ', link)
                self.counter += 1
            #print(image['src'])
                
        except Exception as e:
            print(e)
            print("Error 47")
            pass
        
    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[@class="g47SY "]')
            no_of_posts = str(no_of_posts.text).replace(',', '')
            print(no_of_posts)
            self.no_of_posts = int(no_of_posts)
            
            if self.no_of_posts > 12:
                no_of_scrolls = int(self.no_of_posts/12) + 3
                
                for value in range(no_of_scrolls):
                    print(value)
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(2)
                   # self.picture_source.append()
                    try:
                        self.pull_image_links()
                    except Exception as E:
                        print(E)
                        pass
        except Exception:
            print("Error 2")
            self.driver.close()
        
        
    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@aria-label="Search Input"]')
            search_bar.send_keys(self.target_username)
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
            sleep(3)
        except Exception:
            print("Error with opening profile")
            pass
        
    
    def close_save_box(self):
        try:
            close_btn = self.driver.find_element_by_partial_link_text("Not Now")
            close_btn.click()
            sleep(2)
            
        except Exception:
            sleep(2)
            print("Almost error 3")
            pass
                
        
    def log_in(self):
        try:
            username_input = self.driver.find_element_by_xpath('//input[@name="username"]')
            username_input.send_keys(self.username)
            
            password_input = self.driver.find_element_by_xpath('//input[@aria-label="Password"]')
            password_input.send_keys((self.password))
            sleep(2)
            password_input.submit()
            
            #login_button = driver.find_element_by_link_text('Log In')
            #login_button.click()
        except Exception:
            print('Error1')
        
        
        
if __name__ == '__main__':
    app = App()        
        
     













# Other try
"""
driver.get('https://www.bcorporation.net/en-us/find-a-b-corp/')

sleep(4)

search_button = driver.find_element_by_xpath("//div[@id='gatsby-focus-wrapper']//button")
search_button.click()
sleep(5)

link_to_firm = [li.a for li in soup.find_all('li',class_='ais-Hits-item')]

for link in link_to_firm:
    print(link)
    link.click()
    sleep(4)


"""



#test 1
"""
login_button = driver.find_element_by_link_text('Sign in')
login_button.click()

mobile = driver.find_element_by_id('login-username')
mobile.send_keys('07852988281')

next_button = driver.find_element_by_id('login-signin')
next_button.click()

sleep(15)
"""
#driver.close()
