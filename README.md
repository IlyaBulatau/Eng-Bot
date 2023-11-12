# 📚 English study bot
## Stack
![Static Badge](https://img.shields.io/badge/Python-3.10-brightgreen?style=socila&logo=Python&labelColor=grey) ![Static Badge](https://img.shields.io/badge/MongoDB-7.0-brightgreen?style=socila&logo=mongodb&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Python%20telegram%20bot-20.6-brightgreen?style=socila&logo=telegram&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Redis-7.1-brightgreen?style=socila&logo=redis&labelColor=grey)

![Static Badge](https://img.shields.io/badge/Celery-5.3.4-brightgreen?style=socila&logo=celery&labelColor=grey) ![Static Badge](https://img.shields.io/badge/RabbitMQ-3.13-brightgreen?style=socila&logo=RabbitMQ&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Pytest-7.4.3-brightgreen?style=socila&logo=Pytest&labelColor=grey) ![Static Badge](https://img.shields.io/badge/Docker-24.0.2-brightgreen?style=socila&logo=docker&labelColor=grey)

![Static Badge](https://img.shields.io/badge/Ubuntu-22.04.1-brightgreen?style=socila&logo=Ubuntu&labelColor=grey)






This bot implements the process save words and they translate.
Also it can translate word and return pronocuation this word.
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
 - Translating words
 - Showing list of words by date
 - Tracking chats updates
 - Limiting on use
 - Scheduling and sending learn reminders
 - Controlling updates

# Description commands
 - `/start` - Greeting command
 - `/cancel` - Resetting all works processes , for example if user is writing new word and want save, but then change his mind, he can use this command. In this case word will be not save.
 - `/new` - Creation of a new word and its translation. At the beginning of this process, the bot requests a word in English, only letters of the English alphabet are accepted. Then the bot asks to translate this word into Russian, but the bot does not check the correctness of the translation, the user is responsible for this, and only Russian letters are accepted.
 - `/words` - Show a list of saved words.
 - `/translate <word or phrase>` - Translates word specifite after /translate command, you must enter the word or phrase to translate after the command.
If after the `translate` command a phrase/word is entered in Russian, the bot will respond with an English translation and vice versa.
Responce containe transalte and pronunciation word.
- `/info` - Description commands
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
