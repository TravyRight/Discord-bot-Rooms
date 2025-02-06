import disnake
import time

from disnake import TextInputStyle

from config import bot


async def rooms_button_access(inter: disnake.Interaction, room: disnake.VoiceChannel, channel_settings: disnake.TextChannel) -> bool:
    await inter.response.defer()

    embed = disnake.Embed(
        description="Напишите никнейм пользователя, у которого нужно забрать/выдать доступ.\n"
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

    member = inter.guild.get_member(int(str(message.content)[2:-1]))
    overwrites = room.overwrites_for(member)

    if overwrites.connect in [True, None]:
        overwrites.update(connect=False)
        embed = disnake.Embed(
            description=f"{member} больше не сможет зайти в вашу комнату",
            color=disnake.Color.green()
        )

    else:
        overwrites.update(connect=True)
        embed = disnake.Embed(
            description=f"{member} снова может зайти в вашу комнату",
            color=disnake.Color.green()
        )

    await room.set_permissions(
        target=member,
        overwrite=overwrites
    )

    if member in room.members:
        await member.move_to(None)

    await msg.edit(embed=embed)
    return True
