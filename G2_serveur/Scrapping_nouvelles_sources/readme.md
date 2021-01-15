## Installation of ChromeDriver

##### If you are using UNIX/LINUX you need to open a shell and execute the following lines :

sudo apt-get -y install google-chrome-stable
unzip chromedriver_linux64.zip 
sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root /usr/bin/chromedriver 
sudo chmod +x /usr/bin/chromedriver


Note that you need to change repository between line 1 and 2.



##### If you are using  WINDOWS you need to  :

Download ChromeDriver and specify the path to .exe file into a 
environment variable "PATH". 

In both cases we invite you to consult the official documentation (https://chromedriver.chromium.org/).
Note you can also use it for another browser.



## How to add a line in the tags_crawl.json file.

You can achieve this task using g2_update_json.add_line_json python function.
This function takes 2 arguments ; the path to json file and a list of data you want to add.
In the list you need to put in this exact order :
    • The site name
    • URL of the source site
    • The part of URL before keywords (ex: search?q=).
    • name of the closest identifiable tag to get article url (ex : div)
    • attribute key of the closest identifiable tag (ex : class)
    • attribute value of the closest identifiable tag
    • The separator between keywords (ex : +)
    • PHP attributes that may be after the keywords
