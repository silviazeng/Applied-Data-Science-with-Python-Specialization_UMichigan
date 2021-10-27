#---------------------------------------Assignment 3---------------------------------------
# QUESTION 1

# Load the energy data from the file assets/Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of Energy.
#Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
  # ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]
# Convert Energy Supply to gigajoules (Note: there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.
# Rename the following list of countries (for use in later questions):
  #"Republic of Korea": "South Korea",
  #"United States of America": "United States",
  #"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
  #"China, Hong Kong Special Administrative Region": "Hong Kong"
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. 'Bolivia (Plurinational State of)' should be 'Bolivia'. 'Switzerland17' should be 'Switzerland'.
# Next, load the GDP data from the file assets/world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.
# Make sure to skip the header, and rename the following list of countries:
  #"Korea, Rep.": "South Korea", 
  #"Iran, Islamic Rep.": "Iran",
  #"Hong Kong SAR, China": "Hong Kong"
# Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file assets/scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".

def answer_one():
    # YOUR CODE (HERE)
    import pandas as pd
    # Load DF1: Energy
    Energy = pd.read_excel("assets/Energy Indicators.xls", usecols="C:F", skiprows=17, #or use drop.(range(:20)) instead of skiprows\ 
                        skipfooter=265-227, names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000).replace('...', np.NaN)
    Energy['Country'] = Energy['Country'].replace("\d| \(.*\)","", regex=True) #drop digits and brackets in country names
    Energy = Energy.replace({"Republic of Korea": "South Korea",\
                    "United States of America": "United States",\
                    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",\
                    "China, Hong Kong Special Administrative Region": "Hong Kong"})
    # check1 = Energy.iloc[[24,43,98, 164,214,216]]
    
    # Load DF2: GDP
    GDP = pd.read_csv("assets/world_bank.csv", skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",\
                                                       "Iran, Islamic Rep.": "Iran",\
                                                       "Hong Kong SAR, China": "Hong Kong"})
    #check2 = GDP.iloc[[93,109,123]]  
    
    # Load DF3: ScimEn
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")
    
    # Merge 3 DFs
    last_10_years = [str(year) for year in list(range(2006,2016,1))]
    last_10_years.append('Country Name')
    DF = pd.merge(Energy, GDP[last_10_years], how='inner', left_on='Country', right_on='Country Name')
    DF = pd.merge(DF, ScimEn.iloc[range(15)], how='inner', on='Country')
    DF= DF.drop('Country Name', axis=1).set_index('Country')
    DF = DF[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    DF = DF.sort_values('Rank')
    return DF
    
    raise NotImplementedError()
    
    
# QUESTION 2
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose? This function should return a single number.

def answer_two():
    # YOUR CODE HERE    
    # Reproduce the merge in Q1 (but how='outer' & excluding redundant steps):
    import pandas as pd
    # Load DF1: Energy
    Energy = pd.read_excel("assets/Energy Indicators.xls", usecols="C:F", skiprows=17, #or use drop.(range(:20)) instead of skiprows\ 
                        skipfooter=265-227, names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
    Energy['Country'] = Energy['Country'].replace("\d| \(.*\)","", regex=True) #drop digits and brackets in country names
    Energy = Energy.replace({"Republic of Korea": "South Korea",\
                    "United States of America": "United States",\
                    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",\
                    "China, Hong Kong Special Administrative Region": "Hong Kong"})
    # Load DF2: GDP
    GDP = pd.read_csv("assets/world_bank.csv", skiprows=4)
    GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",\
                                                       "Iran, Islamic Rep.": "Iran",\
                                                       "Hong Kong SAR, China": "Hong Kong"})
    # Load DF3: ScimEn
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")
    
    # Merge 3 DFs
    last_10_years = [str(year) for year in list(range(2006,2016,1))]
    last_10_years.append('Country Name')
    DF = pd.merge(Energy, GDP[last_10_years], how='outer', left_on='Country', right_on='Country Name')
    DF = pd.merge(DF, ScimEn, how='outer', on='Country').set_index('Country')
    DF = DF.sort_values('Rank')
    
    DF_r = DF.iloc[:15]
    diff = len(DF) - len(DF_r)
    return diff
    
    raise NotImplementedError()
    
    
# QUESTION 3
#What are the top 15 countries for average GDP over the last 10 years? 
#This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.

def answer_three():
    # YOUR CODE HERE
    DF = answer_one()[[str(y) for y in list(range(2006,2016,1))]]
    avgGDP = DF.apply(np.mean, axis=1).sort_values(ascending=False) #Default ascending=True
    return avgGDP

    raise NotImplementedError()
    
    
# QUESTION 4

#By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP? This function should return a single number.
def answer_four():
    # YOUR CODE HERE
    country6 = answer_three().index[5]
    DF = answer_one()[[str(y) for y in list(range(2006,2016,1))]]
    change = DF.loc[country6]['2015'] - DF.loc[country6]['2006']
    return change
       
    raise NotImplementedError()

    
# QUESTION 5
#What is the mean energy supply per capita? This function should return a single number.
def answer_five():
    # YOUR CODE HERE
    mean_espc = answer_one()['Energy Supply per Capita'].mean()
    return mean_espc
  
    raise NotImplementedError()
    
    
# QUESTION 6
#What country has the maximum % Renewable and what is the percentage? This function should return a tuple with the name of the country and the percentage.

def answer_six():
    # YOUR CODE HERE
    return (answer_one()['% Renewable'].idxmax(), answer_one()['% Renewable'].max())
    raise NotImplementedError()
    
    
# QUESTION 7
#Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?
#This function should return a tuple with the name of the country and the ratio.

def answer_seven():
    # YOUR CODE HERE
    DF = answer_one()[['Citations', 'Self-citations']]
    
    def ratio(series):
        return series['Self-citations'] / series['Citations']
    
    DF['citation ratio'] = DF.apply(ratio, axis=1)
    return (DF['citation ratio'].idxmax(), DF['citation ratio'].max())
    raise NotImplementedError()
        
    
# QUESTION 8
#Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
#This function should return the name of the country

def answer_eight():
    # YOUR CODE HERE
    DF = answer_one()
    def ratio(series):
        return series['Energy Supply'] / series['Energy Supply per Capita']
    
    DF['estimated pop'] = DF.apply(ratio, axis=1)
    return DF['estimated pop'].idxmax()
  
    raise NotImplementedError()
            
    
# QUESTION 9
#Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation). This function should return a single number.
#(Optional: Use the built-in function plot9() to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)

def answer_nine():
    # YOUR CODE HERE
    def ratio(series):
        estimated_pop = series['Energy Supply'] / series['Energy Supply per Capita']
        return series['Citable documents'] / estimated_pop
    
    DF = answer_one()
    DF['Citable docs per Capita'] = DF.apply(ratio, axis=1)
    DF['Energy Supply per Capita'] = [float(x) for x in DF['Energy Supply per Capita']]  # corr() can only apply to same data type!!!
    
    corr = DF[['Energy Supply per Capita','Citable docs per Capita']].corr()  
    return corr
    
    raise NotImplementedError()
                
    
# QUESTION 10
#Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median. This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.

def answer_ten():
    # YOUR CODE HERE
    DF = answer_one()
    benchmark = DF['% Renewable'].median()
    
    def above_median_or_not(series):
        if series['% Renewable'] >= benchmark:
            return 1
        else:
            return 0
    
    DF['HighRenew']=DF.apply(above_median_or_not, axis=1)
    HighRenew = DF['HighRenew'].sort_values()
    
    return HighRenew
    
    raise NotImplementedError()
             
    
# QUESTION 11   
       
#Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
#This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']

def answer_eleven():
    # YOUR CODE HERE
    import pandas as pd
    import numpy as np
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    DF = answer_one().reset_index()   # put 'Country' from idx back into a column
    DF['est_pop'] = (DF['Energy Supply'] / DF['Energy Supply per Capita']).astype(float)
    
    def gen_continent(Series):
        return ContinentDict[Series['Country']]    
    DF['Continent'] = DF.apply(gen_continent, axis=1)    
    continent_sum = DF.groupby('Continent').agg({'est_pop':(np.size, np.sum, np.nanmean, np.nanstd)})   
    return continent_sum
    
    raise NotImplementedError()
             
    
# QUESTION 12   
#Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
#This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.
def answer_twelve():
    # YOUR CODE HERE
    import pandas as pd
    import numpy as np
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    DF = answer_one().reset_index()   # put 'Country' from idx back into a column
    
    def gen_continent(Series):
        return ContinentDict[Series['Country']]
    
    DF['Continent'] = DF.apply(gen_continent, axis=1)
    DF['% Renewable_bins'] = pd.cut(DF['% Renewable'], 5)
    
    DF = DF.set_index(['Continent','% Renewable_bins'])
    summ = DF.groupby(level=(0,1)).size() # to create a multi-index Series
    return summ
   
    raise NotImplementedError()
                 
    
# QUESTION 13

#Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results). 
#e.g. 12345678.90 -> 12,345,678.90
#This function should return a series PopEst whose index is the country name and whose values are the population estimate string

def answer_thirteen():
    # YOUR CODE HERE
    DF = answer_one()
    DF['est_pop'] = (DF['Energy Supply'] / DF['Energy Supply per Capita']).astype(float)    
    DF['PopEst']= DF['est_pop'].apply(lambda x: "{:,}".format(x))
    return DF['PopEst']
    
    raise NotImplementedError()


    
