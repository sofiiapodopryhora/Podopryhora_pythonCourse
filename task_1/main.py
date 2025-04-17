from MovieData import MovieData

def main():
    processor = MovieData(num_pages=2)

    if processor.fetch_movie_data():
        print("Successfully fetched movie data!")
    else:
        print("Failed to fetch movie data")
        return

    print("\n1. Most popular title:")
    print(processor.get_most_popular_title())

    print("\n2. Movies with 'love' or 'romance' in description:")
    print(processor.search_titles_by_keywords("love", "romance"))

    print("\n3. Unique genres:")
    print(processor.get_unique_genres())

    print("\n4. Most popular genres:")
    for genre, count in processor.get_most_popular_genres()[:5]:
        print(f"{genre}: {count}")

    print("\n5. Deleting Action movies...")
    deleted_count = processor.delete_movies_by_genre("Action")
    print(f"Deleted {deleted_count} movies")

    print("\n6. Writing structured data to CSV...")
    if processor.write_structured_data_to_csv("movie_data.csv"):
        print("Successfully wrote to movie_data.csv")
    else:
        print("Failed to write CSV file")

if __name__ == "__main__":
    main()
