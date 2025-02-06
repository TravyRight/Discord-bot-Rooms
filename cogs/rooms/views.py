import disnake

from cogs.rooms.info import rooms, buttons


class RoomsView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for key in buttons.keys():
            button = disnake.ui.Button(
                emoji=buttons[key],
                custom_id=key
            )
            self.add_item(button)


class DialogButtons(disnake.ui.View):
    def __init__(self, inter: disnake.Interaction, member: disnake.Member, msg: disnake.Message):
        super().__init__(timeout=None)
        self.inter = inter
        self.member = member
        self.msg = msg

    @disnake.ui.button(label="Передать", style=disnake.ButtonStyle.green)
    async def accept(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        room_id = rooms[inter.user.id]
        rooms.pop(inter.user.id)
        rooms.update({self.member.id: room_id})

        embed = disnake.Embed(
            description=f"**Права** на комнату **переданы** пользователю {self.member.mention}",
            color=disnake.Color.green()
        )

        await self.msg.edit(embed=embed, view=None)

    @disnake.ui.button(label="Отмена", style=disnake.ButtonStyle.red)
    async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(
            description=f"**Права** на комнату **не будут переданы** пользователю {self.member.mention}",
            color=disnake.Color.green()
        )

        await self.msg.edit(embed=embed, view=None)
