import disnake
import time

from disnake import TextInputStyle

from config import bot


async def rooms_button_name(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    custom_id = f"modal.rooms.slots.{inter.user.id}.{round(time.time())}"

    await inter.response.send_modal(
        title="Комната",
        custom_id=custom_id,
        components=[
            disnake.ui.TextInput(
                label="Название",
                custom_id=f"{custom_id}.name",
                style=TextInputStyle.short,
            )
        ]
    )

    try:
        modal_inter: disnake.ModalInteraction = await bot.wait_for(
            event="modal_submit",
            check=lambda x: x.custom_id == custom_id,
            timeout=60,
        )
    except:
        return

    new_name = modal_inter.text_values[f"{custom_id}.name"]
    await room.edit(name=new_name)

    embed = disnake.Embed(
        description=f"Название изменено на `{new_name}`",
        color=disnake.Color.green()
    )
    await modal_inter.send(embed=embed, ephemeral=True)
