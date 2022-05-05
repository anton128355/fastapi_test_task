from app.api.models import UserSchema
from app.db import users, database
import random
import string
import hashlib


async def put(id: int, payload: UserSchema):
    delete(id)
    post(payload)


async def patch(id: int, payload: UserSchema):

    query = (
            users
            .update()
            .where(id == users.c.id)
            .values(**payload)
            .returning(users.c.id)
        )
    return await database.execute(query=query)


async def post(payload: UserSchema):
    if payload.password != None:
        salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
        enc = hashlib.pbkdf2_hmac("sha256", payload.password.encode(), salt.encode(), 100_000)
        query = users.insert().values(username=payload.username, email=payload.email, password=enc.hex())
    else:
        query = users.insert().values(username=payload.username, email=payload.email, password=payload.password)

    return await database.execute(query=query)


async def get(id: int):
    query = users.select().where(id == users.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = users.select()
    return await database.fetch_all(query=query)


async def delete(id: int):
    query = users.delete().where(id == users.c.id)
    return await database.execute(query=query)
