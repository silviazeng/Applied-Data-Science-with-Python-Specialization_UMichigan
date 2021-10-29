#---------------------------------------Assignment 4---------------------------------------
#Description
#In this assignment you must read in a file of metropolitan regions and associated sports teams from assets/wikipedia_data.html and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in assets/nfl.csv), MLB (baseball, in assets/mlb.csv), NBA (basketball, in assets/nba.csv or NHL (hockey, in assets/nhl.csv). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
#For each sport I would like you to answer the question: what is the win/loss ratio's correlation with the population of the city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with pearsonr, so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%*4=80%) of the grade for this assignment. You should only use data from year 2018 for your analysis -- this is important!


# QUESTION 1
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NHL using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def nhl_correlation(): 
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # YOUR CODE HERE
    
    # 1. process nhl_df      
    DivisionNames = [x for x in nhl_df['GP'] if x.isnumeric()==False]
    
    nhl_df = nhl_df.drop(nhl_df[nhl_df['team'].isin(DivisionNames)].index)  #Drop Division rows
    
    nhl_df = nhl_df[nhl_df['year']==2018]  #keep data from year 2018 only
    
    nhl_df['team'] = nhl_df['team'].replace("\*","", regex=True) #drop "*" in team names
    
    nhl_df[['W','L']] = nhl_df[['W','L']].apply(pd.to_numeric)
    
    def winlossratio(series):
        return series['W']/(series['W']+series['L'])
    nhl_df['win_loss_ratio'] = nhl_df.apply(winlossratio, axis=1)

    # 2. process cities
    cities['NHL'] = cities['NHL'].replace("\[.*\]","", regex=True) #drop "[...]" in team names
    
    def split_team_name(str):
        splits = re.findall(r'([A-Z][a-z]+([ ][A-Z][a-z]+)*)', str)
        if splits == []:
            return []
        else:
            return pd.DataFrame(splits)[0].tolist()
    cities['NHL'] = cities['NHL'].apply(split_team_name)

    # 3. create a 'WLRatio' col in cities
        #shorten the team name in nhl_df:
    team_list = []
    for i in range(len(cities)):
        team_list = team_list + cities['NHL'][i]
        
    for team in team_list:
        nhl_df['team'][nhl_df['team'][nhl_df['team'].str.contains(team)==True].index] = team
    nhl_df = nhl_df.set_index('team')
    
        #calculate the avg ratio
    def avg_WLRatio(Series):
        teams = Series['NHL']
        return nhl_df.loc[teams]['win_loss_ratio'].mean()
    cities['avg_Ratio'] = cities.apply(avg_WLRatio, axis=1)
    
    cities.dropna(subset=['avg_Ratio'],inplace=True)
    
    population_by_region = pd.to_numeric(cities['Population (2016 est.)[8]'])  # pass in metropolitan area population from cities
    win_loss_by_region = pd.to_numeric(cities['avg_Ratio']) # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"  
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

    raise NotImplementedError()
    

# QUESTION 2
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NBA using 2018 data.
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def nba_correlation():
    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # YOUR CODE HERE
     
    # 1. process nba_df      
    nba_df = nba_df[nba_df['year']==2018]  #keep data from year 2018 only
    
    nba_df['team'] = nba_df['team'].replace("\*.*|\s\(.*\)","", regex=True) #clean team names
   
    nba_df['W/L%'] = nba_df['W/L%'].apply(pd.to_numeric)
    
    # 2. process cities
    cities['NBA'] = cities['NBA'].replace("\[.*\]","", regex=True) #drop "[...]" in team names
 
    def split_team_name(str):
        splits = re.findall(r'[A-Z][a-z]+|\d{2}.*', str)
        if splits == []:
            return []
        else:
            return pd.DataFrame(splits)[0].tolist()
    cities['NBA'] = cities['NBA'].apply(split_team_name)

    # 3. create a 'WLRatio' col in cities
        #shorten the team name in nba_df:
    team_list = []
    for i in range(len(cities)):
        team_list = team_list + cities['NBA'][i]
        
    for team in team_list:
        nba_df['team'][nba_df['team'][nba_df['team'].str.contains(team)==True].index] = team
    nba_df = nba_df.set_index('team')
 
        #calculate the avg ratio
    def avg_WLRatio(Series):
        teams = Series['NBA']
        return nba_df.loc[teams]['W/L%'].mean()
    cities['avg_Ratio'] = cities.apply(avg_WLRatio, axis=1)
    
    cities.dropna(subset=['avg_Ratio'],inplace=True)
  
    population_by_region = pd.to_numeric(cities['Population (2016 est.)[8]']) # pass in metropolitan area population from cities
    win_loss_by_region = pd.to_numeric(cities['avg_Ratio'])  # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
 
    raise NotImplementedError() 
      

# QUESTION 3
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the MLB using 2018 data.
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def mlb_correlation(): 
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # YOUR CODE HERE
     
    # 1. process mlb_df      
    mlb_df = mlb_df[mlb_df['year']==2018]  #keep data from year 2018 only
    mlb_df['W-L%'] = mlb_df['W-L%'].apply(pd.to_numeric)

    # 2. process cities
    cities['MLB'] = cities['MLB'].replace("\[.*\]","", regex=True) #drop "[...]" in team names

    def split_team_name(str):
        splits = re.findall(r'([A-Z][a-z]+([ ][A-Z][a-z]+)*)', str)
        if splits == []:
            return []
        else:
            return pd.DataFrame(splits)[0].tolist()
    cities['MLB'] = cities['MLB'].apply(split_team_name)


    # 4. create a 'WLRatio' col in cities
        #shorten the team name in nba_df:
    team_list = []
    for i in range(len(cities)):
        team_list = team_list + cities['MLB'][i]
        
    for team in team_list:
        mlb_df['team'][mlb_df['team'][mlb_df['team'].str.contains(team)==True].index] = team
    mlb_df = mlb_df.set_index('team')

        #calculate the avg ratio
    def avg_WLRatio(Series):
        teams = Series['MLB']
        return mlb_df.loc[teams]['W-L%'].mean()
    cities['avg_Ratio'] = cities.apply(avg_WLRatio, axis=1)
    
    cities.dropna(subset=['avg_Ratio'],inplace=True)

    population_by_region = pd.to_numeric(cities['Population (2016 est.)[8]']) # pass in metropolitan area population from cities
    win_loss_by_region = pd.to_numeric(cities['avg_Ratio'])  # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
    raise NotImplementedError()


# QUESTION 4
#For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data.
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def nfl_correlation(): 
    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # YOUR CODE HERE
    
    # 1. process nfl_df      
    DivisionNames = [x for x in nfl_df['L'] if x.isnumeric()==False]
    
    nfl_df = nfl_df.drop(nfl_df[nfl_df['team'].isin(DivisionNames)].index)  #Drop Division rows
    
    nfl_df = nfl_df[nfl_df['year']==2018]  #keep data from year 2018 only
    
    nfl_df['team'] = nfl_df['team'].replace("\*","", regex=True) #drop "*" in team names
    
    nfl_df[['W-L%']] = nfl_df[['W-L%']].apply(pd.to_numeric)

    # 2. process cities
    cities['NFL'] = cities['NFL'].replace("\[.*\]","", regex=True) #drop "[...]" in team names
  
    def split_team_name(str):
        splits = re.findall(r'[A-Z][a-z]+|\d{2}[^A-Z]*', str)
        if splits == []:
            return []
        else:
            return pd.DataFrame(splits)[0].tolist()
    cities['NFL'] = cities['NFL'].apply(split_team_name)

    # 3. create a 'WLRatio' col in cities
        #shorten the team name in nfl_df:
    team_list = []
    for i in range(len(cities)):
        team_list = team_list + cities['NFL'][i]
        
    for team in team_list:
        nfl_df['team'][nfl_df['team'][nfl_df['team'].str.contains(team)==True].index] = team
    nfl_df = nfl_df.set_index('team')
     
        #calculate the avg ratio
    def avg_WLRatio(Series):
        teams = Series['NFL']
        return nfl_df.loc[teams]['W-L%'].mean()
    cities['avg_Ratio'] = cities.apply(avg_WLRatio, axis=1)
    
    cities.dropna(subset=['avg_Ratio'],inplace=True)
    
    population_by_region = pd.to_numeric(cities['Population (2016 est.)[8]'])  # pass in metropolitan area population from cities
    win_loss_by_region = pd.to_numeric(cities['avg_Ratio']) # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]
    
    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# QUESTION 5
#In this question I would like you to explore the hypothesis that given that an area has two sports teams in different sports, those teams will perform the same within their respective sports. How I would like to see this explored is with a series of paired t-tests (so use ttest_rel) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.
  











    
