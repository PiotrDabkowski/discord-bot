# ElevenBot

### This bot interacts with ElevenLabs API.

To use the code for your own bot, add your bots token in line 4. You also must be on the "Starter" plan or above to use custom voices. You can still use the bot on the "Free" plan, but only the premade voices.

# Bugs

There might some bugs, but the most known ones are:
1. Request will fail and send a less than normal audio file that is 0 seconds long. (**This has been mostly fixed**)
2. The beta command (add-voice) might break if the video is too long. (**This has an error message backup if it does fail**)
3. Sometimes, upon setting an ID and using the synthesize command and selecting the wrong model, the bot will error out. (**Still needs to test if this happens**)
4. If the bot responds with "NoneType: None", that would mean your voice is incompatible with your current plan. (**Need to find an easier way to check the current plan**)

If there are any other bugs that I don't know about, either make an issue in this repo or DM me on Discord.

---

~~Multilingual model support will come in a future update to the bot.~~ **Multilingual models are now supported.**

## This bot will require you to input your API key to login and it will be saved. This will never be used for malicious purpose however. 

I will never use your API key for anything malicious. 

## If you really dont trust this though, if you have previously logged in, you can run '/logout' to remove the key from storage.

#### If any issues happen with the bot, please DM @hawtcawfee. (discord username haha totally not a bad decision)
