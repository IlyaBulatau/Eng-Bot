# 📚 English study bot
## Stack
![Static Badge](https://img.shields.io/badge/Python-3.10-brightgreen?style=socila&logo=Python&labelColor=grey) ![Static Badge](https://img.shields.io/badge/MongoDB-7.0-brightgreen?style=socila&logo=mongodb&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Python%20telegram%20bot-20.6-brightgreen?style=socila&logo=telegram&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Redis-7.1-brightgreen?style=socila&logo=redis&labelColor=grey)

![Static Badge](https://img.shields.io/badge/Celery-5.3.4-brightgreen?style=socila&logo=celery&labelColor=grey) ![Static Badge](https://img.shields.io/badge/RabbitMQ-3.13-brightgreen?style=socila&logo=RabbitMQ&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Pytest-7.4.3-brightgreen?style=socila&logo=Pytest&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Docker-24.0.2-brightgreen?style=socila&logo=docker&labelColor=grey)

![Static Badge](https://img.shields.io/badge/Ubuntu-22.04.1-brightgreen?style=socila&logo=Ubuntu&labelColor=grey)






This bot implements the process save words and they translate.
MongoDB is a database, main models which it manage are word and user objects.
In databse keeping user models that containe following fields: telegram_id, username or first name, language code, and list of word list models. 
Word list model in it case has following field: created time and list of words.
Finally word model containe: english word and translate fields. These models introduce in below.

| User          |     
|---------------|
|telegram ID    | 
|username       |
|language code  |
|words          |
--------------------------

| Word          | 
|---------------|
|english word   |
|translate      |
--------------------------

| List of words | 
|---------------|
|created time   |
|words          |

# Functionality
 - Adding new word
 - Showing list of words by date
 - Tracking chats updates
 - Limiting on use
 - scheduling learn reminders
 - Controlling updates

#  How run!?

1. #### Clone the repo.
```
git clone https://github.com/IlyaBulatau/Eng-Bot.git
```
___
2. #### Install of requirements.
```
poetry install
```
___
3. #### Activate poetry.
```
poetry shell
```
___
4. #### Create .env file.
```
touch .env
```
___
5. #### Fill in the file data according to the example .env.example.
 
> [!NOTE]
> All fields in the env file are required.
> Also, you need a token of bot
___
6. #### Now you can run bot!
```
make app
```
## Services
For more comfortable development and tracking of the bot, there are user interfaces for MongoDB, RabbitMQ and Celery.
You can use them if you open them in a browser on your localhost.

> [!IMPORTANT]
> **If you set DEBUG=0 as your environment variable.
> When launched, the bot will read the .env.prod file, but not the .env file.
> And if you don't have the file, the bot won't be able to work.
> Check the config.py file.**

___
### If you have ideas on how to improve the bot, please submit a pull request.
