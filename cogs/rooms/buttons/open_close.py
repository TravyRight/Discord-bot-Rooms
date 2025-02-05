import disnake
import time

from disnake import TextInputStyle

from config import bot


async def rooms_button_open_close(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    await inter.response.defer()
    overwrites = room.overwrites_for(inter.guild.default_role)

    if overwrites.connect in [True, None]:
        overwrites.update(speak=False)
        embed = disnake.Embed(
            description="Комната закрыта",
            color=disnake.Color.green()
        )

    else:
        overwrites.update(speak=True)
        embed = disnake.Embed(
            description="Комната открыта",
            color=disnake.Color.green()
        )

    await room.set_permissions(
        target=inter.guild.default_role,
        overwrite=overwrites
    )

    await inter.send(embed=embed, ephemeral=True)
