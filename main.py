from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq
from typing import Optional


class AddWishItem(BaseModel):
    tg_id: int
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    priority: Optional[int] = 3
    link: Optional[str] = None


class CompleteWishItem(BaseModel):
    id: int


class DeleteWishItem(BaseModel):
    id: int


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('Доска желаний готова к работе!')
    yield


app = FastAPI(title="Доска желаний", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/wishes/{tg_id}")
async def get_wishes(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_wish_items(user.id)


@app.get("/api/profile/{tg_id}")
async def profile(tg_id: int):
    user = await rq.add_user(tg_id)
    completed_wishes_count = await rq.get_completed_wishes_count(user.id)
    return {'completedWishes': completed_wishes_count}


@app.post("/api/add")
async def add_wish(wish: AddWishItem):
    user = await rq.add_user(wish.tg_id)
    wish_data = rq.AddWishItemSchema(
        title=wish.title,
        description=wish.description,
        price=wish.price,
        priority=wish.priority,
        link=wish.link
    )
    new_wish = await rq.add_wish_item(user.id, wish_data)
    return {'status': 'ok', 'wish_id': new_wish.id}


@app.patch("/api/complete")
async def complete_wish(wish: CompleteWishItem):
    await rq.update_wish_item(wish.id)
    return {'status': 'ok'}


@app.delete("/api/delete")
async def delete_wish(wish: DeleteWishItem):
    await rq.delete_wish_item(wish.id)
    return {'status': 'ok'}