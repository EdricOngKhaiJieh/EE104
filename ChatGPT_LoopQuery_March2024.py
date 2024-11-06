# -*- coding: utf-8 -*-
"""
Created on Friday March 22 11:24:40 2024
@author: chris.pham
"""

#The following code will work for Python 3.7.x+

#----------------------------------------------
#REMEMBER TO RUN THESE PIP COMMANDS if you have an older OpenAI:
#pip uninstall openai
#Note: the command may look like this in your venv  C:\Python310\Scripts\pip install openai pandas python-dotenv

#----------------------------------------------
#RUN THESE COMMANDS FROM THE TERMINAL
#Create the virtual environment called "venv"
#python -m venv venv   

#from venv
#pip install openai==0.28 pandas python-dotenv

#Activate the venv 
#Windows command:
#venv\Scripts\activate
#MacOS or Linix command: 
#source chatgpt_env/bin/activate



import os
import openai #remember to pip install pandas openai
from dotenv import load_dotenv  #remember to pip install python-dotenv
load_dotenv()

# Set the API key
"""
# Visit your API Keys page to retrieve the API key you'll use in your requests.
# Remember that your API key is a secret! Do not share it with others or expose 
#  it in any client-side code (browsers, apps).
https://platform.openai.com/account/api-keys 

You will need these two (both are confidential):
YOUR OPENAI ORG KEY (from the left panel, click on Settings)
OPENAI_API_KEY (from your picture on the top right of the browser, click on your organization, then click on View API keys)
"""
openai.api_key=("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")

#Examples of messages being built with two parts: Role & Tasks
#---
#messages = [{"role": "system", "content": "You are a poet"}]
#messages.append({"role": "user", "content": "Get the sum of 5 and 5^2"})
#---
#messages = [{"role": "system", "content": "You are a mathematician"}]
#messages.append({"role": "user", "content": "Get the sum of 5 and 5^2"})

while (True):
    myrole = input("\nWhat is my role? (or type 'quitme' to quit): \n")
    if(myrole == 'quitme'):
        break
    mytask = input("\nWhat is my task? (or type 'quitme' to quit): \n")
    if(mytask == 'quitme'):
        break

    messages = [{"role": "system", "content": myrole}]
    messages.append({"role": "user", "content": mytask})
    

    #Uncomment each of the optional parameters below and 
    #  observe the differences. Try different values and see more differences.
    #Go to this site to learn about parameters https://www.codecademy.com/article/setting-parameters-in-open-ai
    
    answers = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #original model = "gpt-3.5-turbo". 
        temperature = 0.1,   #original temperature = 0.7. "temperature" controls the randomness of responses
        max_tokens = 1000,    #original max_token = 100. "max_tokens" sets the maximum length for the models output
        top_p = 0.5,          # original top_p = 1. "top_p" dictates the variety in responses by only considering the top 'P' percent of probable words.
        frequency_penalty = 2,  #original frequency_penalty = 0. "frequency_penalty" reduces repetition by decreasing the liklihood of frequency used words.
        presence_penalty = 2,   #original presence_penalty. "presence_penalty" promots the introduction of new topics in conversation.
        messages = messages     #messages helps set the behavior of the assistant
    )



    print("----------------\n")
    print(answers['choices'][0]['message']['content'])
    # same as print(answers.choices[0].message.content)
    print("----------------\n")