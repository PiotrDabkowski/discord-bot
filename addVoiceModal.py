import miru, hikari, yt_dlp, os, glob, traceback, requests

class AddVoiceModal(miru.Modal):
    name = miru.TextInput(label="Name of voice.", placeholder="Enter the name of the voice you want here!", style=hikari.TextInputStyle.SHORT, required=True, max_length=25)
    labels = miru.TextInput(label="Labels. Leave alone for default labels.", placeholder=None, style=hikari.TextInputStyle.SHORT, required=True, max_length=30, value='{"accent": "American"}')
    description = miru.TextInput(label="Description of your voice.", placeholder="Enter a description you want for your voice here! This is not required however.", style=hikari.TextInputStyle.PARAGRAPH, required=False, max_length=2000)
    link_to_voice = miru.TextInput(label="YouTube link for your voice.", placeholder="Paste your youtube link for your voice here!", style=hikari.TextInputStyle.SHORT, required=True, max_length=500)
    async def callback(self, ctx: miru.ModalContext) -> None:
        ytinput = self.link_to_voice.value
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }],
            }
            await ctx.respond("Attempting to create voice... ⏰")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ytinput])
            for file in glob.glob("*.mp3"):
                if os.path.exists(file):
                    os.rename(file, "voice.mp3")
            url = "https://api.elevenlabs.io/v1/voices/add"
            with open(f"{ctx.user.id}.txt", "r") as outfile:
                headers = {
                    "Accept": "application/json",
                    "xi-api-key": outfile.read()
                }
                outfile.close()
            data = {
                'name': self.name.value,
                'labels': self.labels.value if self.labels.value != "" else self.labels.value == '{"accent": "American"}',
                'description': self.description.value
            }
            files = [
                ('files', ('voice.mp3', open('voice.mp3', 'rb'), 'audio/mpeg'))
            ]
            r = requests.post(
                url,
                headers=headers,
                data=data,
                files=files
            )
            if r.ok != True:
                await ctx.respond(r.text)
            else:
                await ctx.respond(f"Hooray! Your new voice is now available to use under the name '{self.name.value}'!")
                os.remove("voice.mp3")
        except:
            await ctx.respond("Oops! An error occured!\n\n" + traceback.format_exc())

class AddVoiceModalView(miru.View):
    @miru.button(label="Start!", style=hikari.ButtonStyle.SUCCESS)
    async def model_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = AddVoiceModal(title="Add voice.")
        await ctx.respond_with_modal(modal)
