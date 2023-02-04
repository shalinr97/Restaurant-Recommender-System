import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import random
from time import time

def recommender(request,lucky):

    df = pd.read_csv('Restro/data/last_2_years_restaurant_reviews.csv')
    dfuser = pd.read_csv('Restro/data/dfuser1.csv')

    df_data=pd.read_csv('Restro/data/df_data.csv')
    unique_users_id = df_data['user_id'].unique()
    user_shape = unique_users_id.shape
    #print('Number of Unique User ID: %d' % user_shape[0])
    user_df = pd.DataFrame({
           'user_id': unique_users_id,
         'user_index': range(user_shape[0])
        })
    # user_df.head(2)

    unique_business_id = df_data['business_id'].unique()
    business_shape = unique_business_id.shape
    #print('Number of Unique Business ID: %d' % business_shape[0])
    business_df = pd.DataFrame({
            'business_id' :unique_business_id,
            'business_index': range(business_shape[0])
        })
    # business_df.head(2)
    # df_data.head(100)


    # construct sparse matrix
    highest_user_id = unique_users_id.shape[0]
    highest_business_id = unique_business_id.shape[0]
    ratings_mat = sparse.lil_matrix((highest_user_id, highest_business_id))
    ratings_mat
    df_data=df_data.head(100)
    for _, row in df_data.iterrows():
        # subtract 1 from id's due to match 0 indexing
        ratings_mat[row.user_index_x, row.business_index] = row.stars

    #print(ratings_mat[0])

    class ItemItemRecommender(object):

        def __init__(self, neighborhood_size):
            self.neighborhood_size = neighborhood_size

        def fit(self, ratings_mat):
            self.ratings_mat = ratings_mat
            self.n_users = ratings_mat.shape[0]
            self.n_items = ratings_mat.shape[1]
            self.item_sim_mat = cosine_similarity(self.ratings_mat.T)
            self._set_neighborhoods()

        def _set_neighborhoods(self):
            least_to_most_sim_indexes = np.argsort(self.item_sim_mat, 1)
            self.neighborhoods = least_to_most_sim_indexes[:, -self.neighborhood_size:]

        def pred_one_user(self, user_id, report_run_time=False):
            start_time = time()
            items_rated_by_this_user = self.ratings_mat[user_id].nonzero()[1]
            # Just initializing so we have somewhere to put rating preds
            out = np.zeros(self.n_items)
            for item_to_rate in range(self.n_items):
                relevant_items = np.intersect1d(self.neighborhoods[item_to_rate], items_rated_by_this_user, assume_unique=True)
                 # assume_unique speeds up intersection op
                out[item_to_rate] = self.ratings_mat[user_id, relevant_items] *                 self.item_sim_mat[item_to_rate, relevant_items] /                 self.item_sim_mat[item_to_rate, relevant_items].sum()
            if report_run_time:
                print("Execution time: %f seconds" % (time()-start_time))
            cleaned_out = np.nan_to_num(out)
            return cleaned_out

        def pred_all_users(self, report_run_time=False):
            start_time = time()
            all_ratings = [
                self.pred_one_user(user_id) for user_id in range(self.n_users)]
            if report_run_time:
                print("Execution time: %f seconds" % (time()-start_time))
            return np.array(all_ratings)

        def top_n_recs(self, user_id, n, verbose = False):
            pred_ratings = self.pred_one_user(user_id, report_run_time = verbose)
            item_index_sorted_by_pred_rating = list(np.argsort(pred_ratings))
            items_rated_by_this_user = self.ratings_mat[user_id].nonzero()[1]
            unrated_items_by_pred_rating = [item for item in item_index_sorted_by_pred_rating
                                            if item not in items_rated_by_this_user]
            return unrated_items_by_pred_rating[-n:]


    Top_N = 10
    recommender = ItemItemRecommender(neighborhood_size=100)
    recommender.fit(ratings_mat)

    print('User Chosen is: %d' % lucky)
    result = recommender.top_n_recs(lucky, Top_N, verbose = True)
    print(result)

    def printBusiness(result_list, unique_user_id):
        business_list = []
        for index in result:
            business_list.append(unique_users_id[index])
        return business_list

    convert_result = printBusiness(result, unique_users_id)
    print(convert_result)

    convert_result = pd.DataFrame({'user_id': convert_result})
    #convert_result=convert_result.rename( columns={'':'new column name'}, inplace=True )
    convert_result

    join_user = pd.merge(dfuser,convert_result, how='inner', on="user_id")
    # print(df.info())
    # pd.DataFrame(df['business_id'].unique())
    # print(df.info())


    join_business = pd.merge(df, join_user, how = 'inner', left_on='user_id', right_on = 'user_id') #
    final_business=join_business[join_business.stars>4]
    final_business=(final_business[['user_id','name_y','business_id','name_x','review_id','stars']]).rename(columns = {"name_x": "business_name","name_y":"user_name"})
    final_business=final_business.sort_values('business_id')
    final_business = final_business.drop_duplicates(subset=['business_id'])
    final_business
    final_business.to_json('final_business.json')

    #df=final_business.to_json(index='false',orient='records')
#for index, row in final_business.iterrows():
    #print(row['username'], row['business_name'])


    #print("Similar users like %d are" %lucky)
    #join_user=join_user.loc[:,['user_id','name']]
    #join_user

    #df_data.to_csv('cleaned_data.csv')
    #final_business.to_csv('final_business.csv')
    return (final_business)
