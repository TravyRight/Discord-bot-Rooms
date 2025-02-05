import disnake


async def rooms_button_up(inter: disnake.Interaction, room: disnake.VoiceChannel, channel_create: disnake.VoiceChannel) -> None:
    await inter.response.defer()
    await room.edit(position=channel_create.position + 1)

    embed = disnake.Embed(
        description="Комната перемещена вверх",
        color=disnake.Color.green()
    )

    await inter.send(embed=embed, ephemeral=True)
