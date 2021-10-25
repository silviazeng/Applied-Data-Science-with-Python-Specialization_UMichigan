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

def chickenpox_by_sex():
    # YOUR CODE HERE
    import pandas as pd
    df = pd.read_csv('assets/NISPUF17.csv')
    df_r = df[['SEX','HAD_CPOX','P_NUMVRC']] 
    # 'SEX' = 1: Male; 2: Female
    # 'Had_CPOX' = 1: Yes; 2:No; 3: Don't know; 4: Refused; 5:Missing
    
    df_male = df_r[(df_r['SEX']==1) & (df_r['P_NUMVRC']>=1)]
    df_female = df_r[(df_r['SEX']==2) & (df_r['P_NUMVRC']>=1)]
    
    male_ratio = len(df_male[df_male['HAD_CPOX']==1])/len(df_male[df_male['HAD_CPOX']==2])
    female_ratio = len(df_female[df_female['HAD_CPOX']==1])/len(df_female[df_female['HAD_CPOX']==2])   
    
    dic = {'male': male_ratio, 'female': female_ratio}
    
    return dic
    
    raise NotImplementedError()
  

# QUESTION 4
# A correlation is a statistical relationship between two variables. If we wanted to know if vaccines work, we might look at the correlation between the use of the vaccine and whether it results in prevention of the infection or disease [1]. In this question, you are to see if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses given (varicella).
# Some notes on interpreting the answer. The had_chickenpox_column is either 1 (for yes) or 2 (for no), and the num_chickenpox_vaccine_column is the number of doses a child has been given of the varicella vaccine. A positive correlation (e.g., corr > 0) means that an increase in had_chickenpox_column (which means more no’s) would also increase the values of num_chickenpox_vaccine_column (which means more doses of vaccine). If there is a negative correlation (e.g., corr < 0), it indicates that having had chickenpox is related to an increase in the number of vaccine doses.
# Also, pval is the probability that we observe a correlation between had_chickenpox_column and num_chickenpox_vaccine_column which is greater than or equal to a particular value occurred by chance. A small pval means that the observed correlation is highly unlikely to occur by chance. In this case, pval should be very small (will end in e-18 indicating a very small number).
# [1] This isn’t really the full picture, since we are not looking at when the dose was given. It’s possible that children had chickenpox and then their parents went to get them the vaccine. Does this dataset have the data we would need to investigate the timing of the dose?

def corr_chickenpox():
    import scipy.stats as stats
    import numpy as np
    import pandas as pd
    
    # this is just an example dataframe
    df=pd.DataFrame({"had_chickenpox_column":np.random.randint(1,3,size=(100)),
                   "num_chickenpox_vaccine_column":np.random.randint(0,6,size=(100))})

    # here is some stub code to actually run the correlation
    corr, pval=stats.pearsonr(df["had_chickenpox_column"],df["num_chickenpox_vaccine_column"])
    
    # just return the correlation
    #return corr

    # YOUR CODE HERE
    df = pd.read_csv('assets/NISPUF17.csv')
    df_r = df[['HAD_CPOX','P_NUMVRC']].dropna()     # 'Had_CPOX' = 1: Yes; 2:No; 3: Don't know; 4: Refused; 5:Missing
    corr, pval = stats.pearsonr(df_r['HAD_CPOX'], df_r['P_NUMVRC'])
    
    return corr
    
    raise NotImplementedError()
  
