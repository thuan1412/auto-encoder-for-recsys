# import click
import pandas as pd 
from util import *
from sklearn.model_selection import train_test_split

# @click.command("Processes the source data to create new data for the model")
# @click.option("--min_interactions", type=click.INT, default=5,
#                 help="Minimun number of interactions for user")

# @click.option("--test_size", type=click.FLOAT, default=0.2)
# @click.option("--factor_negative_sample", type=click.INT, default=0)

def run(min_interactions=5, test_size=0.2, factor_negative_sample=1):
    base_path = './data/raw/'
    steam_200 = 'steam-200k.csv'
    # Contains logs of user interactions
    interactions_df = pd.read_csv(base_path+steam_200)
    interactions_df.columns = ['user_id', 'game', 'type', 'hours', 'none']
    # group interaction by user_id and game
    interactions_full_df = interactions_df.groupby(['user_id', 'game'])\
                            .sum()['hours'].reset_index()  
    interactions_full_df['view'] = 1
    # filter interactions
    interactions_full_df = filter_interactions(interactions_full_df, min_interactions)

    return interactions_full_df

def filter_interactions(interactions_df, min_interactions=5):
    '''
    Filter interactions of users with at least {min_interactions} interactions
    '''
    # get groupby user_id and number of interactions
    user_interactions_count_df = interactions_df.groupby(['user_id']).size()
    print("# user: %d" % len(user_interactions_count_df))
    # filter out user with enough interactions
    users_with_enough_interactions_df = user_interactions_count_df[user_interactions_count_df>=min_interactions].reset_index()['user_id']

    print('# users with at least %d interactions: %d' % (min_interactions, len(users_with_enough_interactions_df)))  

    print('# of interactions: %d' % len(interactions_df))
    # choose selected user from interactions_df
    interactions_from_selected_users_df = interactions_df.merge(users_with_enough_interactions_df, 
                                                               how = 'right',
                                                               left_on = 'user_id',
                                                               right_on = 'user_id')
    print('# of interactions from users with at least %d interactions: %d' % (min_interactions, len(interactions_from_selected_users_df)))

    return interactions_from_selected_users_df    

if __name__ == '__main__':
    interactions_full_df = run()
    # interactions_full_df = filter_interactions(interactions_full_df, 5)
    print(interactions_full_df.head())