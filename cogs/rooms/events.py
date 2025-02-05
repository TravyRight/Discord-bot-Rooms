import disnake
from disnake.ext import commands

from config import cur, bot
from cogs.rooms.info import rooms, buttons

from cogs.rooms.buttons.up import rooms_button_up
from cogs.rooms.buttons.slots import rooms_button_slots
from cogs.rooms.buttons.name import rooms_button_name
from cogs.rooms.buttons.kick import rooms_button_kick
from cogs.rooms.buttons.access import rooms_button_access
from cogs.rooms.buttons.down import rooms_button_down
from cogs.rooms.buttons.mute_unmute import rooms_button_mute_unmute
from cogs.rooms.buttons.open_close import rooms_button_open_close
from cogs.rooms.buttons.show_hide import rooms_button_show_hide
from cogs.rooms.buttons.give_room import rooms_button_give_room


class RoomsEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        """try:


        except Exception as e:
            print(e)
        """

        if before.channel == after.channel:
            return

        data = cur.execute("SELECT category_id, channel_create_id FROM guilds WHERE guild_id=?",
                           (member.guild.id,)).fetchone()

        if after.channel and after.channel.id == data["channel_create_id"]:
            new_channel = await member.guild.create_voice_channel(
                name=f"{member.name}",
                category=member.guild.get_channel(data["category_id"])
            )
            await member.move_to(new_channel)

            rooms.update({member.id: new_channel.id})

        if before.channel and before.channel.category.id == data["category_id"] and before.channel.id != data["channel_create_id"] and not before.channel.members:
            await before.channel.delete()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message):
        try:
            channel_settings_id = cur.execute("SELECT channel_settings_id FROM guilds").fetchone()[0]
            channel_settings = message.guild.get_channel(channel_settings_id)

            if message.channel.id == channel_settings.id and message.author.id != bot.user.id:
                await message.delete()

        except Exception as e:
            print(e)

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

            if custom_id in ["kick", "access", "mute_unmute", "give_room"]:
                channel_settings_id = int(cur.execute("SELECT channel_settings_id FROM guilds").fetchone()[0])
                channel_settings = inter.guild.get_channel(channel_settings_id)

                overwrites = channel_settings.overwrites_for(inter.user)
                overwrites.update(send_messages=True)

                await channel_settings.set_permissions(
                    target=inter.user,
                    overwrite=overwrites
                )

            elif custom_id in ["up"]:
                channel_create_id = int(cur.execute("SELECT channel_create_id FROM guilds").fetchone()[0])
                channel_create = inter.guild.get_channel(channel_create_id)

            else:
                channel_settings, channel_create = None, None

            room = inter.guild.get_channel(rooms[inter.user.id])

            button_functions = {
                "up": lambda: rooms_button_up(inter, room, channel_create),
                "slots": lambda: rooms_button_slots(inter, room),
                "name": lambda: rooms_button_name(inter, room),
                "kick": lambda: rooms_button_kick(inter, room, channel_settings),
                "access": lambda: rooms_button_access(inter, room, channel_settings),
                "down": lambda: rooms_button_down(inter, room),
                "mute_unmute": lambda: rooms_button_mute_unmute(inter, room, channel_settings),
                "open_close": lambda: rooms_button_open_close(inter, room),
                "show_hide": lambda: rooms_button_show_hide(inter, room),
                "give_room": lambda: rooms_button_give_room(inter, room, channel_settings),
            }

            await button_functions[custom_id]()

            if custom_id in ["kick", "access", "mute_unmute", "give_room"]:
                overwrites = channel_settings.overwrites_for(inter.user)
                overwrites.update(send_messages=True)

                await channel_settings.set_permissions(
                    target=inter.user,
                    overwrite=overwrites
                )


def setup(bot: commands.Bot):
    bot.add_cog(RoomsEvents(bot))
