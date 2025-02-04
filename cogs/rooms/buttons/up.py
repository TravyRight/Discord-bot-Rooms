import disnake


async def rooms_button_up(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    await inter.response.defer()
    await room.edit(position=0)

    embed = disnake.Embed(
        description="Комната поднята вверх",
        color=disnake.Color.green()
    )

    await inter.send(embed=embed, ephemeral=True)
