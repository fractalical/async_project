import aiohttp
import asyncio
import sys
from more_itertools import chunked

from models import engine, Session, Base, SwapiPeaple


async def get_homeworld(homeworld_url, session):
    async with session.get(url=homeworld_url) as response:
        json_data = await response.json()
    return json_data.get('name')


async def get_vehicle(vehicle_url, session):
    async with session.get(url=vehicle_url) as response:
        json_data = await response.json()
    return json_data.get('name')


async def get_starship(starship_url, session):
    async with session.get(url=starship_url) as response:
        json_data = await response.json()
    return json_data.get('name')


async def get_specie(specie_url, session):
    async with session.get(url=specie_url) as response:
        json_data = await response.json()
    return json_data.get('name')


async def get_film(film_url, session):
    async with session.get(url=film_url) as response:
        json_data = await response.json()
    return json_data.get('title')


async def get_pers(pers_id, session):
    async with session.get(url=f'https://swapi.dev/api/people/{pers_id}/')\
            as response:
        json_data = await response.json()
        print(pers_id)
        try:
            homeworld = await get_homeworld(homeworld_url=json_data.get('homeworld'), session=session)
            film_tasks = []
            for film_url in json_data.get('films'):
                film_tasks.append(asyncio.create_task(get_film(film_url=film_url, session=session)))
            films = await asyncio.gather(*film_tasks)
            species_tasks = []
            for specie_url in json_data.get('species'):
                species_tasks.append(asyncio.create_task(
                    get_specie(specie_url=specie_url, session=session)))
            species = await asyncio.gather(*species_tasks)
            starships_tasks = []
            for starship_url in json_data.get('starships'):
                starships_tasks.append(asyncio.create_task(
                    get_starship(starship_url=starship_url, session=session)))
            starships = await asyncio.gather(*starships_tasks)
            vehicles_tasks = []
            for vehicle_url in json_data.get('vehicles'):
                vehicles_tasks.append(asyncio.create_task(
                    get_vehicle(vehicle_url=vehicle_url, session=session)))
            vehicles = await asyncio.gather(*vehicles_tasks)
            json_data['homeworld'] = homeworld
            json_data['films'] = ', '.join(films)
            json_data['species'] = ', '.join(species)
            json_data['starships'] = ', '.join(starships)
            json_data['vehicles'] = ', '.join(vehicles)
            json_data.pop('url')
            json_data.pop('edited')
            json_data.pop('created')
            return json_data
        except Exception as e:
            print(f"ERROR: {e}. URL: https://swapi.dev/api/people/{pers_id}/")


async def write_to_db(persons_json):
    async with Session() as session:
        orm_objects = [SwapiPeaple(**person) for person in persons_json if person]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=f'https://swapi.dev/api/people/')
        count = await response.json()

        persons_coro = (get_pers(i, session) for i in range(1, count.get('count')+2))
        persons_coro_chunked = chunked(persons_coro, 5)
        for persons_coro_chunk in persons_coro_chunked:
            persons = await asyncio.gather(*persons_coro_chunk)
            task = asyncio.create_task(write_to_db(persons))
            await asyncio.gather(task)


if __name__ == '__main__':
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

