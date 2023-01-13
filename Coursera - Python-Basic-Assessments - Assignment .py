import requests
import json
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

def get_movies_from_tastedive(suggest):
    base_url = 'https://tastedive.com/api/similar'
    pars = {}
    pars['q'] = suggest
    pars['type'] = 'movies'
    pars['limit'] = '5'
    r = requests.get(base_url, params = pars)
    return json.loads(r.text)

def extract_movie_titles(data):
    top_5 = []
    for title in data['Similar']['Results']:
        print(title['Name'])
        top_5.append(title['Name'])
    return top_5

def get_related_titles(l):
    x = []
    for movie in l:
        x.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(x))

def get_movie_data(title):
    base_url = 'http://www.omdbapi.com/'
    pars = {}
    pars['t'] = title
    pars['r'] = 'json'
    r = requests.get(base_url, params=pars)
    r2 = r.json()
    return json.loads(r.text)

def get_movie_rating(x):
    ratings = x['Ratings']

    for rate in ratings:
        if rate['Source'] == 'Rotten Tomatoes':  
            return int(rate['Value'][:-1])
    return 0


def get_sorted_recommendations(x):
    titles = get_related_titles(x)
    result_dict = {}
    for title in titles:
        rating = get_movie_rating(get_movie_data(title))
        result_dict[title] = rating
    return [i[0] for i in sorted(result_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
