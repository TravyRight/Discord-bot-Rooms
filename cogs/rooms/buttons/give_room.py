import disnake

from cogs.rooms.views import DialogButtons
from config import bot


async def rooms_button_give_room(inter: disnake.Interaction, room: disnake.VoiceChannel, channel_settings: disnake.TextChannel) -> bool:
    await inter.response.defer()

    embed = disnake.Embed(
        description="Напишите никнейм пользователя, которому хотите передать права на комнату.\n"
                    "Например: `@username`",
        color=disnake.Color.dark_embed()
    )

    embed.set_footer(
        text="На ответ у вас есть минута"
    )

    msg = await inter.followup.send(embed=embed, ephemeral=True)

    try:
        message = await bot.wait_for(
            event="message",
            check=lambda x: x.author.id == inter.user.id and x.channel.id == channel_settings.id,
            timeout=60
        )
    except TimeoutError:
        return False

    member_id = str(message.content)[2:-1]

    if not(member_id.isdigit()):
        embed = disnake.Embed(
            description=f"Неверный ID пользователя",
            color=disnake.Color.red()
        )
        await msg.edit(embed=embed)
        return False

    member = inter.guild.get_member(int(member_id))

    if member is None:
        embed = disnake.Embed(
            description=f"Нет такого пользователя",
            color=disnake.Color.red()
        )
        await msg.edit(embed=embed)
        return False

    embed = disnake.Embed(
        description=f"Вы действительно хотите передать права на комнату пользователю {member.mention}?",
        color=disnake.Color.dark_embed()
    )

    view = DialogButtons(inter, member, msg)

    await msg.edit(embed=embed, view=view)
    return True
