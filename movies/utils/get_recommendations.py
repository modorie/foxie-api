import requests
import environ
import json

from tmdb_helper import TMDBHelper


def get_recommendations():
    tmdb_helper = TMDBHelper(TMDB_API_KEY)
    movie_list = []

    with open('../fixtures/movies.json', 'r', encoding='UTF8') as f:
        movies = json.load(f)

    for movie in movies:
        movie = movie.get('fields')
        movie_id = movie.get('id')

        print(movie.get('title'))

        recommendations_request_url = tmdb_helper.get_request_url(method=f'/movie/{movie_id}/recommendations', language='ko')
        recommendations = requests.get(recommendations_request_url).json().get('results')

        recommendations_list = []

        for recommendation in recommendations:
            recommendations_list.append(recommendation.get('id'))

            print(f"\t\t {recommendation.get('title')}")

        movie['recommendations'] = recommendations_list

        record = {
            'model': 'movies.movie',
            'fields': movie,
        }

        movie_list.append(record)

    return movie_list


def write_json_file(filename, content):
    with open(filename, 'w', encoding='UTF8') as file:
        json.dump(content, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    env = environ.Env()
    environ.Env.read_env()
    TMDB_API_KEY = env('TMDB_API_KEY')

    movie_data = get_recommendations()

    write_json_file('../fixtures/movies.json', movie_data)
