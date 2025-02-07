def is_member(member_id: int | str) -> bool:
    if member_id.isalpha():
        return False

    member = inter.guild.get_member(int(member_id))

    if member is None:
        embed = disnake.Embed(
            description=f"Нет такого пользователя",
            color=disnake.Color.green()
        )
        await msg.edit(embed=embed)
        return False