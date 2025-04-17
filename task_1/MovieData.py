import requests
import csv
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple, Any, Union
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.themoviedb.org/3")
MOVIE_ENDPOINT = os.getenv("MOVIE_ENDPOINT", "/discover/movie")
GENRE_ENDPOINT = os.getenv("GENRE_ENDPOINT", "/genre/movie/list")

DEFAULT_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

class MovieData:

    def __init__(self, num_pages: int = 1):
        self.base_movie_url = f"{API_BASE_URL}{MOVIE_ENDPOINT}?include_adult=false&include_video=false&sort_by=popularity.desc&page={{}}"
        self.genre_url = f"{API_BASE_URL}{GENRE_ENDPOINT}?language=en"
        self.headers = DEFAULT_HEADERS
        self.num_pages = num_pages
        self.all_movies = []
        self.genres = {}

    def _fetch_data(self, url: str) -> Union[Dict, None]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_movie_data(self) -> bool:
        genre_data = self._fetch_data(self.genre_url)
        if not genre_data:
            return False

        self.genres = {genre['id']: genre['name'] for genre in genre_data.get('genres', [])}

        for page in range(1, self.num_pages + 1):
            url = self.base_movie_url.format(page)
            movie_data = self._fetch_data(url)
            if movie_data:
                self.all_movies.extend(movie_data.get('results', []))
            else:
                return False

        return True

    def get_all_data(self) -> List[Dict]:
        return self.all_movies

    def get_sliced_data(self) -> List[Dict]:
        return self.all_movies[3:20:4]

    def get_most_popular_title(self) -> str:
        if not self.all_movies:
            return ""
        return self.all_movies[0].get('title', '')

    def search_titles_by_keywords(self, *keywords: str) -> List[str]:
        if not keywords or not self.all_movies:
            return []

        keywords_lower = [kw.lower() for kw in keywords]
        matches = []

        for movie in self.all_movies:
            overview = movie.get('overview', '').lower()
            if any(kw in overview for kw in keywords_lower):
                matches.append(movie.get('title', ''))

        return matches

    def get_unique_genres(self) -> Set[str]:
        unique_genre_ids = set()

        for movie in self.all_movies:
            unique_genre_ids.update(movie.get('genre_ids', []))

        return frozenset(self.genres.get(gid, '') for gid in unique_genre_ids)

    def delete_movies_by_genre(self, genre_name: str) -> int:
        genre_id = None
        for gid, name in self.genres.items():
            if name.lower() == genre_name.lower():
                genre_id = gid
                break

        if genre_id is None:
            return 0

        original_count = len(self.all_movies)
        self.all_movies = [movie for movie in self.all_movies if genre_id not in movie.get('genre_ids', [])]
        return original_count - len(self.all_movies)

    def get_most_popular_genres(self) -> List[Tuple[str, int]]:
        genre_counts = {}

        for movie in self.all_movies:
            for genre_id in movie.get('genre_ids', []):
                genre_name = self.genres.get(genre_id, 'Unknown')
                genre_counts[genre_name] = genre_counts.get(genre_name, 0) + 1

        return sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

    def get_movies_grouped_by_genres(self) -> Dict[str, Set[str]]:
        genre_to_movies = {}

        for movie in self.all_movies:
            title = movie.get('title', '')
            for genre_id in movie.get('genre_ids', []):
                genre_name = self.genres.get(genre_id, 'Unknown')
                genre_to_movies.setdefault(genre_name, []).append(title)

        result = {}
        for genre, movies in genre_to_movies.items():
            pairs = set()
            for i in range(len(movies)):
                for j in range(i + 1, len(movies)):
                    pairs.add(frozenset({movies[i], movies[j]}))
            if pairs:
                result[genre] = frozenset(pairs)

        return result

    def get_modified_genre_data(self) -> Tuple[List[Dict], List[Dict]]:
        modified_data = []

        for movie in self.all_movies:
            movie_copy = movie.copy()
            genre_ids = movie_copy.get('genre_ids', [])
            if genre_ids:
                genre_ids = genre_ids.copy()
                genre_ids[0] = 22
                movie_copy['genre_ids'] = genre_ids
            modified_data.append(movie_copy)

        return (self.all_movies.copy(), modified_data)

    def get_structured_data(self) -> List[Dict[str, Any]]:
        structured = []

        for movie in self.all_movies:
            release_str = movie.get('release_date', '')
            last_day = None
            if release_str:
                try:
                    release_date = datetime.strptime(release_str, '%Y-%m-%d')
                    last_day = release_date + timedelta(days=30*2 + 14)
                except ValueError:
                    pass

            structured.append({
                'Title': movie.get('title', ''),
                'Popularity': round(movie.get('popularity', 0), 1),
                'Score': int(movie.get('vote_average', 0)),
                'Last_day_in_cinema': last_day.strftime('%Y-%m-%d') if last_day else 'Unknown'
            })

        return sorted(structured, key=lambda x: (-x['Score'], -x['Popularity']))

    def write_structured_data_to_csv(self, file_path: str) -> bool:
        structured_data = self.get_structured_data()
        if not structured_data:
            return False

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Title', 'Popularity', 'Score', 'Last_day_in_cinema']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for row in structured_data:
                    writer.writerow(row)

            return True
        except IOError as e:
            print(f"Error writing to CSV: {e}")
            return False
