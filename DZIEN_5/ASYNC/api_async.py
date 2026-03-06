import asyncio
import random

async def fetch_user_data(user_id: int) -> dict:
    delay = random.uniform(0.5,2.0)
    print(f"Pobieram dane użytkownika: {user_id}....")
    await asyncio.sleep(delay)
    return {
        "user_id": user_id,
        "name": f"User_{user_id}",
        "delay": round(delay,2)
    }

async def main():
    tasks = [fetch_user_data(i) for i in range(1,6)]
    results = await asyncio.gather(*tasks)

    print("\nWyniki:")
    for item in results:
        print(item)

asyncio.run(main())
