import disnake

from cogs.rooms.views import DialogButtons
from config import bot


async def rooms_button_give_room(inter: disnake.Interaction, room: disnake.VoiceChannel, channel_settings: disnake.TextChannel) -> None:
    await inter.response.defer()

    embed = disnake.Embed(
        description="Напишите никнейм участника, которому хотите передать права на комнату.\n"
                    "Например: `@username`",
        color=disnake.Color.dark_embed()
    )

    embed.set_footer(
        text="На ответ у вас есть минута"
    )

    msg = await inter.followup.send(embed=embed, ephemeral=True)

    message = await bot.wait_for(
        event="message",
        check=lambda x: x.author.id == inter.user.id and x.channel.id == channel_settings.id,
        timeout=60
    )

    member = inter.guild.get_member(int(str(message.content)[2:-1]))

    embed = disnake.Embed(
        description=f"Вы действительно хотите передать права на комнату участнику {member.mention}?",
        color=disnake.Color.dark_embed()
    )

    view = DialogButtons(member, msg)

    await msg.edit(embed=embed, view=view)
