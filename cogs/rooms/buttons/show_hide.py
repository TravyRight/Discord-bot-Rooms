import disnake
import time

from disnake import TextInputStyle

from config import bot


async def rooms_button_show_hide(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    await inter.response.defer()
    overwrites = room.overwrites_for(inter.guild.default_role)

    if overwrites.view_channel in [True, None]:
        overwrites.update(view_channel=False)
        embed = disnake.Embed(
            description="Комната скрыта",
            color=disnake.Color.green()
        )

    else:
        overwrites.update(view_channel=True)
        embed = disnake.Embed(
            description="Комната видна всем пользователям",
            color=disnake.Color.green()
        )

    await room.set_permissions(
        target=inter.guild.default_role,
        overwrite=overwrites
    )

    await inter.send(embed=embed, ephemeral=True)
