import hikari, lightbulb, requests, random, os, time, json as j, miru, asyncio
from loginModal import ModalView

bot = lightbulb.BotApp("")
miru.install(bot)

@bot.listen(hikari.StartedEvent)
async def on_ready(event):
    print("Ready!")

@bot.command
@lightbulb.option("use_stream", "Whether or not to use the audio stream method, which might be faster, but could break at any time.", required=True, type=bool)
@lightbulb.option("text", "The text to synthesize.")
@lightbulb.command("favorite-synthesize", "Synthesize using favorite voice ID.")
@lightbulb.implements(lightbulb.SlashCommand)
async def favsynthesizecmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}-favorite.txt"):
        await ctx.respond("No favorite detected! Set a favorite up first.")
        return
    elif not os.path.exists(f"{ctx.user.id}.txt"):
        await ctx.respond("You are not logged in! Please run '/login' to continue.")
        return
    else:
        await ctx.respond("WARNING: This command will be renamed to 'synthesize' in a future update to ElevenBot!")
        time.sleep(3)
        with open(f"{ctx.user.id}-favorite.txt", 'r') as favid:
            if ctx.options.use_stream == True:
                site = "https://api.elevenlabs.io/v1/text-to-speech/" + favid.read() + '/stream'
            else:
                site = "https://api.elevenlabs.io/v1/text-to-speech/" + favid.read()
            favid.close()
        with open(f"{ctx.user.id}.txt", 'r') as outfile:
            headers = {
            'accept': 'audio/mpeg',
            'xi-api-key': outfile.read(),
            'Content-Type': 'application/json'
            }
        if len(ctx.options.text) >= 1000:
            await ctx.respond("Text is more than 1000 characters! Please try a shorter sentence.")
            return
        else:
            await ctx.respond("Sending request... ⏰")
            await asyncio.sleep(0.50)
            await ctx.edit_last_response("Sending request... ⏰\n\nIf this takes more than **5 seconds**, some heavy site traffic is happening.")
            r = requests.post(site, json={"text": f"{ctx.options.text}"}, headers=headers)
            if r.json()['detail']['status'] == "unauthorized":
                await ctx.edit_last_response("ERROR: Your subscription does not allow you to synthesize custom voices! Are you on 'Starter' or above?")
                return
            else:
                await ctx.edit_last_response("Checking if voice ID is valid... ⏰")
                if r.status_code == 400:
                    await ctx.edit_last_response("ERROR: Entered voice ID does not exist! Did you enter the ID correctly?")
                    return
                else:
                    await ctx.edit_last_response("Voice ID is valid! ✅")
                    audiofilename = "audio-" + str(random.randint(1, 372855)) + ".mp3"
                    with open(audiofilename, 'wb') as out:
                        out.write(r.content)
                    await ctx.respond(f"Done ✅! Sending audio file...\nYou have used {len(ctx.options.text)} characters.")
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
@lightbulb.option("voice_id", "The voice ID you want to add to the favorites.")
@lightbulb.command("set-favorite", "Set a voice ID to favorites. Run '/favorite-synthesize' to use your favorite voice ID.")
@lightbulb.implements(lightbulb.SlashCommand)
async def favcmd(ctx: lightbulb.context.Context):
    if os.path.exists(f"{ctx.user.id}-favorite.txt"):
        await ctx.respond("You can only save one voice ID per favorite! To remove a favorite, run '/remove-favorite'.")
        return
    else:
        with open(f"{ctx.user.id}-favorite.txt", 'w') as favwrite:
            favwrite.write(ctx.options.voice_id)
            favwrite.close()
        await ctx.respond("Favorite voice ID set! Now, you can use the '/favorite-synthesize' command to synthesize without needing to provide a voice ID!")
        return

@bot.command
@lightbulb.command("remove-favorite", "Removes the voice ID from your favorites.")
@lightbulb.implements(lightbulb.SlashCommand)
async def removefavcmd(ctx: lightbulb.context.Context):
    if not os.path.exists(f"{ctx.user.id}-favorite.txt"):
        await ctx.respond("You do not have a favorite voice ID set!")
        return
    else:
        os.remove(f"{ctx.user.id}-favorite.txt")
        await ctx.respond("Favorite list removed! ✅")
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
        await ctx.edit_last_response(f"User info for user {ctx.user.username}:\n\nSubscription: {r.json()['subscription']['tier']}\nCharacter count: {r.json()['subscription']['character_count']}\nCharacter limit: {r.json()['subscription']['character_limit']}\nCan user extend character limit? {r.json()['subscription']['can_extend_character_limit']}\nIs user allowed to extend character limit? {r.json()['subscription']['allowed_to_extend_character_limit']}\nTime until next character reset (in unix): {r.json()['subscription']['next_character_count_reset_unix']}\nVoice limit: {r.json()['subscription']['voice_limit']}\nCan user extend voice limit? {r.json()['subscription']['can_extend_voice_limit']}\nCan user use instant voice cloning? {r.json()['subscription']['can_use_instant_voice_cloning']}\nIs user a new user? {r.json()['is_new_user']}")
        
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
