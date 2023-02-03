import hikari, lightbulb, requests, time, random, json as j, os

bot = lightbulb.BotApp("") #<- replace with token here

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")  

@bot.command
@lightbulb.option("text", "Text to use the TTS. Max is 1000.", required=True)
@lightbulb.command("synthesize", "Main synthesize command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def mainttscmd(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/text-to-speech/" + ctx.options.voice_id
    headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': #replace with the API key here,
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
bot.run()
