import requests


class TMDBHelper:

    def __init__(self, api_key=None):
        self.api_key = api_key

    def get_request_url(self, method='/movie/popular', **kwargs):

        base_url = 'https://api.themoviedb.org/3'
        request_url = base_url + method
        request_url += f'?api_key={self.api_key}'

        for k, v in kwargs.items():
            request_url += f'&{k}={v}'

        return request_url

    def get_movie_id(self, title):

        request_url = self.get_request_url('/search/movie', query=title, region='KR', language='ko')
        data = requests.get(request_url).json()
        results = data.get('results')
        if results:
            movie = results[0]
            movie_id = movie['id']
            return movie_id
        else:
            return None
