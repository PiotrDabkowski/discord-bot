import miru, hikari

class SuggestModal(miru.Modal):
    userid = miru.TextInput(label="User ID", placeholder="Enter your user ID here only if you want to be credited.", style=hikari.TextInputStyle.SHORT, required=False)
    suggestion = miru.TextInput(label='Suggestion', placeholder="Enter your suggestion here! If I do add the feature, I will credit you for it!", style=hikari.TextInputStyle.PARAGRAPH, required=True, max_length=4000)
    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.respond("Sending suggestion to owner... ⏰")
        suggestionDM = await ctx.bot.rest.create_dm_channel(414558788092428299)
        await suggestionDM.send(f"({self.userid.value if self.userid.value != '' else 'An anonymous user'}) suggested this: '{self.suggestion.value}'")
        await ctx.edit_response("Suggestion sent! ✅")

class ModalView(miru.View):
    @miru.button(label="Suggest!", style=hikari.ButtonStyle.SUCCESS)
    async def modal_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = SuggestModal(title="Suggest ideas here!")
        await ctx.respond_with_modal(modal)