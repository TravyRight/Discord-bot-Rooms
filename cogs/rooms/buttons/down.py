import disnake


async def rooms_button_down(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    await inter.response.defer()
    await room.edit(position=1000)

    embed = disnake.Embed(
        description="Комната убрана вниз",
        color=disnake.Color.green()
    )

    await inter.send(embed=embed, ephemeral=True)
