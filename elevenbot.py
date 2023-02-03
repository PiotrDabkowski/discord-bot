import hikari, lightbulb, requests, time, random, json as j, os

bot = lightbulb.BotApp("")

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")

#TODO: If user is on starter, tell user they must upgrade the plan to use the bot, otherwise the bot will send a 45 byte audio file (typically means it failed)    

@bot.command
@lightbulb.option("apikey", "Your ElevenLabs API key. This key is NEVER stored anywhere and is only used to lookup your profile.")
@lightbulb.option("sendasjson", "Sends output as a JSON.", type=bool, required=True)
@lightbulb.command("subscription", "Tells you more info about your current subscription.")
@lightbulb.implements(lightbulb.SlashCommand)
async def subscriptioninfo(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/user/subscription"
    headers = {
        'accept': 'application/json',
        'xi-api-key': ctx.options.apikey
    }
    r = requests.get(site, headers=headers)
    if ctx.options.sendasjson == True:
        await ctx.respond(r.json())
        return
    else:
        await ctx.respond(f"Current tier: {r.json()['tier']}\nTotal character count: {r.json()['character_count']}\nMax character limit: {r.json()['character_limit']}\nCan user extend character limit?: {r.json()['can_extend_character_limit']}\nIs user allowed to extend character limit?: {r.json()['allowed_to_extend_character_limit']}\nNext character count reset: {r.json()['next_character_count_reset_unix']}\nVoice limit: {r.json()['voice_limit']}\nCan user extend voice limit?: {r.json()['can_extend_voice_limit']}\nCan user use instant voice cloning?: {r.json()['can_use_instant_voice_cloning']}\nAmount due (in cents): {r.json()['next_invoice']['amount_due_cents']}\nTime until next payment attempt: {r.json()['next_invoice']['next_payment_attempt_unix']}")
        return

@bot.command
@lightbulb.option("apikey", "Your ElevenLabs API key. This key is NEVER stored anywhere and is only used to lookup your profile.")
@lightbulb.command("history", "Sends history.")
@lightbulb.implements(lightbulb.SlashCommand)
async def historycmd(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/history"
    headers = {
        'accept': 'application/json',
        'xi-api-key': ctx.options.apikey
    }
    r = requests.get(site, headers=headers)
    await ctx.respond("Getting history...")
    time.sleep(2)
    fileobj = j.dumps(r.json(), indent=4)
    with open("history.json", 'w') as outfile:
        outfile.write(fileobj)
    f = hikari.File("history.json")
    await ctx.edit_last_response(f)
    os.remove("history.json")

@bot.command
@lightbulb.option("apikey", "Your ElevenLabs API key. This key is NEVER stored anywhere and is only used to lookup your profile.")
@lightbulb.command("voices", "Gets a list of all voices, custom and conversational that are on your account.")
@lightbulb.implements(lightbulb.SlashCommand)
async def voicelistcmd(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/voices"
    headers = {
        'accept': 'application/json',
        'xi-api-key': ctx.options.apikey
    }
    r = requests.get(site, headers=headers)
    await ctx.respond("Listed voices tied to your account are below: ")
    time.sleep(0.50)
    fileobj = j.dumps(r.json(), indent=4)
    with open("voices.json", 'w') as outfile:
        outfile.write(fileobj)
    f = hikari.File("voices.json")
    await ctx.edit_last_response(f)
    os.remove("voices.json")

@bot.command
@lightbulb.option("apikey", "Your ElevenLabs API key. This key is NEVER stored anywhere and is only used to lookup your profile.", required=True)
@lightbulb.option("voice_id", "The ID of the voice. Run '/voices' for a list of voices.", required=True)
@lightbulb.command("voicesettings", "View your voices current settings.")
@lightbulb.implements(lightbulb.SlashCommand)
async def voicesettingsbyID(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/voices/" + ctx.options.voice_id + '/settings'
    headers = {
    'accept': 'application/json',
    'xi-api-key': ctx.options.apikey
    }
    r = requests.get(site, headers=headers)
    if r.status_code == 401:
        await ctx.respond("Invalid API key! Please make sure your API key was entered correctly or was not stolen!")
        return
    else:
        await ctx.respond(f"Current voice settings for ID [{ctx.options.voice_id}]: ⏰")
        time.sleep(0.50)
        await ctx.edit_last_response(f"Stability = {str(r.json()['stability'])}\nSimilarity = {str(r.json()['similarity_boost'])}")

@bot.command
@lightbulb.command("findapikey", "A command of where to find your API key.")
@lightbulb.implements(lightbulb.SlashCommand)
async def apikeylocatecmd(ctx: lightbulb.context.Context):
    randcolor = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    embed = hikari.Embed(title="How do I find my API key?", color=randcolor)
    embed.add_field(name="Follow the instructions below:", value="**If you have an account**, go to your profile and click the eye, then copy the key. **If you don't have an account**, you can sign up for free, then do the same thing, go to your profile, click the eye, then copy the key.")
    await ctx.respond(embed)

@bot.command
@lightbulb.option("apikey", "Your ElevenLabs API key. This key is NEVER stored anywhere and is only used to lookup your profile.", required=True)
@lightbulb.option("voice_id", "The ID of the voice you want to use. Run '/voices' for a list of voices.", required=True)
@lightbulb.option("text", "Text to use the TTS. Max is 1000.", required=True)
@lightbulb.command("synthesize", "Main synthesize command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def mainttscmd(ctx: lightbulb.context.Context):
    site = "https://api.elevenlabs.io/v1/text-to-speech/" + ctx.options.voice_id
    headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': ctx.options.apikey,
    'Content-Type': 'application/json'
    }
    r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
    audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
    with open(audiofilename, 'wb') as out:
        out.write(r.content)
    await ctx.respond("Done! Sending audio file...")
    f = hikari.File(audiofilename)
    await ctx.respond(f)
    return

bot.run()
