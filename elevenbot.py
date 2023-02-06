import hikari, lightbulb, requests, random, os, time, json as j, miru
from loginModal import ModalView

bot = lightbulb.BotApp("")
miru.install(bot)

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")

@bot.command
@lightbulb.option("voice", "The voice to use. To use your custom voices, use the '/custom-synthesize' command.", required=True, choices=["Adam", "Antoni", "Arnold", "Bella", "Josh", "Rachel", "Domi", "Elli", "Sam"])
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
    'xi-api-key': ctx.options.apikey,
    'Content-Type': 'application/json'
    }
    if len(ctx.options.text) > 1000:
        await ctx.respond("WARNING: Text is over 1000 characters! Please try a sentence less than 1000 characters.")
        return
    else:
        await ctx.respond("Sending request... ⏰")
        r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
        audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
        with open(audiofilename, 'wb') as out:
            out.write(r.content)
        await ctx.respond("Done ✅! Sending audio file...")
        f = hikari.File(audiofilename)
        await ctx.respond(f)
        return

@bot.command
@lightbulb.command("voices", "Gets a list of all voices, custom and conversational that are on your account.")
@lightbulb.implements(lightbulb.SlashCommand)
async def voicelistcmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("You are not logged in! Please run '/login' to continue.")
        return
    else:
        site = "https://api.elevenlabs.io/v1/voices"
        with open(f"{ctx.user.id}.txt", 'r') as outfile:
            headers = {
                'accept': 'application/json',
                'xi-api-key': outfile.read()
            }
            outfile.close()
        r = requests.get(site, headers=headers)
        await ctx.respond("Listed voices tied to your account are below: ")
        time.sleep(0.50)
        fileobj = j.dumps(r.json(), indent=4)
        with open("voices.json", 'w') as outfile:
            outfile.write(fileobj)
        f = hikari.File("voices.json")
        await ctx.respond(f)
        os.remove("voices.json")

@bot.command
@lightbulb.command("about", "Details about the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def aboutcmd(ctx: lightbulb.context.Context):
    randcolor = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    embed = hikari.Embed(
        title="About",
        description="About this bot.",
        color=randcolor
    ).add_field(
        "About the bot.",
        "This bot is an unofficial bot for ElevenLabs, an AI TTS website where you can make your own voices.\n\nThere are 2 modes for this bot: 'synthesize', and 'custom-synthesize'.\n\n1. The default command, 'synthesize', will let you use **only** the default voices for no cost of your quota.\n2. The 'custom-synthesize' command will let you use your own custom voices, but with a cost of your quota."
    ).set_footer(
        "This bot was made by @HawtCawfee☕#1337 in collaboration with ElevenLabs. If any issues arise, please contact @HawtCawfee☕#1337 first before contacting ElevenLabs."
    ).set_thumbnail("https://i.ibb.co/Gn6C0s5/1668126895443.jpg")
    await ctx.respond(embed)

@bot.command
@lightbulb.command("login", "Login using your API key.")
@lightbulb.implements(lightbulb.SlashCommand)
async def logincmd(ctx: lightbulb.context.Context):
    view = ModalView()
    message = await ctx.respond("Click the button below to sign in.\n\n**This info will never be saved anywhere and will only be used to validate your profile.**", components=view)
    await view.start(message)

@bot.command
@lightbulb.option("voice_id", "Voice ID to use. Run '/voices' for a list of voices you can use.", required=True)
@lightbulb.option("text", "The text to synthesize. Max 1000 characters", required=True)
@lightbulb.command("custom-synthesize", "Use your own API key to synthesize your custom voices.")
@lightbulb.implements(lightbulb.SlashCommand)
async def customsynthesize(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("You are not logged in! Please run '/login' to continue.")
        return
    else:
        site = "https://api.elevenlabs.io/v1/text-to-speech/" + ctx.options.voice_id
        with open(f"{ctx.user.id}.txt", 'r') as outfile:  
            headers = {
                'accept': 'audio/mpeg',
                'xi-api-key': outfile.read(),
                'Content-Type': 'application/json'
            }
            outfile.close()
        if len(ctx.options.text) > 1000:
            await ctx.respond("WARNING: Text is over 1000 characters! Please try a sentence less than 1000 characters.")
            return
        else:
            await ctx.respond("Sending request... ⏰")
            r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
            audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
            with open(audiofilename, 'wb') as out:
                out.write(r.content)
            await ctx.respond("Done ✅! Sending audio file...")
            f = hikari.File(audiofilename)
            await ctx.respond(f)
            os.remove(audiofilename)
            return

bot.run(asyncio_debug=True)
