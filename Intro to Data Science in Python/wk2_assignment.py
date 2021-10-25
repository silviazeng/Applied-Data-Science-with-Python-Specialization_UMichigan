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
    import pandas as pd
    df = pd.read_csv('assets/NISPUF17.csv')
    ValueCounts = df['EDUC1'].value_counts()
    ValueCounts = ValueCounts.rename({1:'less than high school', 2:'high school', 3:'more than high school but not college', 4:'college'})
    #1: <12 years
    #2: 12 years
    #3:>12 years, not a college graduate
    #4: College graduate
    
    ValueProp = dict(ValueCounts/sum(ValueCounts))  # if it needs to be rounded: ValueProp = ValueProp.round(2)
    
    return ValueProp
    raise NotImplementedError()


# QUESTION 2

# Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine from a healthcare provider. Return a tuple of the average number of influenza vaccines for those children we know received breastmilk as a child and those who know did not.
# This function should return a tuple in the form (use the correct numbers: (2.5, 0.1)

def average_influenza_doses():
    # YOUR CODE HERE
    import pandas as pd
    import numpy as np
    df = pd.read_csv('assets/NISPUF17.csv')
    df_r = df[['CBF_01','P_NUMFLU']] # !!!double brackets
    
    df_y = df_r[df_r['CBF_01'] == 1]  #breast milk -- Y
    df_n = df_r[df_r['CBF_01'] == 2]  #breast milk -- N
    avg_vacc_y = np.mean(df_y['P_NUMFLU'])
    avg_vacc_n = np.mean(df_n['P_NUMFLU'])
    tup = tuple((avg_vacc_y, avg_vacc_n))
    return tup
    
    raise NotImplementedError()
    
 
# QUESTION 3

# It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) versus those who were vaccinated but did not contract chicken pox. Return results by sex.
# This function should return a dictionary in the form of (use the correct numbers):
    # {"male":0.2,
    # "female":0.4}
# Note: To aid in verification, the chickenpox_by_sex()['female'] value the autograder is looking for starts with the digits 0.0077.
  
