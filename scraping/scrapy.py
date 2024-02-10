import asyncio
import csv
import re
import time

from dataclasses import astuple, fields
from typing import NoReturn

from bs4 import BeautifulSoup
from httpx import AsyncClient
from urllib.parse import urljoin
from config import regex_pattern
from scraping.models import Vacancy


HOME_URL = "https://djinni.co"
URL = "https://djinni.co/jobs/?primary_keyword=Python"


async def get_number_of_pages(client: AsyncClient) -> int:
    response = await client.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    return int(
        [
            link.text.strip()
            for link in soup.select(
                "ul.pagination > li.page-item:not(.disabled) > a.page-link"
            )
        ][-3]
    )


async def get_djinni_jobs(page: int, client: AsyncClient) -> list:
    if page == 1:
        response = await client.get(URL)
    else:
        response = await client.get(URL, params={"page": page})
    soup = BeautifulSoup(response.content, "html.parser")
    return [
        job.select_one("a.job-list-item__link")["href"]
        for job in soup.select("li.list-jobs__item")
    ]


async def parse_job(link: str, client: AsyncClient) -> Vacancy:
    response = await client.get(urljoin(HOME_URL, link))
    soup = BeautifulSoup(response.content, "html.parser")
    title = "".join(soup.select_one("h1").stripped_strings)
    company_element = soup.select_one("h4")
    company = (
        re.findall(r"Про компанію\s+([\w\s]+)", company_element.text.strip())
        if company_element
        else None
    )
    location = "".join(soup.select_one("span.location-text").stripped_strings)
    views_count = int(
        soup.select_one(".bi-eye").next_sibling.strip().split()[0]
    )
    reviews_count = int(
        soup.select_one(".bi-people-fill").next_sibling.strip().split()[0]
    )
    requirements = re.findall(
        regex_pattern, soup.select("div.mb-4")[0].get_text()
    )

    if company:
        company = company[0]

    return Vacancy(
        title=title,
        company=company,
        location=location,
        requirements=requirements,
        views_count=views_count,
        reviews_count=reviews_count,
    )


def write_vacancy_to_csv(vacancies: [Vacancy]) -> NoReturn:
    with open("vacancies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([field.name for field in fields(Vacancy)])
        writer.writerows([astuple(vacancy) for vacancy in vacancies])


async def main():
    async with AsyncClient() as client:
        number_of_pages = await get_number_of_pages(client)

        job_links = await asyncio.gather(
            *[
                get_djinni_jobs(page, client)
                for page in range(1, number_of_pages)
            ]
        )
        job_links = [job for sublist in job_links for job in sublist]

        job_titles = await asyncio.gather(
            *[parse_job(link, client) for link in job_links]
        )
        write_vacancy_to_csv(job_titles)


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    print("Elapsed:", end_time - start_time)
