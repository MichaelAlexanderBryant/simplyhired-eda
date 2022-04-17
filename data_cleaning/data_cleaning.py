"""Clean scraped data science jobs from SimplyHired job board."""

# Import libraries.
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import re
from ast import literal_eval
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.impute import KNNImputer


# Function containing cleaning, runs if script is executed.
def main():
    """Clean scraped data science jobs from SimplyHired job board."""

    # Load data.
    raw_data = pd.read_csv('../scraping/raw_data.csv')
    
    # Remove duplicate rows.
    raw_data = raw_data.loc[~raw_data.duplicated(), :]
    raw_data = raw_data.reset_index()
    raw_data = raw_data.drop('index', axis=1)
    
    # Convert all titles to lowercase.
    for i in range(len(raw_data)):
        raw_data.loc[i,'title'] = raw_data.loc[i,'title'].lower()
    
    # Initialize lists of indices.
    patent_indices = []
    leader_indices = []
    analyst_indices = []
    engineer_indices = []
    as_indices = []
    ds_indices = []
    software_indices = []
    architect_indices = []
    sci_indices = []
    math_indices = []
    mle_indices = []
    uncategorized_indices = []
    
    # Categorize titles and append indices to appropriate lists.
    for i in range(len(raw_data)):
        if 'patent' in raw_data.title[i]:
            patent_indices.append(i)
            
        elif ('manager' in raw_data.title[i] or 'vp' in raw_data.title[i] or
                           'director' in raw_data.title[i] or
                           'head' in raw_data.title[i] or
                           'vice president' in raw_data.title[i]):
            leader_indices.append(i)
            
        elif 'analyst' in raw_data.title[i]:
            analyst_indices.append(i)
            
        elif ('data engineer' in raw_data.title[i] or 
              'data science engineer' in raw_data.title[i]):
            engineer_indices.append(i)
            
        elif 'applied scientist' in raw_data.title[i]:
            as_indices.append(i)
    
        elif ('data scientist' in raw_data.title[i] or
              'data science' in raw_data.title[i]):
            ds_indices.append(i)
            
        elif ('developer' in raw_data.title[i] or
              'programmer' in raw_data.title[i] or
              'software' in raw_data.title[i] or
              'user experience' in raw_data.title[i] or
              'programming' in raw_data.title[i]):
            software_indices.append(i)
            
        elif 'architect' in raw_data.title[i]:
            architect_indices.append(i)
            
        elif 'scientist' in raw_data.title[i]:
            sci_indices.append(i)
            
        elif ('mathematician' in raw_data.title[i] or
              'statistician' in raw_data.title[i]):
            math_indices.append(i)
    
        elif ('machine learning' in raw_data.title[i] or
              'engineer' in raw_data.title[i]):
            mle_indices.append(i)
    
        else:
            uncategorized_indices.append(i)
            
    # Categorize leader titles.
    raw_data.iloc[leader_indices, :].title.unique()
    
    for i in leader_indices:
        
        if 'manager' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Data Science Manager'
            
        elif ('vp' in raw_data.loc[i, 'title'] or
              'vice president' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Vice President of Data Science'
            
        elif 'director' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Director of Data Science'
            
        else:
            raw_data.loc[i,'title'] = 'Head of Data Science'     
            
    raw_data.iloc[leader_indices, :].title.value_counts()
    
    # Categorize data analyst titles.
    raw_data.iloc[analyst_indices, :].title.unique()
    
    for i in analyst_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Data Analyst'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Data Analyst'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Data Analyst'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Data Analyst'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Data Analyst'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Data Analyst'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Data Analyst'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Data Analyst'
            
        else:
            raw_data.loc[i,'title'] = 'Data Analyst'
            
    raw_data.iloc[analyst_indices, :].title.value_counts()
    
    # Categorize data engineer titles.
    raw_data.iloc[engineer_indices, :].title.unique()
    
    for i in engineer_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Data Engineer'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Data Engineer'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Data Engineer'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Data Engineer'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Data Engineer'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Data Engineer'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Data Engineer'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Data Engineer'
            
        else:
            raw_data.loc[i,'title'] = 'Data Engineer'
            
    raw_data.iloc[engineer_indices, :].title.value_counts()
    
    # Categorize applied scientist titles.
    raw_data.iloc[as_indices, :].title.unique()
    
    for i in as_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Applied Scientist'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Applied Scientist'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Applied Scientist'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Applied Scientist'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Applied Scientist'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Applied Scientist'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Applied Scientist'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Applied Scientist'
            
        else:
            raw_data.loc[i,'title'] = 'Applied Scientist'
            
    raw_data.iloc[as_indices, :].title.value_counts()
    
    # Categorize data scientist titles.
    raw_data.iloc[ds_indices, :].title.unique()
    
    for i in ds_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Data Scientist'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Data Scientist'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Data Scientist'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Data Scientist'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Data Scientist'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Data Scientist'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Data Scientist'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Data Scientist'
            
        else:
            raw_data.loc[i,'title'] = 'Data Scientist'
            
    raw_data.iloc[ds_indices, :].title.value_counts()
    
    # Categorize software titles.
    raw_data.iloc[software_indices, :].title.unique()
    
    for i in software_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Software Engineer'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Software Engineer'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Software Engineer'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Software Engineer'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Software Engineer'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Software Engineer'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Software Engineer'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Software Engineer'
            
        else:
            raw_data.loc[i,'title'] = 'Software Engineer'
            
    raw_data.iloc[software_indices, :].title.value_counts()
    
    # Categorize architect titles.
    raw_data.iloc[architect_indices, :].title.unique()
    
    for i in architect_indices:
    
        if 'senior' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Sr. Data Architect'
            
        elif 'distinguished' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Distinguished Data Architect'
            
        else:
            raw_data.loc[i,'title'] = 'Data Architect'
            
    raw_data.iloc[architect_indices, :].title.value_counts()
    
    # Categorize scientist titles.
    raw_data.iloc[sci_indices, :].title.unique()
    
    for i in sci_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Machine Learning Scientist'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Machine Learning Scientist'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Machine Learning Scientist'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Machine Learning Scientist'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Machine Learning Scientist'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Machine Learning Scientist'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Machine Learning Scientist'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Machine Learning Scientist'
            
        else:
            raw_data.loc[i,'title'] = 'Machine Learning Scientist'
            
    raw_data.iloc[sci_indices, :].title.value_counts()
    
    # Categorize mathematician/statistician titles.
    raw_data.iloc[math_indices, :].title.unique()
    
    for i in math_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Statistician'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Statistician'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Statistician'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Statistician'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Statistician'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Statistician'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Statistician'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Statistician'
            
        else:
            raw_data.loc[i,'title'] = 'Statistician'
            
    raw_data.iloc[math_indices, :].title.value_counts()
    
    # Categorize machine learning engineer titles.
    raw_data.iloc[mle_indices, :].title.unique()
    
    for i in mle_indices:
        
        if ('entry' in raw_data.loc[i, 'title'] or
            'jr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Jr. Machine Learning Engineer'
            
        elif 'staff' in raw_data.loc[i, 'title']:
            raw_data.loc[i,'title'] = 'Staff Machine Learning Engineer'
            
        elif ('senior' in raw_data.loc[i, 'title'] or
              'sr' in raw_data.loc[i, 'title'] or
              'snr' in raw_data.loc[i, 'title']):
            raw_data.loc[i,'title'] = 'Sr. Machine Learning Engineer'
            
        elif ('principal' in raw_data.loc[i, 'title'] or
              'rincipal' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Principal Machine Learning Engineer'
            
        elif ('lead' in raw_data.loc[i, 'title'] or
              'lead data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Lead Machine Learning Engineer'
            
        elif (' iii' in raw_data.loc[i, 'title'] or
              ' 3' in raw_data.loc[i, 'title'] or
              'senior data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Sr. Machine Learning Engineer'
            
        elif (' ii' in raw_data.loc[i, 'title'] or
              ' 2' in raw_data.loc[i, 'title'] or
              'staff data' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Staff Machine Learning Engineer'
            
        elif (' i' in raw_data.loc[i, 'title'] or
              ' 1' in raw_data.loc[i, 'title'] or
              'entry' in raw_data.loc[i, 'description']):
            raw_data.loc[i,'title'] = 'Jr. Machine Learning Engineer'
            
        else:
            raw_data.loc[i,'title'] = 'Machine Learning Engineer'
            
    raw_data.iloc[mle_indices, :].title.value_counts()
    
    # Remaining uncategorized titles.
    raw_data.iloc[uncategorized_indices, :].title.unique()
    
    # Remove unwanted job postings, reset index, drop extra index column.
    raw_data = raw_data.drop(uncategorized_indices)
    raw_data = raw_data.drop(patent_indices)
    raw_data = raw_data.reset_index()
    raw_data = raw_data.drop('index', axis=1)
    
    # Display unique titles.
    raw_data.title.unique()
    
    # Replace [] with NaN for entire dataframe.
    raw_data = raw_data.replace('[]',np.nan)
    
    # Calculate missing values for each variable.
    print('Missing values per column')
    for i in raw_data.columns:
        print('{}: {} ({} %)'.format(i, sum(pd.isna(raw_data[i])),
                                     round(sum(pd.isna(raw_data[i]))/len(
                                         raw_data),3)*100))
        
    # Display unique locations.
    raw_data['location'].unique()
    
    # Locations with 'United States' not relevant to California analysis, so
    # drop job postings with 'United States' location from data, reset index,
    # drop extra index column.
    raw_data[raw_data.location == 'United States'].index
    raw_data = raw_data.drop(
        raw_data[raw_data.location == 'United States'].index)
    raw_data = raw_data.reset_index()
    raw_data = raw_data.drop('index', axis=1)
    
    # Some job postings do not specify city in California. Therefore, remove
    # location and impute by KNNImputer using company and salary.
    raw_data[raw_data.location == 'California']
    cali_loc = pd.DataFrame(raw_data[raw_data.location == 'California'])
    
    # View dataframe information, drop extra index column.
    raw_data.info()
    raw_data = raw_data.drop('Unnamed: 0', axis=1)
    
    # Remove ratings from company names.
    companies = raw_data.company
    
    # Regular expression to identify part of string at hypen before rating.
    pattern = re.compile('(-[^-]*){1}$')
    
    # Remove everything at hypen and after where [:-1] also removes space
    # before hypen.
    for i in raw_data[~pd.isna(raw_data.company)].index:
        raw_data.loc[i,'company'] = pattern.sub('',
                                                raw_data.loc[i,'company'])[:-1]
    
    # Data with missing companies also have missing locations. 
    company_na = pd.DataFrame(raw_data[pd.isna(raw_data.company)])
    
    # Display unique salaries.
    raw_data[~pd.isna(raw_data.salary)].salary.unique()
    
    # Remove 'quick apply' from salary and replace with NaN.
    for i in raw_data[~pd.isna(raw_data.salary)].index:
        if 'Quick' in raw_data.salary[i]:
            raw_data.loc[i,'salary'] = np.nan
    
    # Initialize salary columns.
    raw_data['est_salary'] = 0 #binary for estimated salary (1) or not (0)
    raw_data['annual_salary'] = 0 #binary for annual salary (1) or not (0)
    raw_data['hourly_salary'] = 0 #binary for hourly salary (1) or not (0)
    raw_data['one_num_salary'] = np.nan #column for exact one-number salaries
    raw_data['min_num_salary'] = np.nan #column for lower end of salary range
    raw_data['max_num_salary'] = np.nan #column for higher end of salary range
    
    # Remove '$', ',' '-', 'Estimated:', 'an', 'a', 'hour', 'year' from salary
    # and categorize cleaned salaries into columns.
    for i in raw_data[~pd.isna(raw_data.salary)].index:
        
        split_salary = raw_data.salary[i].split()
        
        if 'Estimated:' in split_salary:
            split_salary.remove('Estimated:')
            raw_data.loc[i,'est_salary'] = 1
        if '-' in split_salary:
            split_salary.remove('-')
        if 'a' in split_salary:
            split_salary.remove('a')
        if 'an' in split_salary:
            split_salary.remove('an')
        if 'year' in split_salary:
            split_salary.remove('year')
            raw_data.loc[i,'annual_salary'] = 1
        if 'hour' in split_salary:
            split_salary.remove('hour')
            raw_data.loc[i,'hourly_salary'] = 1
            
        if len(split_salary) == 1:
            split_salary = split_salary[0]
            double_split = [i for i in split_salary]
            if '$' in double_split:
                double_split.remove('$')
            if ',' in double_split:
                double_split.remove(',')
            split_salary = ''.join(double_split)
            raw_data.loc[i,'one_num_salary'] = float(split_salary)
            
        if len(split_salary) == 2:
            min_num = split_salary[0]
            max_num = split_salary[1]
            
            double_split_min = [i for i in min_num]
            if '$' in double_split_min:
                double_split_min.remove('$')
            if ',' in double_split_min:
                double_split_min.remove(',')
            min_num = ''.join(double_split_min)
            
            double_split_max = [i for i in max_num]
            if '$' in double_split_max:
                double_split_max.remove('$')
            if ',' in double_split_max:
                double_split_max.remove(',')
            max_num = ''.join(double_split_max)
    
            raw_data.loc[i,'min_num_salary'] = float(min_num)
            raw_data.loc[i,'max_num_salary'] = float(max_num)
                    
    # Calculate average salary from salaries given in a range.
    raw_data['avg_salary'] = (raw_data[~pd.isna(
        raw_data.salary)].max_num_salary +raw_data[~pd.isna(
            raw_data.salary)].max_num_salary)/2
    
    # Initialize cleaned salary column.
    raw_data['clean_salary'] = np.nan
    
    # Insert final cleaned salaries into clean_salary column and also convert
    # hourly salary to annual salary
    for i in range(len(raw_data)):
        
        if raw_data.one_num_salary[i] != np.nan:
            raw_data.loc[i,'clean_salary'] = raw_data.one_num_salary[i]
        if raw_data.avg_salary[i] != np.nan:
            raw_data.loc[i,'clean_salary'] = raw_data.avg_salary[i]
            
        if raw_data.hourly_salary[i] == 1:
            raw_data.loc[i,'clean_salary'] = raw_data.clean_salary[i]*40*52
            
    # Remove unnecessary columns.
    raw_data.info()
    raw_data = raw_data.drop('salary', axis=1)
    raw_data = raw_data.drop('one_num_salary', axis=1)
    raw_data = raw_data.drop('min_num_salary', axis=1)
    raw_data = raw_data.drop('max_num_salary', axis=1)
    raw_data = raw_data.drop('avg_salary', axis=1)
    
    # Calculate missing values for each variable.
    print('Missing values per column')
    for i in raw_data.columns:
        print('{}: {} ({} %)'.format(i, sum(pd.isna(raw_data[i])),
                                     round(sum(pd.isna(raw_data[i]))/len(
                                         raw_data),3)*100))
        
    # Inspect cleaned salaries with scatterplot.
    sns.scatterplot(raw_data.title, raw_data.clean_salary)
    
    # Initialize qualifications and benefits columns.
    raw_data['qualifications'] = np.nan
    raw_data['benefits'] = np.nan
    
    # Search benefits_qual1 and benefits_qual2 for keywords to categorize
    # entries into qualifications and benefits columns.
    for i in range(len(raw_data)):
        
        if not pd.isna(raw_data.loc[i,'benefits_qual1']):
            
            if ('sourcing' in raw_data.loc[i,'benefits_qual1'].lower() or
                'node' in raw_data.loc[i,'benefits_qual1'].lower() or
                'spark' in raw_data.loc[i,'benefits_qual1'].lower() or
                'java' in raw_data.loc[i,'benefits_qual1'].lower() or
                'clinical' in raw_data.loc[i,'benefits_qual1'].lower() or
                'automation' in raw_data.loc[i,'benefits_qual1'].lower() or
                'software' in raw_data.loc[i,'benefits_qual1'].lower() or
                'master' in raw_data.loc[i,'benefits_qual1'].lower() or
                'natural' in raw_data.loc[i,'benefits_qual1'].lower() or
                'tensorflow' in raw_data.loc[i,'benefits_qual1'].lower() or
                'pytorch' in raw_data.loc[i,'benefits_qual1'].lower() or
                'machine learning' in raw_data.loc[i,'benefits_qual1'].lower()
                or 'c++' in raw_data.loc[i,'benefits_qual1'].lower() or
                'research' in raw_data.loc[i,'benefits_qual1'].lower() or
                'python' in raw_data.loc[i,'benefits_qual1'].lower() or
                'sql' in raw_data.loc[i,'benefits_qual1'].lower() or
                'tableau' in raw_data.loc[i,'benefits_qual1'].lower() or
                'power bi' in raw_data.loc[i,'benefits_qual1'].lower() or
                'excel' in raw_data.loc[i,'benefits_qual1'].lower() or
                'sas' in raw_data.loc[i,'benefits_qual1'].lower() or
                'data' in raw_data.loc[i,'benefits_qual1'].lower() or
                'skills' in raw_data.loc[i,'benefits_qual1'].lower()):
                raw_data.loc[i,
                             'qualifications'] =raw_data.loc[i,
                                                             'benefits_qual1']
                
            elif ('relocation' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'sponsorship' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'assistance' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'leave' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'flexible' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'from home' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'unlimited' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'advancement' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'health' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'stock' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'insurance' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'remote' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'paid' in raw_data.loc[i,'benefits_qual1'].lower() or
                  'tuition' in raw_data.loc[i,'benefits_qual1'].lower() or
                  '401' in raw_data.loc[i,'benefits_qual1'] or
                  'dental' in raw_data.loc[i,'benefits_qual1'].lower()):
                raw_data.loc[i,'benefits'] = raw_data.loc[i,'benefits_qual1']
                
        if not pd.isna(raw_data.loc[i,'benefits_qual2']):
            
            if ('sourcing' in raw_data.loc[i,'benefits_qual2'].lower() or
                'node' in raw_data.loc[i,'benefits_qual2'].lower() or
                'spark' in raw_data.loc[i,'benefits_qual2'].lower() or
                'java' in raw_data.loc[i,'benefits_qual2'].lower() or
                'clinical' in raw_data.loc[i,'benefits_qual2'].lower() or
                'automation' in raw_data.loc[i,'benefits_qual2'].lower() or
                'software' in raw_data.loc[i,'benefits_qual2'].lower() or
                'master' in raw_data.loc[i,'benefits_qual2'].lower() or
                'natural' in raw_data.loc[i,'benefits_qual2'].lower() or
                'tensorflow' in raw_data.loc[i,'benefits_qual2'].lower() or
                'pytorch' in raw_data.loc[i,'benefits_qual2'].lower() or
                'learning' in raw_data.loc[i,'benefits_qual2'].lower() or
                'c++' in raw_data.loc[i,'benefits_qual2'].lower() or
                'research' in raw_data.loc[i,'benefits_qual2'].lower() or
                'python' in raw_data.loc[i,'benefits_qual2'].lower() or
                'sql' in raw_data.loc[i,'benefits_qual2'].lower() or
                'tableau' in raw_data.loc[i,'benefits_qual2'].lower() or
                'power bi' in raw_data.loc[i,'benefits_qual2'].lower() or
                'excel' in raw_data.loc[i,'benefits_qual2'].lower() or
                'sas' in raw_data.loc[i,'benefits_qual2'].lower() or
                'data' in raw_data.loc[i,'benefits_qual2'].lower() or
                'skills' in raw_data.loc[i,'benefits_qual2'].lower()):
                raw_data.loc[i,
                             'qualifications'] = raw_data.loc[i,
                                                              'benefits_qual2']
                
            elif ('relocation' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'sponsorship' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'assistance' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'leave' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'flexible' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'from home' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'unlimited' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'advancement' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'health' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'stock' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'insurance' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'remote' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'paid' in raw_data.loc[i,'benefits_qual2'].lower() or
                  'tuition' in raw_data.loc[i,'benefits_qual2'].lower() or
                  '401' in raw_data.loc[i,'benefits_qual2'] or
                  'dental' in raw_data.loc[i,'benefits_qual2'].lower()):
                raw_data.loc[i,'benefits'] = raw_data.loc[i,'benefits_qual2']
    
    # Drop benefits_qual columns.
    raw_data.info()
    raw_data = raw_data.drop('benefits_qual1', axis=1)
    raw_data = raw_data.drop('benefits_qual2', axis=1)
    
    # Clean qualifications and benefits, create binary predictors for each
    # unique entry, and retrieve unique qualifications
    qualifications = []
    for i in raw_data.qualifications:
        if not pd.isna(i):
            a = literal_eval(i) #converts list stored as string to actual list
            for j in a:
                qualifications.append(j)
    unique_qualifications = list(pd.Series(qualifications).unique())
    
    # Display value counts for qualifications.
    pd.Series(qualifications).value_counts()
    
    # Retrieve unique benefits.
    benefits = []
    for i in raw_data.benefits:
        if not pd.isna(i):
            a = literal_eval(i) #converts list stored as string to actual list
            for j in a:
                benefits.append(j)
    unique_benefits = list(pd.Series(benefits).unique())
    
    # Display value counts for benefits.
    pd.Series(benefits).value_counts()
    
    # Create a zeros matrix with columns with unique qualifications.
    qual_df = pd.DataFrame(np.zeros((raw_data.shape[0],
                                     len(unique_qualifications))))
    qual_df.columns = unique_qualifications
     
    # Put ones in the matrix for postings that contain each qualification.
    for i in range(len(raw_data)):  
        for j in unique_qualifications:
            if not pd.isna(raw_data.qualifications[i]):
                if j in raw_data.qualifications[i]:
                    qual_df.loc[i,j] = 1
                    
    # Create a zeros matrix with columns with unique benefits.          
    benefits_df = pd.DataFrame(np.zeros((raw_data.shape[0],
                                         len(unique_benefits))))
    benefits_df.columns = unique_benefits
     
    # Put ones in the matrix for postings that contain each benefit.
    for i in range(len(raw_data)):  
        for j in unique_benefits:
            if not pd.isna(raw_data.benefits[i]):
                if j in raw_data.benefits[i]:
                    benefits_df.loc[i,j] = 1
     
    # For rows which are entirely zeros, replace entries with np.nan.
    # Insert np.nan into qualifications binary matrix.
    for i in range(len(raw_data)):
        if sum(qual_df.loc[i,:]) == 0:
            for j in qual_df.columns:
                qual_df.loc[i,j] = np.nan
    # Inswer np.nan into benefits binary matrix.         
    for i in range(len(raw_data)):
        if sum(benefits_df.loc[i,:]) == 0:
            for j in benefits_df.columns:
                benefits_df.loc[i,j] = np.nan
                
    # Count the number of mentions of each job qualification.            
    total_qual = pd.DataFrame(qual_df.sum(axis=0))
    total_qual.columns = ['Counts']
    total_qual.sort_values(by=['Counts'], ascending=False)
    
    # Count number of mentions of each job benefit.
    total_benefits = pd.DataFrame(benefits_df.sum(axis=0))
    total_benefits.columns = ['Counts']
    total_benefits.sort_values(by=['Counts'], ascending=False)
    
    # Display value counts for number of job posting salaries.
    raw_data.info()
    raw_data.est_salary.value_counts()
    raw_data.annual_salary.value_counts()
    
    # Remove unnecessary columns for modeling.
    raw_data.info()
    raw_data = raw_data.drop('description', axis=1)
    raw_data = raw_data.drop('est_salary', axis=1)
    raw_data = raw_data.drop('annual_salary', axis=1)
    raw_data = raw_data.drop('hourly_salary', axis=1)
    raw_data = raw_data.drop('qualifications', axis=1)
    raw_data = raw_data.drop('benefits', axis=1)
    raw_data.info()
    
    # Capitalize column names.
    raw_data.columns = ['Title', 'Company', 'Location', 'Salary']
    raw_data.info()
    
    # Arrays with all possible positions and levels.
    positions = ['Manager', 'Vice President', 'Director', 'Head',
                 'Data Analyst', 'Data Engineer', 'Applied Scientist',
                 'Data Scientist', 'Software Engineer', 'Data Architect',
                 'Machine Learning Scientist', 'Statistician',
                 'Machine Learning Engineer']
    levels = ['Jr.', 'Staff', 'Sr.', 'Principal', 'Lead', 'Distinguished',
              'Unknown']
    
    # Create columns filled with zeros and names from levels array.
    raw_data = pd.concat([raw_data.reset_index(),
                          pd.DataFrame(np.zeros((raw_data.shape[0],
                                                 len(levels))),
                                       columns = levels)], axis=1)
    
    # Drop extra index column.
    raw_data.info()
    raw_data = raw_data.drop('index', axis=1)
    
    # Seperate Levels and Title creating a binary matrix for levels.
    for j in levels:
        for k in range(len(raw_data)):
            if j in raw_data.loc[k,'Title']:
                raw_data.loc[k,j] = 1
                if 'Data Analyst' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Data Analyst'
                if 'Data Engineer' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Data Engineer'
                if 'Machine Learning Engineer' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Machine Learning Engineer'
                if 'Data Scientist' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Data Scientist'
                if 'Software Engineer' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Software Engineer'
                if 'Statistician' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Statistician'
                if 'Applied Scientist' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Applied Scientist'
                if 'Data Architect' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Data Architect'
                if 'Machine Learning Scientist' in raw_data.loc[k,'Title']:
                    raw_data.loc[k,'Title'] = 'Machine Learning Scientist'
    
    # For rows with Levels columns containing all zeros, add a one to the
    # Unknown level column.          
    for i in range(len(raw_data)):
        if raw_data.iloc[i,4:].sum() == 0:
            raw_data.loc[i,'Unknown'] = 1
    
    # Convert binary matrix to integer data type.      
    for i in levels:
        raw_data.loc[:,i] = raw_data.loc[:,i].astype('Int64')     
    
    # Stack levels binary matrix into one column and include in dataframe. 
    x = raw_data.iloc[:,4:].stack()
    raw_data['Levels'] = pd.Series(
        pd.Categorical(x[x!=0].index.get_level_values(1)))
    
    # Drop levels binary matrix.
    for i in levels:
        raw_data = raw_data.drop(i, axis=1)
    
    # Display columns and information.  
    raw_data.info()
    
    # Convert qualifications and benefits binary matricies to integer data
    # types.
    for i in qual_df.columns:
        qual_df.loc[:,i] = qual_df.loc[:,i].astype('Int64')  
    for i in benefits_df.columns:
        benefits_df.loc[:,i] = benefits_df.loc[:,i].astype('Int64')
        
    # Remove rows with a 'California' location and replace with np.nan.
    for i in raw_data.loc[raw_data.Location == 'California', :].index:
        raw_data.loc[i, 'Location'] = np.nan
    
    
    # Export data for EDA:
    # Dataframe with title, locations,companies, and salaries.
    df_title_loc_comp_salary = raw_data
    # Dataframe with qualifications (binary matrix).
    df_qualifications = qual_df
    # Dataframe with benefits (binary matrix).
    df_benefits = benefits_df
    # Export data to CSV files
    df_title_loc_comp_salary.to_csv('df_title_loc_comp_salary.csv')
    df_qualifications.to_csv('df_qualifications.csv')
    df_benefits.to_csv('df_benefits.csv')
    
    #Imputation by SimpleImputer and KNNImputer:
    
    # "Most frequent" SimpleImputer for location.
    imp_most_frequent = SimpleImputer(missing_values=np.nan,
                                      strategy='most_frequent')
    raw_data.loc[:,'Location'] = imp_most_frequent.fit_transform(
        raw_data.loc[:,'Location'].values.reshape(-1,1))
    
    # Dataframe without missing companies.
    knn_impute_salary = raw_data[~pd.isna(raw_data.Company)].loc[:,['Title',
                                                                    'Company',
                                                                    'Location',
                                                                    'Salary']]
    
    # Find optimal k for KNNImputer using KNeighborsRegressor
    # Dataframe without missing companies and missing salary.
    no_na_salary = knn_impute_salary.loc[~pd.isna(knn_impute_salary.Salary),:]
    
    # X and y dataframes, create dummies for X.
    X = no_na_salary.copy()
    y = no_na_salary.pop('Salary')
    X = pd.get_dummies(X)
    
    # Perform train-test-split.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25,
                                                        random_state = 1)
    
    # Function to output best parameters for model.
    def reg_performance(regressor, model_name):
        print(model_name)
        print('Best Score: {} +/- {}'.format(str(regressor.best_score_),str(
            regressor.cv_results_['std_test_score'][regressor.best_index_])))
        print('Best Parameters: ' + str(regressor.best_params_))
    
    # GridSearchCV for optimal parameters using KNeighborsRegressor.
    knn = KNeighborsRegressor()
    param_grid = { 'n_neighbors' : np.arange(1,15,1),
                   'weights' : ['uniform','distance']}
    reg_knn = GridSearchCV(knn,
                           param_grid = param_grid, cv = 10,
                           scoring='neg_mean_squared_error', n_jobs = -1)
    best_reg_knn = reg_knn.fit(X_train,y_train)
    reg_performance(best_reg_knn,'kNeighborsRegressor')
    
    # KNeighborsRegressor performance metrics with optimal parameters.
    knn = KNeighborsRegressor(n_neighbors= 2, weights= 'distance')
    knn.fit(X_train,y_train)
    pred_knn = knn.predict(X_test)
    print('KNeighborsRegressor')
    print('MSE: {}'.format(mean_squared_error(y_test,pred_knn)))
    print('RMSE: {}'.format(np.sqrt(mean_squared_error(y_test,pred_knn))))
    print('MAE: {}'.format(mean_absolute_error(y_test,pred_knn)))
    print('R-squared: {}'.format(r2_score(y_test,pred_knn)))
    
    # Impute salary with KNNImputer with optimal values.
    knn_impute_salary = pd.get_dummies(knn_impute_salary)
    imputer = KNNImputer(n_neighbors=2, weights='distance')
    result = pd.DataFrame(imputer.fit_transform(knn_impute_salary))
    
    # Imputed salary column.
    imputed_salary = result.iloc[:,0]
    
    # Insert imputed values into original dataframe (two rows were not used due
    # to missing company and location).
    j = 0
    for i in raw_data[~pd.isna(raw_data.Company)].index:
        raw_data.loc[i,'Salary'] = imputed_salary[j]
        j+=1
    
    # Impute missing Location and Company with "most frequent" values.
    raw_data.loc[:,['Location','Company']] = imp_most_frequent.fit_transform(
        raw_data.loc[:,['Location','Company']])
    raw_data.info()
    
    # Impute missing Qualifications with "most frequent" values
    imputer_most_frequent = SimpleImputer(
        missing_values=np.nan, strategy='most_frequent')
    qual_df = pd.DataFrame(
        imputer_most_frequent.fit_transform(qual_df),
        columns = unique_qualifications)
    pd.isna(qual_df).sum().sum()
    
    # Too many missing benefits to use for modeling, so no imputation.
    
    # Export data for modeling:
    
    # Combine original dataframe with qualifications dataframe.
    df_1 = pd.concat([raw_data, qual_df], axis=1)
    df_1.shape
    df_1.columns
    
    # Create dummy variables for modeling where multicollinearity doesn't
    # matter (no drop_first).
    df_modeling = pd.DataFrame(pd.get_dummies(df_1.copy()))
    
    # Export to CSV file.
    df_modeling.to_csv('df_modeling.csv')
    
    # Create dummy variables while dropping first for models where
    # multicollinearity matters.
    df_modeling_drop_first = pd.DataFrame(pd.get_dummies(df_1.copy(),
                                                         drop_first=True))
    
    # Array with dropped columns from dummy creation (used for interpretting
    # model).
    dropped_columns = list(set(df_modeling.columns) -
                           set(df_modeling_drop_first.columns))
    
    # Export dataframes to CSVs.
    df_modeling_drop_first.to_csv('df_modeling_drop_first.csv')
    pd.DataFrame(dropped_columns).to_csv('dropped_columns.csv')
    
if __name__ == "__main__":
    main()
