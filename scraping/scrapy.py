import asyncio
import re
import time

from bs4 import BeautifulSoup
from httpx import AsyncClient
from urllib.parse import urljoin
from config import regex_pattern

HOME_URL = "https://djinni.co"
URL = "https://djinni.co/jobs/?primary_keyword=Python"


async def get_number_of_pages(client: AsyncClient) -> int:
    response = await client.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    return int([link.text.strip() for link in soup.select("ul.pagination > li.page-item:not(.disabled) > a.page-link")][-3])


async def get_djinni_jobs(page: int, client: AsyncClient) -> list:
    if page == 1:
        response = await client.get(URL)
    else:
        response = await client.get(URL, params={"page": page})
    soup = BeautifulSoup(response.content, "html.parser")
    return [job.select_one("a.job-list-item__link")["href"] for job in soup.select("li.list-jobs__item")]


async def parse_job(link: str, client: AsyncClient) -> list:
    response = await client.get(urljoin(HOME_URL, link))
    soup = BeautifulSoup(response.content, "html.parser")
    job_description = soup.select("div.mb-4")[0].get_text()
    return re.findall(regex_pattern, job_description)


async def main():
    async with AsyncClient() as client:
        number_of_pages = await get_number_of_pages(client)

        job_links = await asyncio.gather(
            *[get_djinni_jobs(page, client) for page in range(1, number_of_pages)]
        )
        job_links = [job for sublist in job_links for job in sublist]

        job_titles = await asyncio.gather(*[parse_job(link, client) for link in job_links])
        for i in job_titles:
            print(i)

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print("Elapsed:", end_time - start_time)
