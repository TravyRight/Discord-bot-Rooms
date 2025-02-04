import disnake

from cogs.rooms.info import rooms


class RoomsView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    def interaction_check(self, inter: disnake.MessageInteraction) -> bool:
        if inter.user.id not in rooms.keys():
            """
            embed = disnake.Embed(
                description="У вас нет комнаты"
            )
            await inter.send(embed=embed, ephemeral=True)
            """
            return False

    @disnake.ui.button(emoji="❌")
    async def up_the_room(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()

        room = inter.guild.get_channel(rooms[inter.user.id])
        room.position = 0

    @disnake.ui.button(emoji="❌")
    async def button2(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button3(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button4(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button5(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button6(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button7(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button8(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button9(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

    @disnake.ui.button(emoji="❌")
    async def button10(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        pass

