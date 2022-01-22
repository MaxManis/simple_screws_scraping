import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://razmery.info/strmat/bolty/razmery-boltov.html'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71'
                 ' Safari/537.36'
}

# Получам и сохраняем страницу
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(src)


# работаем с уже сохраненной страницей
with open("index.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')


# собираем заголовки таблицы
table_head = soup.find(class_='table_standart').find('tr').find_all('th')
standard = table_head[0].text
diameter = table_head[1].text
length = table_head[2].text

# форматируем текст, убираем лишнее
standard = standard[standard.find('арт') + 4:]
diameter = diameter[diameter.find(')') + 2:]
length = length[length.find(')') + 2:]

diameter = diameter[:diameter.find(')') + 1]
length = length[:length.find(')') + 1]

# записываем данные в csv
with open('screws.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            standard,
            diameter,
            length
        ]
    )


# собираем данные продуктов
table_info = soup.find(class_='table_standart').find('tbody').find_all('tr')

screws_json = []
for item in table_info:
    screw_info = item.find_all('td')

    standard = screw_info[0].text
    diameter = screw_info[1].text
    length = screw_info[2].text

    screws_json.append(
        {
            'Standard': standard,
            'Diameter': diameter,
            'Length': length
        }
    )

    # записываем данные в csv
    with open('screws.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                standard,
                diameter,
                length
            ]
        )

# записываем данные в json
with open("screws.json", "w", encoding="utf-8") as file:
    json.dump(screws_json, file, indent=4, ensure_ascii=False)

print('Парсинг данных завершен.')
