import hikari, lightbulb, requests, time, random, json as j, os

bot = lightbulb.BotApp("") #<- replace with token here

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")  

@bot.command
@lightbulb.option("voice", "The voice to use using the default API key. To use your custom voices, use the '/custom-synthesize' command.", required=True, choices=["Adam", "Antoni", "Arnold", "Bella", "Josh", "Rachel", "Domi", "Elli", "Sam"])
@lightbulb.option("text", "Text to use the TTS. Max is 1000.", required=True)
@lightbulb.command("synthesize", "Main synthesize command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def mainttscmd(ctx: lightbulb.context.Context):
    if ctx.options.voice == "Adam":
        site = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
    elif ctx.options.voice == "Antoni":
        site = "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV"
    elif ctx.options.voice == "Arnold":
        site = "https://api.elevenlabs.io/v1/text-to-speech/VR6AewLTigWG4xSOukaG"
    elif ctx.options.voice == "Bella":
        site = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"
    elif ctx.options.vocie == "Josh":
        site = "https://api.elevenlabs.io/v1/text-to-speech/TxGEqnHWrfWFTfGW9XjX"
    elif ctx.options.voice == "Rachel":
        site = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
    elif ctx.options.voice == "Domi":
        site = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"
    elif ctx.options.voice == "Elli":
        site = "https://api.elevenlabs.io/v1/text-to-speech/MF3mGyEYCl7XYWbV9V6O"
    elif ctx.options.voice == "Sam":
        site = "https://api.elevenlabs.io/v1/text-to-speech/yoZ06aMxZJJ28mfd3POQ"
    headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': #to devs, add your api key here,
    'Content-Type': 'application/json'
    }
    if len(ctx.options.text) > 1000:
        await ctx.respond("WARNING: Text is over 1000 characters! Please try a sentence less than 1000 characters.")
        return
    else:
        r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
        audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
        with open(audiofilename, 'wb') as out:
            out.write(r.content)
        await ctx.respond("Done! Sending audio file...")
        f = hikari.File(audiofilename)
        await ctx.respond(f)
        return

@bot.command
@lightbulb.option("voice_id", "Use your custom voices using your own API key.", required=True)
@lightbulb.option("apikey", "Enter your own API key here. Only use this command if you want to synthesize using your custom voices.", required=True)
@lightbulb.option("text", "The text to synthesize. Max 1000 characters", required=True)
@lightbulb.command("custom-synthesize", "Use your own API key to synthesize your custom voices.")
@lightbulb.implements(lightbulb.SlashCommand)
async def customsynthesize(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/text-to-speech/" + ctx.options.voice_id
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': ctx.options.apikey,
        'Content-Type': 'application/json'
    }
    if len(ctx.options.text) > 1000:
        await ctx.respond("WARNING: Text is over 1000 characters! Please try a sentence less than 1000 characters.")
        return
    else:
        r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
        audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
        with open(audiofilename, 'wb') as out:
            out.write(r.content)
        await ctx.respond("Done! Sending audio file...")
        f = hikari.File(audiofilename)
        await ctx.respond(f)
        os.remove(audiofilename)
        return

bot.run()
