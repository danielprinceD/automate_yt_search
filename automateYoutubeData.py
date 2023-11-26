import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# Ask the user to input what they want to search for on YouTube
search = input("What are you looking for on YouTube? ")

# Formulate the YouTube search URL based on the user's input
website = 'https://www.youtube.com/results?search_query=' + search

# Print the type of the 'website' variable for reference
print(f'The type of the website variable is: {type(website)}')

# Specify the location of the ChromeDriver executable
path = "./chromedriver-win64/chromedriver.exe"

# Configure the ChromeDriver service
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Open the YouTube search results page using the constructed URL
driver.get(website)

# Prepare lists to store information about the videos in the search results
titles = []       # Video titles
channels = []     # Channel links
views = []        # Number of views
year_agos = []     # Time since upload

# Scroll down to load more search results
driver.execute_script('window.scrollBy(0,30000)')
time.sleep(5)  # Wait for the page to load

# Retrieve all video elements from the search results
templates = driver.find_elements(by='xpath', value='//div[@id="dismissible"]/div')

# Iterate through each video element to extract relevant information
for template in templates:
    try:
        # Extract information from each video element
        title = template.find_element(by='xpath', value=".//div[@id='meta']/div/h3/a[@id='video-title']").get_attribute('title')
        channel = template.find_element(by='xpath', value=".//div[@id='channel-info']//div[@id='container']/div//a").get_attribute('href')
        view = template.find_element(by='xpath', value="./div[@id='meta']//span[1]").text
        year_ago = template.find_element(by='xpath', value="./div[@id='meta']//div[@id='metadata-line']//span[2]").text

        # Append the extracted information to the respective lists
        titles.append(title)
        channels.append(channel)
        views.append(view)
        year_agos.append(year_ago)
    except Exception as e:
        # If an exception occurs (e.g., an element is not found), skip to the next iteration
        pass

# Create a dictionary from the collected information and convert it into a DataFrame
form_dict = {
    'Title': titles,
    'Channel': channels,
    'Views': views,
    'Ago': year_agos
}
data_frame = pd.DataFrame(form_dict)

# Save the DataFrame to a CSV file with a name based on the search query
data_frame.to_csv('Search_Results_'+str(search)+'.csv')

# Close the ChromeDriver
driver.quit()
