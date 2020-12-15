from db.models import *
from db import db_handler


async def add_quote(channel_name, author, quote):
    data = [Quotes(
        channel_name=channel_name,
        author=author,
        quote=quote
    )]
    await db_handler.insert(data)


async def delete_quote(channel_name, id):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_delete_quote, channel_name, id)


def local_delete_quote(session, channel_name, id):
    row = session.query(Quotes).filter(Quotes.channel_name == channel_name, Quotes.id == id).one_or_none()
    if row:
        session.delete(row)
        session.commit()
        return True


async def get_quotes(channel_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_quotes, channel_name)


def local_get_quotes(session, channel_name):
    row = session.query(Quotes).filter(Quotes.channel_name == channel_name)
    return [
        {
            'id': quote.id,
            'author': quote.author,
            'quote': quote.quote
        } for quote in row
    ]
