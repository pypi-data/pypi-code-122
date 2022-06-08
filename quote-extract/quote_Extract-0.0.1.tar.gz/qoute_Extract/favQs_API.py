import json #including the json library for handling .json files
import requests #For making request to the website


#Storing the requested information to DataJson
DataJson = requests.get('https://favqs.com/api/qotd').text

#Converting the DataJson into a dictionary
data = json.loads(DataJson)

quote = data['quote']['body']
author = data['quote']['author']
print(f'{quote} by {author}')

