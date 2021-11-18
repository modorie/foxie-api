import requests
import environ
import json

from tmdb_helper import TMDBHelper


def get_popular_movies():
    tmdb_helper = TMDBHelper(TMDB_API_KEY)
    movies_data = []

    for i in range(1, 501):
        request_url = tmdb_helper.get_request_url(region='KR', language='ko', page=i)
        movies = requests.get(request_url).json().get('results')
        data = []
        for movie in movies:
            movie_id = movie.get('id')
            credits_request_url = tmdb_helper.get_request_url(method=f'/movie/{movie_id}/credits', language='ko')
            casts_and_crews = requests.get(credits_request_url).json()

            actors = casts_and_crews.get('cast')
            staffs = casts_and_crews.get('crew')

            result = {
                'actors': [],
                'directors': [],
            }

            for actor in actors:
                actor_id = actor.get('id')
                result['actors'].append(actor_id)
                actor_ids.add(actor_id)

            for staff in staffs:
                if staff.get('department') == 'Directing':
                    director_id = staff.get('id')
                    result['directors'].append(director_id)
                    director_ids.add(director_id)

            movie['actors'] = result['actors']
            movie['directors'] = result['directors']

            record = {
                'model': 'movies.movie',
                'fields': movie,
            }
            data.append(record)

        movies_data.extend(data)
    return movies_data


def get_people(person_ids, model):
    tmdb_helper = TMDBHelper(TMDB_API_KEY)
    people = []

    for person_id in person_ids:
        request_url = tmdb_helper.get_request_url(method=f'/person/{person_id}', language='ko')
        person = requests.get(request_url).json()
        name = person.get('name')

        record = {
            'model': f'movies.{model}',
            'fields': {
                'id': person.get('id'),
                'name': person.get('name'),
                'profile_path': person.get('profile_path'),
                'also_known_as': person.get('also_known_as')
            },
        }

        people.append(record)

    return people


def write_json_file(filename, content):
    with open(filename, 'w', encoding='UTF8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    env = environ.Env()
    environ.Env.read_env()
    TMDB_API_KEY = env('TMDB_API_KEY')

    actor_ids = set()
    director_ids = set()

    popular_movies = get_popular_movies()
    write_json_file('../fixtures/movies.json', popular_movies)

    actors = get_people(actor_ids, 'actor')
    directors = get_people(director_ids, 'director')

    write_json_file('../fixtures/actors.json', actors)
    write_json_file('../fixtures/directors.json', directors)

    print('-----------------------------------------------------------')
    print(f'actors : {len(actors)}')
    print(f'directors : {len(directors)}')
    print('-----------------------------------------------------------')
    print('컴퓨터 고생 많았다.')
