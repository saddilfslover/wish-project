from sqlalchemy import select, update, delete, func
from models import async_session, User, WishItem
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class WishItemSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    priority: int
    link: Optional[str] = None
    completed: bool
    user: int
    
    model_config = ConfigDict(from_attributes=True)


class AddWishItemSchema(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    priority: Optional[int] = 3
    link: Optional[str] = None


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user
        
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_wish_items(user_id):
    async with async_session() as session:
        wish_items = await session.scalars(
            select(WishItem).where(WishItem.user == user_id, WishItem.completed == False)
            .order_by(WishItem.priority, WishItem.id)
        )
        
        serialized_items = [
            WishItemSchema.model_validate(w).model_dump() for w in wish_items
        ]
        
        return serialized_items


async def get_completed_wishes_count(user_id):
    async with async_session() as session:
        return await session.scalar(select(func.count(WishItem.id)).where(WishItem.completed == True))


async def add_wish_item(user_id, wish_data: AddWishItemSchema):
    async with async_session() as session:
        new_wish = WishItem(
            title=wish_data.title,
            description=wish_data.description,
            price=wish_data.price,
            priority=wish_data.priority,
            link=wish_data.link,
            user=user_id
        )
        session.add(new_wish)
        await session.commit()
        await session.refresh(new_wish)
        return new_wish


async def update_wish_item(wish_id):
    async with async_session() as session:
        await session.execute(update(WishItem).where(WishItem.id == wish_id).values(completed=True))
        await session.commit()


async def delete_wish_item(wish_id):
    async with async_session() as session:
        await session.execute(delete(WishItem).where(WishItem.id == wish_id))
        await session.commit()