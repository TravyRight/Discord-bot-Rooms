import disnake
from disnake.ext import commands
from disnake import Localized

from cogs.rooms.views import RoomsView
from config import conn, cur


class RoomsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name=Localized(key="CREATE_ROOMS_NAME"), description=Localized(key="CREATE_ROOMS_DESCRIPTION"))
    @commands.has_permissions(administrator=True)
    async def create_rooms(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        guild = inter.guild

        category = await guild.create_category(
            name="комнаты"
        )

        channel_settings = await guild.create_text_channel(
            name="📝┃управление",
            category=category
        )

        await channel_settings.set_permissions(
            target=guild.default_role,
            send_messages=False
        )

        channel_create = await guild.create_voice_channel(
            name="➕┃создать",
            category=category
        )

        embed = disnake.Embed(
            title="Настройки",
            description="**Выберите, что хотите изменить и нажмите на нужную кнопку**\n"
                        "\n"
                        " — `Поднять комнату`\n"
                        " — `Опустить комнату вниз`\n"
                        " — `Установить кол-во слотов`\n"
                        " — `Сменить название`\n"
                        " — `Кикнуть участника`\n"
                        " — `Забрать/Выдать доступ участнику`\n"
                        " — `Замутить/Размутить участника`\n"
                        " — `Открыть/Закрыть комнату`\n"
                        " — `Показать/Скрыть комнату`\n"
                        " — `Передать все права на комнату`\n",
            color=disnake.Color.dark_embed()
        )

        if cur.execute("SELECT COUNT(*) FROM guilds WHERE guild_id=?", (inter.guild.id,)).fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO guilds(guild_id, category_id, channel_create_id, channel_setting_id) VALUES(?, ?, ?, ?)",
                (
                    inter.guild.id,
                    category.id,
                    channel_create.id,
                    channel_settings.id
                )
            )

        else:
            cur.execute(
                "UPDATE guilds SET category_id=?, channel_create_id=?, channel_setting_id=? WHERE guild_id=?",
                (
                    category.id,
                    channel_create.id,
                    channel_settings.id,
                    inter.guild.id
                )
            )

        conn.commit()

        view = RoomsView()
        await channel_settings.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(RoomsCommands(bot))
