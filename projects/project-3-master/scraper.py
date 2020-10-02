# Standards
import pandas as pd
import numpy as np

# API
import requests

# Automating
import time
import datetime
import warnings
import sys
import datetime
import os

class reddit_scraper:
    
    def __init__(self,subreddit, n_iter, epoch_right_now):
        '''
        I recommend n_iter to be low, no higher than 10 
        
        n_iter  = how many times you want to scrape 100 reddit messages
        epoch_right_now = start here
        subreddit = name of subreddit in a string
        '''
        self.subreddit = subreddit
        self.n_iter = n_iter
        self.epoch_start = epoch_right_now
        self.epoch_earliest = 0
        
        # check for folder, is it does not exist make the folder
        try:
            os.makedirs(f'./data/reddit/{self.subreddit}', exist_ok=True)
        except OSError as e:
            if e.errno != errno.EEXIST:
                pass
        
        
    def get_comments(self, subreddit, n_iter, epoch_right_now): # subreddit name and number of times function should run

        # store base url variable
        base_url = 'https://api.pushshift.io/reddit/search/submission/?subreddit='
        # instantiate empty list    
        df_list = []
        # save current epoch, 
        current_time = epoch_right_now

        # set up for loop
        for post in range(n_iter):
            # instantiate get request
            #time.sleep(5)
            res = requests.get(
                # requests.get takes base_url and params
                base_url,
                # parameters for get request
                params={ 
                    # specify subreddit
                    'subreddit': subreddit,
                    # specify number of posts to pull
                    'size': 100,
                    # ???
                    'lang': True,
                    # pull everything from current time backward
                    'before': current_time})

            # take data from most recent request, store as df
            df = pd.DataFrame(res.json()['data'])

            # pull specific columns from dataframe for analysis
            try:
                df_filtered = df.T.loc[['title', 'created_utc', 'selftext', 'subreddit', 'media_only', 'author', 'permalink']]
            except:
                df_filtered = df.T.loc[['title', 'created_utc', 'selftext', 'subreddit', 'author', 'permalink']]
                #print(f'Stopped at {self.epoch_earliest}')
            except:
                
                
            # append to empty dataframe list
            df_list.append(df_filtered)

            # set current time counter back to last epoch in recently grabbed df
            current_time = df['created_utc'].min()
            self.epoch_earliest = current_time
        # return one dataframe for all requests
        df = pd.concat(df_list, axis=1)
        df = df.T
        return df.reset_index()
    # Adapated from Tim Book's Lesson Example

    def reddit_getter(self,sessions):
        '''
        This function multiplies n_iter by sessions, resulting in a total amount of requested scraped datapoints
        
        The amount scraped each request is 100 comments and their associated metadata
        
        The sessions define how many scraping sessions there will be
        
        Eg: n_iter = 10, sessions = 1 # hard define request = 100
        Total Scraped Message = 10 * 100 * 1 = 1000
        
        n_iter = 10, sessions = 100
        Total Scraped Messages = 10 * 100 * 1000 = 1000000
        
        Use this function to contuinopusly scrape because it has a wait timer to ensure reddit is not overloaded. It is set to a 2 second wait 
        '''
                
        for i in range(sessions):
            print('earliest',self.epoch_earliest,'starting',self.epoch_start)
            # scrape reddit based on inputted parameters when instantiating class
            time.sleep(10)
            scraped = self.get_comments(subreddit='askengineers', n_iter=self.n_iter, epoch_right_now=self.epoch_start)

            #after messages have been scraped, store amount into a single csv, 
            scraped.to_csv(f'./data/reddit/{self.subreddit}/comments_epoch_{self.epoch_earliest}-{self.epoch_start}.csv', index=False)

            # define the starting point as the epoch with the smallest epoch and go backwards again
            #print('earliest',rs.epoch_earliest, 'starting',rs.epoch_start)
            self.epoch_start = self.epoch_earliest
            
            # print out log for user to monitor amount collectec
            print(f'Scraped {(i+1) * self.n_iter * 100} of {sessions*self.n_iter*100} requested comments from subreddit {self.subreddit}')
        return f'Scraping complete, collected {self.n_iter * sessions*100} of reddit comments from subreddit {self.subreddit}'
        