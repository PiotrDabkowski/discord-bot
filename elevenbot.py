import hikari, lightbulb, requests, random, os, time, json as j, miru, asyncio, datetime, traceback, urllib3
urllib3.disable_warnings()
from loginModal import ModalView
from addVoiceModal import AddVoiceModalView

bot = lightbulb.BotApp("")
miru.install(bot)

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")

@bot.command
@lightbulb.option("model_type", "Type of model to use. Defaults to eleven_monolingual_v1.", required=False, choices=["eleven_monolingual_v1", "eleven_multilingual_v1", "eleven_multilingual_v2", "eleven_english_v2"], default="eleven_monolingual_v1")
@lightbulb.option("text", "The text to synthesize.")
@lightbulb.command("synthesize", "Synthesize using saved voice ID.")
@lightbulb.implements(lightbulb.SlashCommand)
async def synthesizecmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}-id.txt"):
        await ctx.respond("No ID detected! Set up an ID up first.")
        return
    elif not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("You are not logged in! Please run '/login' to continue.")
        return
    else:
        with open(f"{ctx.user.id}-id.txt", 'r') as favid:
            site = "https://api.elevenlabs.io/v1/text-to-speech/" + favid.read()
            favid.close()
        with open(f"{ctx.user.id}.txt", 'r') as outfile:
            headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': outfile.read(),
            'Content-Type': 'application/json'
            }
        data = {
            "text": f"{ctx.options.text}",
            "model_id": ctx.options.model_type
        }
        if len(ctx.options.text) >= 1000:
            await ctx.respond("Text is more than 1000 characters! Please try a shorter sentence.")
            return
        else:
            await ctx.respond("Sending request... ⏰")
            r = requests.post(site, json=data, headers=headers)
            if r.ok != True:
                await ctx.edit_last_response(f"ERROR: Error traceback:\n\n{r.json()}")
                return
            else:
                await ctx.edit_last_response("Checking if voice ID is valid... ⏰")
                if r.status_code == 400:
                    await ctx.edit_last_response("ERROR: Entered voice ID does not exist! Did you enter the ID correctly?")
                    return
                else:
                    await ctx.edit_last_response("Voice ID is valid! ✅")
                    if ctx.options.audio_fx == "none":
                        await ctx.respond(f"Done ✅! Sending audio file...\nYou have used {len(ctx.options.text)} characters.")
                        audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
                        with open(audiofilename, 'wb') as out:
                            out.write(r.content)
                        f = hikari.File(audiofilename)
                        await ctx.respond(f)
                        os.remove(audiofilename)
                        return
                        
@bot.command
@lightbulb.command("logout", "If you really dont trust the bot saving your API key, you can logout and the bot will erase it.")
@lightbulb.implements(lightbulb.SlashCommand)
async def logoutcmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("File doesnt exist or has been deleted already!")
        return
    else:
        await ctx.respond("Deleting API key file... ⏰")
        os.remove(f"{ctx.user.id}.txt")
        await ctx.edit_last_response("Key deleted! ✅")

@bot.command
@lightbulb.option("voice_id", "The voice ID you want to set.")
@lightbulb.command("set-id", "Set a voice ID to favorites. Run '/synthesize' to use your favorite voice ID.")
@lightbulb.implements(lightbulb.SlashCommand)
async def favcmd(ctx: lightbulb.context.Context):
    if os.path.exists(f"{ctx.user.id}-id.txt"):
        await ctx.respond("You can only save one voice ID per favorite! To remove a favorite, run '/remove-id'.")
        return
    else:
        with open(f"{ctx.user.id}-id.txt", 'w') as favwrite:
            favwrite.write(ctx.options.voice_id)
            favwrite.close()
        await ctx.respond("Voice ID set! Now, you can use the '/synthesize' command to synthesize without needing to provide a voice ID!")
        return

@bot.command
@lightbulb.command("support", "Support the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def supportcmd(ctx: lightbulb.context.Context):
    menu = miru.View()
    menu.add_item(miru.Button(label="Ko-fi", url="https://ko-fi.com/acmesupplier"))
    btnmsg = (await ctx.respond("If you want to support the bot and get access to a premium bot with some future perks (faster inference time, etc), click one of the links below!\n\nEverything is still free and will be free, this is just if you want to support the bot's development.", components=menu.build())).message()
    await menu.start(await btnmsg)

@bot.command
@lightbulb.command("commands", "Lists all available commands.")
@lightbulb.implements(lightbulb.SlashCommand)
async def allcmds(ctx: lightbulb.context.Context):
    embed = hikari.Embed(title="Commands", description="See below for all my commands!")
    embed.add_field("/support", "Support the bot, and get access to a premium bot with more features.")
    embed.add_field("/commands", "This menu.")
    embed.add_field("/login", "Run this command to login to your elevenlabs profile.")
    embed.add_field("/logout", "Logout of your profile.")
    embed.add_field("/synthesize [text] [model_type]", "Synthesize audio using the given text and model type.")
    embed.add_field("/set-id [voice_id]", "Set up a voice ID.")
    embed.add_field("/remove-id", "Removes the saved ID.")
    embed.add_field("/voices", "Shows the voices you have on your account.")
    embed.add_field("/userinfo", "Shows your profile info.")
    embed.add_field("/addvoice", "Creates a voice and adds it to your profile.")
    await ctx.respond(embed=embed)

@bot.command
@lightbulb.command("remove-id", "Removes the voice ID.")
@lightbulb.implements(lightbulb.SlashCommand)
async def removefavcmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}-id.txt"):
        await ctx.respond("You do not have a voice ID set!")
        return
    else:
        os.remove(f"{ctx.user.id}-id.txt")
        await ctx.respond("ID list removed! ✅")
        return    

@bot.command
@lightbulb.command("userinfo", "Gets more info about character count, sub tier, etc")
@lightbulb.implements(lightbulb.SlashCommand)
async def userinfocmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("You are not logged in! Please run '/login' to continue.")
        return
    else:
        site = "https://api.elevenlabs.io/v1/user"
        with open(f"{ctx.user.id}.txt", 'r') as outfile:
            headers = {
                'accept': 'application/json',
                'xi-api-key': outfile.read()
            }
            outfile.close()
        await ctx.respond("Getting user info... ⏰")
        r = requests.get(site, headers=headers)
        await ctx.edit_last_response(f"User info for user {ctx.user.username}:\n\nSubscription: {r.json()['subscription']['tier']}\nCharacter count: {r.json()['subscription']['character_count']}\nCharacter limit: {r.json()['subscription']['character_limit']}\nCan user extend character limit? {r.json()['subscription']['can_extend_character_limit']}\nIs user allowed to extend character limit? {r.json()['subscription']['allowed_to_extend_character_limit']}\nTime until next character reset (in datetime format): {datetime.datetime.fromtimestamp(int(r.json()['subscription']['next_character_count_reset_unix'])).strftime('%m-%d-%Y %H:%M:%S')}\nVoice limit: {r.json()['subscription']['voice_limit']}\nCan user extend voice limit? {r.json()['subscription']['can_extend_voice_limit']}\nCan user use instant voice cloning? {r.json()['subscription']['can_use_instant_voice_cloning']}\nIs user a new user? {r.json()['is_new_user']}")
        
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
@lightbulb.command("beta-addvoice", "This is a beta command. Adds a voice to your profile.")
@lightbulb.implements(lightbulb.SlashCommand)
async def addvoicecmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("Key not found! Please run '/login' first!")
        return
    else:
        for file in glob.glob("*.mp3"):
            if os.path.exists(file):             
                os.remove(file)
            elif os.path.exists("voice.mp3"):
                os.remove("voice.mp3")
        view = AddVoiceModalView()
        message = await ctx.respond("Click the button below to start adding a voice!\n\n**Please note, this command is in beta, and as such may be removed or kept in a future update.**", components=view)
        await view.start(message)
        
@bot.command
@lightbulb.command("login", "Login using your API key.")
@lightbulb.implements(lightbulb.SlashCommand)
async def logincmd(ctx: lightbulb.context.Context):
    if os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("No need to login again! You are already logged in.")
        return
    else:
        view = ModalView()
        message = await ctx.respond("Click the button below to sign in.\n\n**This info will have to be saved but will only be used to validate your profile.**", components=view)
        await view.start(message)

bot.run(
    activity=hikari.Activity(
        name="AI voices.",
        type=hikari.ActivityType.LISTENING
    ),
    ignore_session_start_limit=True,
    check_for_updates=False,
    status=hikari.Status.ONLINE,
    coroutine_tracking_depth=20,
    propagate_interrupts=True
)
