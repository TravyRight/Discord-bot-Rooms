import disnake
from disnake.ext import commands
from disnake import TextInputStyle

import time

from cogs.rooms.info import rooms, buttons
from config import bot, cur

from cogs.rooms.buttons.up import rooms_button_up
from cogs.rooms.buttons.slots import rooms_button_slots
from cogs.rooms.buttons.name import rooms_button_name
from cogs.rooms.buttons.kick import rooms_button_kick
from cogs.rooms.buttons.access import rooms_button_access
from cogs.rooms.buttons.down import rooms_button_down
from cogs.rooms.buttons.mute_unmute import rooms_button_mute_unmute


class RoomsView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        for key in buttons.keys():
            button = disnake.ui.Button(
                emoji=buttons[key],
                custom_id=key
            )
            self.add_item(button)


class RoomsViewListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def rooms_listener(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id

        if custom_id not in buttons.keys():
            return

        if inter.user.id not in rooms.keys():
            embed = disnake.Embed(
                description="**У вас нет комнаты",
                color=disnake.Color.red()
            )
            await inter.send(embed=embed, ephemeral=True)
            return

        if custom_id in ["kick", "access", "mute_unmute"]:
            channel_settings_id = int(cur.execute("SELECT channel_settings_id FROM guilds").fetchone()[0])
            channel_settings = inter.guild.get_channel(channel_settings_id)

            overwrites = channel_settings.overwrites_for(inter.user)
            overwrites.update(send_messages=True)

            await channel_settings.set_permissions(
                target=inter.user,
                overwrite=overwrites
            )

        else:
            channel_settings = None

        room = inter.guild.get_channel(rooms[inter.user.id])

        button_functions = {
            "up": lambda: rooms_button_up(inter, room),
            "slots": lambda: rooms_button_slots(inter, room),
            "name": lambda: rooms_button_name(inter, room),
            "kick": lambda: rooms_button_kick(inter, room, channel_settings),
            "access": lambda: rooms_button_access(inter, room, channel_settings),
            "down": lambda: rooms_button_down(inter, room),
            "mute_unmute": lambda: rooms_button_mute_unmute(inter, room),
            "open_close": "",
            "show_hide": "",
            "give_license": "",
        }

        await button_functions[custom_id]()

        if custom_id in ["kick", "access", "mute_unmute"]:
            overwrites = channel_settings.overwrites_for(inter.user)
            overwrites.update(send_messages=True)

            await channel_settings.set_permissions(
                target=inter.user,
                overwrite=overwrites
            )


def setup(bot: commands.Bot):
    bot.add_cog(RoomsViewListener(bot))
