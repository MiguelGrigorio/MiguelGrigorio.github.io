from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime
import json
import os

load_dotenv()

notion_secret = os.getenv('NOTION_SECRET')
notion_database_id = os.getenv('NOTION_DATABASE_ID')

def dict_to_json(content, file_name):
    str = json.dumps(content)

    with open(file_name, 'w') as f:
        f.write(str)


def safe_get(data, dot_chained_keys):
    keys = dot_chained_keys.split('.')
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data

def main():
    client = Client(auth=notion_secret)

    db_rows = client.databases.query(database_id=notion_database_id)

    days = []

    for row in db_rows['results']:
        theme = safe_get(row, 'properties.Tema.title.0.plain_text')
        hours = safe_get(row, 'properties.Horas.number')
        date = safe_get(row, 'properties.Start Date.date.start')

        days.append({
            'Tema': theme,
            'Horas': hours,
            'Data': date
        })
    days.sort(key = lambda d: datetime.strptime(d['Data'], '%Y-%m-%d'))
    dict_to_json(days, 'days.json')

    data = []
    week = 0
    for i in range(len(days)):
        if i != 0 and i % 7 == 0:
            week += 1
        data.append({'day': i - (7 * week), 'week': week, 'hours': days[i]['Horas']})
    dict_to_json(data, 'data.json')
    print('Arquivos gerados com sucesso!')

if __name__ == '__main__':
    main()

