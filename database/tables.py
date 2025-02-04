from config import conn, cur


def create_tables():
    cur.execute("""
        CREATE TABLE IF NOT EXIST guilds(
            "id" INTEGER PRIMARY KEY,
            "guild_id" INTEGER,
            "channel_create_id" INTEGER,
            "channel_setting_id" INTEGER
        );
    """)

    conn.commit()
