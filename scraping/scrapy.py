import asyncio
import time

from bs4 import BeautifulSoup
from httpx import AsyncClient

HOME_URL = "https://djinni.co/jobs/"
URL = "https://djinni.co/jobs/?primary_keyword=Python"


async def get_number_of_pages(client: AsyncClient) -> int:
    response = await client.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    return int([link.text.strip() for link in soup.select("ul.pagination > li.page-item:not(.disabled) > a.page-link")][-3])


async def main():
    async with AsyncClient() as client:
        number_of_pages = await get_number_of_pages(client)


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print("Elapsed:", end_time - start_time)
