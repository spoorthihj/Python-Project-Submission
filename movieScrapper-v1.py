import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

genres = [
    
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western"
    
]
movie_list = []
url_dict = {}
file_name="movieDB.csv"
for genre in genres:
    url="https://www.imdb.com/search/title/?title_type=feature&num_votes=25000,&genres={}&sort=user_rating,desc"
    formated_url = url.format(genre)
    url_dict[genre] = formated_url
    
#print(url_dict)

def get_movies(url, interval, file_name,genre):
    
    resp = requests.get(url, headers=HEADERS)
    content = BeautifulSoup(resp.content, 'lxml')
    #print(content)
    

    for movie in content.select('.ipc-metadata-list-summary-item'):
        metascore="0"
        if movie.findAll('span','sc-b0901df4-0 bcQdDJ metacritic-score-box'):
            #print(movie.findAll('span','sc-b0901df4-0 bcQdDJ metacritic-score-box')[0].text.strip())
            metascore=movie.findAll('span','sc-b0901df4-0 bcQdDJ metacritic-score-box')[0].text.strip()
        try:
            # Creating a python dictonary
            data = {
                
                "title":movie.select('.ipc-title__text')[0].get_text().strip(),
                "year":movie.findAll('span','sc-b189961a-8 kLaxqf dli-title-metadata-item')[0].text.strip(),
                "certificate":movie.findAll('span','sc-b189961a-8 kLaxqf dli-title-metadata-item')[2].text.strip(),
                "time":movie.findAll('span','sc-b189961a-8 kLaxqf dli-title-metadata-item')[1].text.strip(),
                "genre":genre,
                "rating":movie.findAll('span','ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')[0].text.strip(),
                "metascore":metascore,
                "simple_desc":movie.select('.ipc-html-content-inner-div')[0].get_text().strip(),
                "votes":movie.findAll('span','ipc-rating-star--voteCount')[0].text.strip()
                
                    
            }
        except IndexError:
            continue
        #print(data)
        movie_list.append(data)

for genre, url in url_dict.items():
    get_movies(url, 1, genre+'.csv',genre)
    movie_dataframe = pd.DataFrame(movie_list)
    movie_dataframe.to_csv(file_name)
    print("Saved:", genre)

while True:
    # Suggest a random movie based on genre input
    suggest_genre = input(f"Enter a genre to get a random movie suggestion.\nAvailable genres: {', '.join(genres)} \nType Exit to end :").strip()

    if suggest_genre.lower() == 'exit':
        print("Exiting the movie suggestion app. Goodbye!")
        break
    if suggest_genre in genres:
        filtered_df = movie_dataframe[movie_dataframe['genre'] == suggest_genre]
        if not filtered_df.empty:
            random_movie = filtered_df.sample(n=1).iloc[0]
            #random_movie = random.choice(filtered_df)
            print(f"Suggested Movie:\nTitle: {random_movie['title']}\nYear: {random_movie['year']}\nRating: {random_movie['rating']}\nMetascore: {random_movie['metascore']}\nVotes: {random_movie['votes']}\nGenre: {random_movie['genre']}\nShort Desc: {random_movie['simple_desc']}")
        else:
            print(f"No movies found for the genre '{suggest_genre}'")
    else:
        print(f"Error: '{suggest_genre}' is not a valid genre.")