from app.db.models.models import EventsModel, Users, MyEventsModel
from sqlalchemy import select, update, and_
from app.schemas.wallet import Trade
from app.queery.wallet import remittance_to_user

async def create_events(name, date_end, descriotion, price, type, url, session, nickname):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    new_event = EventsModel(
        name=name, descriotion=descriotion, price=price, photo=url, type=type,
        author_id=user.id, date_end=date_end
    )
    session.add(new_event)
    await session.commit()


async def get_events(category: str):
    query_join = (
        select(
            EventsModel.id,
            EventsModel.name,
            EventsModel.photo,
            EventsModel.descriotion,
            EventsModel.price,
            EventsModel.type,
            EventsModel.date_end,
            Users.nickname,
            Users.name.label("user_name"),
            Users.surname.label("user_surname"),
        )
        .join(Users, Users.id == EventsModel.author_id)
    )
    if category is not None:
        pass
    return query_join


async def accept_event(event_id, nickname, session):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    new_event_user = MyEventsModel(
        events_id=event_id, user_id=user.id, condition="Еще не выполнено"
    )
    session.add(new_event_user)
    await session.commit()


async def complete_event(event_id, session, nickname):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    event_query = select(EventsModel).where(EventsModel.id == event_id)
    event: EventsModel = await session.scalar(event_query)
    update_event_query = (
        update(MyEventsModel)
        .values(condition="Выполнено")
        .where(
            and_(
                MyEventsModel.user_id == user.id,
                MyEventsModel.events_id == event_id
            )
        )
    )
    await session.execute(update_event_query)
    await session.commit()
    goto = Trade(fromPrivateKey='c91dfa01c52a4580d847e2e52a90d541977733653192fd54a1d13ef5e563bfe9',
                 toPublicKey=user.wallet_public, type=event.type, amount=event.price)
    return await remittance_to_user(goto, nickname, session)


async def get_myevents(category: str, nickname, session):
    user_query = select(Users).where(Users.nickname == nickname)
    user: Users = await session.scalar(user_query)
    query_join = (
        select(
            EventsModel.id,
            EventsModel.name,
            EventsModel.photo,
            EventsModel.descriotion,
            EventsModel.price,
            EventsModel.type,
            EventsModel.date_end,
            Users.nickname,
            Users.name.label("user_name"),
            Users.surname.label("user_surname"),
            MyEventsModel.user_id,
            MyEventsModel.condition
        )
        .join(Users, Users.id == EventsModel.author_id)
        .join(MyEventsModel, MyEventsModel.events_id == EventsModel.id)
        .where(MyEventsModel.user_id == user.id)
    )
    if category is not None:
        pass
    return query_join