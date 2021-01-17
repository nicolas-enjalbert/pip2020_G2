# Read_me.md
PIP SID 2021
## Groupe 2 : Identification of relevant sources

The document named "DataDocumentation.odt" describes the content of our data frames.
The document named "Présentation du travail du groupe 2" describes the thematic content of the files (french version). 

You can find on on the folder "POC" all our Proofs of concept. 

## Automation 
The folder "G2_serveur_v4" contains our two automation processes. 
If you want to execute the 'Identification of relevant sources' you can execute the file 'G2_pipeline_nouvelles_sources.py'. This process could be executed once a week.
For example if you want to execute it all monday at 8:00 AM, you can use a crontab with ``` 0 8 * * 1 python3 /g2_serveur_v4/G2_pipeline_nouvelles_sources.py```

For daily scraping of relevant sources, you can execute the file 'G2_pipeline_scraping.py' or use the crontab command ``` 0 12 * * * python3 /g2_serveur_v4/ G2_pipeline_scraping.py```
Before that, you need to install chromedriver. 

#### Installation of ChromeDriver

##### If you are using UNIX/LINUX you need to open a shell and execute the following lines :
```
sudo apt-get -y install google-chrome-stable
unzip chromedriver_linux64.zip 
sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root /usr/bin/chromedriver 
sudo chmod +x /usr/bin/chromedriver
```

Note that you need to change repository between line 1 and 2.



##### If you are using  WINDOWS you need to  :

Download ChromeDriver and specify the path to .exe file into a 
environment variable "PATH". 

In both cases we invite you to consult the official documentation (https://chromedriver.chromium.org/).
Note you can also use it for another browser.

## Data 

You can find an example of our data resulting of the automation process in the folder `data`. 
The file `df_crawling_clean.json` contains the result of google crawling to identify revelent sources. 
The file `list_new_sources.json` contains the result of revelent sources. 
The file `scrapedData.json` contains final data obtained from the daily scrapping of revelent sources. The purpose of this file is to be inserted in a database. 
To open this file please use :
``` 
import pandas as pd
pd.read_json('scrapedData.json', orient='records')
```
The file `tags_crawl.json` contains the knowledge base used for the daily crawling of revelent sources. 

##### How to add a line in the tags_crawl.json file.

You can achieve this task using g2_update_json.add_line_json python function.
This function takes 2 arguments ; the path to json file and a list of data you want to add.
In the list you need to put in this exact order :  
  * The site name  
  * URL of the source site  
  * The part of URL before keywords (ex: search?q=).  
  * name of the closest identifiable tag to get article url (ex : div)  
  * attribute key of the closest identifiable tag (ex : class)  
  * attribute value of the closest identifiable tag  
  * The separator between keywords (ex : +)  
  * PHP attributes that may be after the keywords  
