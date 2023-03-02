import requests
from bs4 import BeautifulSoup
import csv


def main() -> None:
    html = requests.get("https://admission.rudn.ru/undergraduate/directions/").text
    html_objects = BeautifulSoup(html, "lxml")
    rows_objects = html_objects.find_all("div", {"class": "block__accordion-wrapper"})
    dropup_objects = [
        row.find(
            "div", {"class": "block__content-accordion-wrapper collapse multi-collapse"}
        )
        for row in rows_objects
        if row.find("a", {"class": "link__accordion-panel"}).text.strip().lower()
        == "инженерная академия"
    ]
    dropup_objects = dropup_objects
    disciplines_cost = list()
    for dropup in dropup_objects:
        data = dict()
        name = dropup.find("h5", {"class": "program-short-info__name"}).text.strip()
        data["Название"] = name
        if name in [
            "Энергетическое машиностроение",
            "Эксплуатация транспортно-технологических машин и комплексов",
        ]:
            dropup = dropup.parent.find_all(
                "div",
                {"class": "block__content-accordion-wrapper collapse multi-collapse"},
            )[1]

        prices_objects = dropup.find_all("div", {"class": "program-cost"})
        for price in prices_objects:

            data[
                price.find("div", {"class": "program-cost__left"})
                .find("span", {"class": "program-cost__year"})
                .text.strip()
            ] = (
                price.find("div", {"class": "program-cost__right"})
                .find("span", class_="program-cost__price")
                .text.replace(" ", "")
                .strip()
            )
        disciplines_cost.append(data)
    print(*disciplines_cost, sep="\n")
    with open("disciplines_cost.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "Название",
                "Первый год обучения",
                "Второй год обучения и последующие",
                "Второй год обучения",
                "Третий год обучения и последующие",
            ],
            dialect="excel",
            restval="",
        )
        writer.writeheader()
        writer.writerows(disciplines_cost)


if __name__ == "__main__":
    main()
