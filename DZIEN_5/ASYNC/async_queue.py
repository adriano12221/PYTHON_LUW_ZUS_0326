
import asyncio
import random

#producent
async def producer(queue: asyncio.Queue):
    for i in range(1,11):
        await asyncio.sleep(0.3)
        item = f"zadanie_{i}"
        await queue.put(item)
        print(f"[PRODUCER] dodano {item} do kolejki")
    await queue.put(None)
    await queue.put(None)

#konsument
async def consumer(name: str, queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            print(f"[CONSUMER] {name} odebrano None, koniec kolejki")
            queue.task_done()
            break
        print(f"[CONSUMER] {name} odebrano {item} z kolejki")
        await asyncio.sleep(random.uniform(0.4,1.2))
        print(f"{name} zakończył przetwarzanie {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()

    producer_task = asyncio.create_task(producer(queue))
    consumer_task1 = asyncio.create_task(consumer("A",queue))
    consumer_task2 = asyncio.create_task(consumer("B",queue))

    await producer_task
    await queue.join()

    await consumer_task1
    await consumer_task2

asyncio.run(main())
