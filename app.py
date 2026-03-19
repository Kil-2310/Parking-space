from fastapi import FastAPI, HTTPException
from database.models import async_session, engine
from database import database_models
from database import models
from sqlalchemy import select
import schemas
from datetime import datetime
from sqlalchemy.orm import selectinload

from typing import List


def create_app():
    app = FastAPI()

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(models.Base.metadata.create_all)

    @app.on_event("shutdown")
    async def shutdown():
        await async_session.close()
        await engine.dispose()

    @app.get("/clients", status_code=200, response_model=List[schemas.BaseClientOut])
    async def route_get_clients() -> List[database_models.Client]:
        async with async_session() as session:
            async with session.begin():
                res = await session.execute(select(database_models.Client))

                return res.scalars().all()

    @app.get(
        "/clients/{client_id}", status_code=200, response_model=schemas.BaseClientOut
    )
    async def route_get_client_by_id(client_id: int) -> database_models.Client:
        async with async_session() as session:
            async with session.begin():
                res = await session.execute(
                    select(database_models.Client).where(
                        database_models.Client.client_id == client_id
                    )
                )
                client = res.scalars().first()
                if not client:
                    raise HTTPException(
                        status_code=404, detail=f"Клиент с ID {client_id} не найден"
                    )
                return client

    @app.put("/clients", status_code=201, response_model=schemas.BaseClientOut)
    async def route_post_creat_user(client: schemas.BaseClientIn):
        async with async_session() as session:
            async with session.begin():
                db_client = database_models.Client(**client.dict())
                session.add(db_client)
                return db_client

    @app.put("/parkings", status_code=201, response_model=schemas.BaseParkingOut)
    async def route_create_parking_place(
        parking: schemas.BaseParkingIn,
    ) -> database_models.Parking:
        async with async_session() as session:
            async with session.begin():
                db_parking = database_models.Parking(**parking.dict())
                session.add(db_parking)
                return db_parking

    @app.put(
        "/client_parkings", status_code=201, response_model=schemas.BaseClientParkingOut
    )
    async def create_client_parkings(
        client_parking: schemas.BaseClientParkingIn,
    ) -> database_models.ClientParking:
        async with async_session() as session:
            async with session.begin():
                parking_id = client_parking.parking_id

                result = await session.execute(
                    select(database_models.Parking).where(
                        database_models.Parking.parking_id == parking_id
                    )
                )

                parking = result.scalar_one_or_none()

                if parking is None:
                    raise HTTPException(404, "Парковка не найдена")

                if not parking.opened:
                    raise HTTPException(400, "Парковка закрыта")

                if parking.count_available_places == 0:
                    raise HTTPException(400, "Парковка заполнена")

                db_client_parking = database_models.ClientParking(
                    **client_parking.dict()
                )
                parking.opened = False
                parking.count_available_places -= 1

                session.add(db_client_parking)

                return db_client_parking

    @app.delete(
        "/client_parkings",
        status_code=200,
        response_model=schemas.BaseClientParkingDelete,
    )
    async def route_delet_client_parking(client_parking: schemas.BaseClientParkingIn):
        async with async_session() as session:
            async with session.begin():
                client_id = client_parking.client_id
                parking_id = client_parking.parking_id

                result = await session.execute(
                    select(database_models.ClientParking)
                    .options(selectinload(database_models.ClientParking.parking))
                    .where(
                        database_models.ClientParking.client_id == client_id,
                        database_models.ClientParking.parking_id == parking_id,
                    )
                )
                client_parking_record = result.scalar_one_or_none()

                if client_parking_record is None:
                    raise HTTPException(404, "Запись о парковке не найдена")

                client_parking_record.time_out = datetime.now()

                parking = client_parking_record.parking

                parking.opened = True
                parking.count_available_places += 1

                return client_parking_record

    return app
