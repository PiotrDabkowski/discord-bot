import hikari, lightbulb, requests, random, os, time, json as j, miru
from loginModal import ModalView

bot = lightbulb.BotApp("")
miru.install(bot)

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")

@bot.command
@lightbulb.option("voice_id", "Voice ID to use. Run '/voices' for a list of voices you can use.", required=True)
@lightbulb.option("text", "Text to use the TTS. Max is 1000.", required=True)
@lightbulb.command("synthesize", "Main synthesize command.")
@lightbulb.implements(lightbulb.SlashCommand)
async def mainttscmd(ctx: lightbulb.context.Context):
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

@bot.command
@lightbulb.command("voices", "Gets a list of all voices that are on your account.")
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
        "About.",
        "This bot is an unofficial bot for ElevenLabs, an AI TTS website where you can make your own voices.\n\nThere are 3 commands for this bot: 'synthesize', 'login', and 'voices'.\n\nThe login command is required to use the bot. If you do not run this command first, you will not be able to use the bot to it's full extent. **Nothing you enter will be saved anywhere.** \n\nThe 'synthesize' command will let you use the voices, but only if you are logged in.\n\nThe 'voices' command will let you view all voices on your account, but just like the synthesize command, will only work if you are logged in."
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

bot.run(asyncio_debug=True)
