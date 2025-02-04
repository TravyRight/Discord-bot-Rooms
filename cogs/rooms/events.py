from disnake.ext import commands

from config import cur
from cogs.rooms.info import rooms


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

        elif before.channel and before.channel.category.id == data["category_id"] and before.channel.id != data["channel_create_id"] and not before.channel.members:
            await before.channel.delete()


def setup(bot: commands.Bot):
    bot.add_cog(RoomsEvents(bot))
