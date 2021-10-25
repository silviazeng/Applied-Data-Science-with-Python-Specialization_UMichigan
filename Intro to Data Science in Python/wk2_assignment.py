#---------------------------------------Assignment 2---------------------------------------

# QUESTION 1

# Write a function called proportion_of_education which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.

# This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

    # {"less than high school":0.2,
    # "high school":0.4,
    # "more than high school but not college":0.2,
    # "college":0.2}
    
def proportion_of_education():
    # your code goes here
    # YOUR CODE HERE
    import pandas as pd
    df = pd.read_csv('assets/NISPUF17.csv')
    ValueCounts = df['EDUC1'].value_counts()
    ValueCounts = ValueCounts.rename({1:'less than high school', 2:'high school', 3:'more than high school but not college', 4:'college'})
    #1: <12 years
    #2: 12 years
    #3:>12 years, not a college graduate
    #4: College graduate
    
    ValueProp = dict(ValueCounts/sum(ValueCounts))
    # if it needs to be rounded: ValueProp = ValueProp.round(2)
    
    return ValueProp
     
    
    raise NotImplementedError()
​
