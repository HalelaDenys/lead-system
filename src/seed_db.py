#!/usr/bin/env python3
"""
Seed the database with sample affiliates and offers, then print JWT tokens.

Usage:
    DATABASE_URL=postgresql+asyncpg://... python scripts/seed_db.py
"""

import asyncio
import sys
import os


from infrastructure import Affiliate, Offer
from infrastructure.db.db_helper import DBHelper
from infrastructure.redis.client import RedisClient
from shared import Security, SubTokenPayloadDTO, settings


async def seed(session, redis_client):
    affiliates = [
        Affiliate(name="WebMaster Alpha"),
        Affiliate(name="WebMaster Beta"),
    ]
    offers = [
        Offer(name="Omega Weight Loss"),
        Offer(name="CardioBoost Pro"),
        Offer(name="SleepWell Supplement"),
    ]
    session.add_all(affiliates + offers)
    await session.commit()

    for a in affiliates:
        await session.refresh(a)
    for o in offers:
        await session.refresh(o)

    print("\n=== Seeded Affiliates ===")
    for a in affiliates:
        await redis_client.get_client().set(f"active_affiliate:{a.id}", str(a.id))
        token = Security.create_token(SubTokenPayloadDTO(sub=a.id))
        print(f"  id={a.id}  name={a.name}")
        print(f"  token: {token}\n")

    print("=== Seeded Offers ===")
    for o in offers:
        print(f"  id={o.id}  name={o.name}")
    print()


async def main():
    redis_client = RedisClient(settings.redis.test_dsn)
    await redis_client.connect()
    db_helper = DBHelper(
        url=settings.db.test_dsn,
        echo=settings.db.alchemy_config.echo,
        echo_pool=settings.db.alchemy_config.echo_pool,
        pool_size=settings.db.alchemy_config.pool_size,
        max_overflow=settings.db.alchemy_config.max_overflow,
    )
    async with db_helper._async_session_maker() as session:
        await seed(session, redis_client)

    await redis_client.close()


if __name__ == "__main__":
    asyncio.run(main())
