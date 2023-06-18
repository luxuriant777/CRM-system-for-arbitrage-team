import random
import asyncio
import httpx
from faker import Faker

USER_URL = "http://127.0.0.1:8000/api/users/register/"
PROSPECT_URL = "http://127.0.0.1:8000/api/prospects/create/"

POSITIONS = [
    "Buyer",
    "Buyer",
    "Buyer",
    "Buyer",
    "Buyer",
    "Buyer",
    "Buyer",
    "Buyer",
    "Team Lead",
    "Funds Coordinator"
]

fake = Faker()

async def create_user():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                username = fake.user_name()
                email = fake.email()
                password = fake.password()
                first_name = fake.first_name()
                last_name = fake.last_name()
                position = random.choice(POSITIONS)

                user_payload = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "position": position
                }

                user_response = await client.post(USER_URL, json=user_payload)

                if user_response.status_code == 201:
                    print(f"Successfully created user: {username}")
                else:
                    print(f"Failed to create user: {user_response.content}")

                await asyncio.sleep(1)
            except httpx.RequestError:
                print("Server is down. Waiting before retrying.")
                await asyncio.sleep(10)

async def create_prospect():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                prospect_payload = {
                    "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    "user_agent": fake.user_agent(),
                    "referral_source": fake.url(),
                    "user_id": random.randint(1, 100)
                }

                prospect_response = await client.post(PROSPECT_URL, json=prospect_payload)

                if prospect_response.status_code == 201:
                    print(f"Successfully created prospect for user_id: {prospect_payload['user_id']}")
                else:
                    print(f"Failed to create prospect: {prospect_response.content}")

                await asyncio.sleep(1)
            except httpx.RequestError:
                print("Server is down. Waiting before retrying.")
                await asyncio.sleep(10)

async def main():
    while True:
        task_create_user = asyncio.create_task(create_user())
        task_create_prospect = asyncio.create_task(create_prospect())

        await asyncio.gather(task_create_user, task_create_prospect)

asyncio.run(main())
