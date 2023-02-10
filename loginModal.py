import miru, hikari, time, requests, json as j

class LoginModal(miru.Modal):
    apikey = miru.TextInput(label="API key", placeholder="Enter your API key here!", style=hikari.TextInputStyle.SHORT, required=True)
    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.respond("Logging in... ⏰")
        time.sleep(1)
        await ctx.edit_response("Validating API key... ⏰")
        site = "https://api.elevenlabs.io/v1/user"
        headers = {
            'accept': 'application/json',
            'xi-api-key': self.apikey.value
        }
        site2 = "https://api.elevenlabs.io/v1/voices"
        headers2 = {
            'accept': 'application/json',
            'xi-api-key': self.apikey.value
        }
        r = requests.get(site, headers=headers)
        r2 = requests.get(site2, headers=headers2)
        if r.status_code == 200:
            with open(f"{ctx.user.id}.txt", 'w') as validate:
                validate.write(self.apikey.value)
                validate.close()
            await ctx.edit_response(f"API key validated ✅! Adding voice list... ⏰")

            with open(f"voicelist-{ctx.user.discriminator}.txt", 'w') as l:
                l.write(r2.text)

            with open(f"voicelist-{ctx.user.discriminator}.txt", 'r') as f1:
                data = f1.read()
                data = data.split("voice_id")
                data = data[1:]
                for i in range(len(data)):
                    data[i] = data[i].split('"')[2]
                with open(f"voicelist-{ctx.user.discriminator}.txt", 'w') as f3:
                    f3.write(j.dumps(data))

            with open(f"voicelist-{ctx.user.discriminator}.txt", 'r') as f4:
                data = f4.read()
                data = data.replace("[", "").replace("]", "").replace(",", "").split('"')
                with open(f"voicelist-{ctx.user.discriminator}.txt", "w") as f5:
                    for i in data:
                        f5.write(i + "\n")

            with open(f"voicelist-{ctx.user.discriminator}.txt", "r") as f6:
                data = f6.readlines()
                data = [i for i in data if i != "\n"]
                with open(f"voicelist-{ctx.user.discriminator}.txt", "w") as txtfile:
                    for v in data:
                        txtfile.write(v)

            await ctx.edit_response("Done! ✅")
        elif r.status_code == 401:
            await ctx.edit_response("API key not validated ❌! Please enter a valid API key!")

class ModalView(miru.View):
    @miru.button(label="Log in", style=hikari.ButtonStyle.SUCCESS)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = LoginModal(title="API Log in")
        await ctx.respond_with_modal(modal)
