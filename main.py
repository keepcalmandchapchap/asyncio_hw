import asyncio
import aiohttp
import requests
from more_itertools import chunked
from models import Session, Persons, close_orm


MAX_COROS = 5

#получить общее кол-во персонажей
async def get_number_of_persons(session):
    response = await session.get('https://swapi.dev/api/people/')
    json_data = await response.json()
    result = json_data['count']
    return int(result)

#может я что-то не понимаю, но почему-то нет 17-ого id, пришлось делать проверку :D
async def get_person(session, i: int):
    response = await session.get(f'https://swapi.dev/api/people/{i}/')
    if response.status == 200:
        return await response.json()
    return None

#получаем информацию с урла
async def get_deep_data(session, url: str):
    response = await session.get(url)
    data = await response.json()
    return data.get('title') or data.get('name')

#собираем персонажа с корректными выводами
async def build_character(session, person, person_index):
    films = [await get_deep_data(session, film_url) for film_url in person['films']]
    homeworld = await get_deep_data(session, person['homeworld'])
    species = [await get_deep_data(session, species_url) for species_url in person['species']]
    starships = [await get_deep_data(session, starship) for starship in person['starships']]
    vehicles = [await get_deep_data(session, vehicle) for vehicle in person['vehicles']]

    return {
        'id': int(person_index),
        'birth_year': person['birth_year'],
        'eye_color': person['eye_color'],
        'films': (', ').join(films),
        'gender': person['gender'],
        'hair_color': person['hair_color'],
        'height': person['height'],
        'homeworld': homeworld,
        'mass': person['mass'],
        'name': person['name'],
        'skin_color': person['skin_color'],
        'species': (', ').join(species),
        'starships': (', ').join(starships),
        'vehicles': (', ').join(vehicles),
    }

async def insert_to_database(json_data):
    async with Session() as session:
        session.add(Persons(**json_data))
        await session.commit()

async def main():
    async with aiohttp.ClientSession() as session:
        number_of_persons = await get_number_of_persons(session)
        for person_indexes in chunked(range(1, number_of_persons+1), 5):
            for person_index in person_indexes:
                person_raw = await get_person(session, person_index)
                if person_raw:
                    person = await build_character(session, person_raw, person_index)
                    asyncio.create_task(insert_to_database(person))
        tasks = asyncio.all_tasks()
        current_task = asyncio.current_task()
        tasks.remove(current_task)
        await asyncio.gather(*tasks)
        await close_orm()


if __name__ == '__main__':
    asyncio.run(main())
    print('Отработал!')

