import pandas as pd
import numpy as np

def get_similar_movies(movie_name, user_rating):
  similar_score = item_similarity_df[movie_name] * (user_rating-2.5)
  similar_score = similar_score.sort_values(ascending = False)

  return similar_score

def get_user_list(user_ratings, id):
    user = list()

    ratings = list(user_ratings.iloc[id])
    titles = list(user_ratings)

    for i in range(0, len(ratings)):
        if ratings[i] != 0.0:
            user.append((titles[i], ratings[i]))

    return user

user_list = input("Input user list separated by commas (ex: 2,32,76): ")

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
ratings = pd.merge(movies, ratings)

userratings = ratings.pivot_table(index = ['userId'], columns = ['title'], values = 'rating')

#to avoid noise, if a movie has less than 5 users who rates it then we will delete it.
#Also, fill NaN w/ 0
userratings = userratings.dropna(thresh=5, axis =1).fillna(0)
#userratings = userratings.fillna(0)

#build the similarity matrix
item_similarity_df = userratings.corr(method = 'pearson')

# setup 
all_users = list()
recommended_list = list()
movie_list = list(movies.iloc[:,1])

# format users into list
user_list = user_list.split(',')
for i in range(0, len(user_list)):
  temp = get_user_list(userratings, int(user_list[i])-1)
  all_users.append(temp)


# iterate recommended ratings per user
for i in range(0, len(all_users)):

  similar_movies = pd.DataFrame()

  for movie,rating in all_users[i]:
    similar_movies = similar_movies.append(get_similar_movies(movie,rating), ignore_index = True)

  user_movies = np.delete(all_users[i], 1, 1).flatten()
  temp = similar_movies.sum().sort_values(ascending = False).drop(labels=user_movies)
  #normalized_df = (temp-temp.mean())/temp.std()
  #recommended_list.append(normalized_df)
  recommended_list.append(temp)

# combine to a final list
final = [0] * len(movie_list)
for i in range(0, len(movie_list)):
  for j in range(0, len(recommended_list)):
    try:
      final[i] = final[i] + recommended_list[j][movie_list[i]]
    except:
      continue

# convert to dataframe
final_df = pd.DataFrame({'Title': movie_list, 'Rating': final}).set_index('Title').sort_values(by=['Rating'], ascending = False)
print(final_df)

