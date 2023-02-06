import miru, hikari, time, requests

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
        r = requests.get(site, headers=headers)
        if r.status_code == 200:
            with open(f"{ctx.user.id}.txt", 'w') as validate:
                validate.write(self.apikey.value)
                validate.close()
            await ctx.edit_response(f"API key validated ✅! Welcome {ctx.user.username}#{ctx.user.discriminator}!")
        elif r.status_code == 401:
            await ctx.edit_response("API key not validated ❌! Please enter a valid API key!")

class ModalView(miru.View):
    @miru.button(label="Log in", style=hikari.ButtonStyle.SUCCESS)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = LoginModal(title="API Log in")
        await ctx.respond_with_modal(modal)