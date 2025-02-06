import disnake
import time

from disnake import TextInputStyle

from config import bot


async def rooms_button_slots(inter: disnake.Interaction, room: disnake.VoiceChannel) -> None:
    custom_id = f"modal.rooms.slots.{inter.user.id}.{round(time.time())}"

    await inter.response.send_modal(
        title="Комната",
        custom_id=custom_id,
        components=[
            disnake.ui.TextInput(
                label="Кол-во слотов",
                custom_id=f"{custom_id}.count",
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

    count = modal_inter.text_values[f"{custom_id}.count"]

    if not (count.isdigit()) or not(0 < int(count) < 100):
        await room.edit(user_limit=0)

        embed = disnake.Embed(
            description="Количество слотов изменено на `∞`",
            color=disnake.Color.green()
        )

    else:
        await room.edit(user_limit=count)

        embed = disnake.Embed(
            description=f"Количество слотов изменено на `{count}`",
            color=disnake.Color.green()
        )

    await modal_inter.send(embed=embed, ephemeral=True)
