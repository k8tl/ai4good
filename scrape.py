import requests #HTTP Request URL for content
from bs4 import BeautifulSoup #Scraping the URL's content
import csv #For saving data to CSV file

#To prevent getting blocked - makes request look like it's coming from a browser
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

#URL of forum main page
URL = "https://www.healingwell.com/community/default.aspx?f=16&p="

#Send an HTTP Get Request to the URL
forum = requests.get(URL)

#Take content of the URL and parse it using BeautifulSoup
#This will give you the document tree
content1 = BeautifulSoup(forum.content, "html.parser")

#Next find where each forum post is located within that tree
#For this example they were all links in the class forum-title
titles = content1.find_all('a', class_="forum-title")

#Create an array to store mined text
mined_text = []

#In my case the URLs are linked to through a relative path so I had to concatenate
base = "https://www.healingwell.com" #Not needed if not relative path

for title in titles:

    #Not necessary if full link is included in your case
    indivURL = base + title.get('href')

    #Send a new Get request for the individual topic
    postURL = requests.get(indivURL)

    #Create BeautifulSoup object from concatenated URL
    post = BeautifulSoup(postURL.content, 'html.parser')

    #Find all forum posts on the page
    text = post.find_all('div', class_="post-body")

    #Now get the text from each post within the topics 
    for item in text:
        go = item.get_text(' ')
        #appends mined 
        mined_text.append(go)
        
#Saves text to a CSV file
with open('healingwell_text.csv', 'w') as csvfile:
    wr = csv.writer(csvfile)
    
    #Each row will be a different comment within the posts
    for topic in mined_text:
        
        #Wrap all text with a list - if you don't do this you will have a column for each character
        wr.writerow([topic]) 
