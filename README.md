# SimplyHired Data Science Jobs EDA

This repository is for the analysis of data science jobs posted to the website [SimplyHired](https://www.simplyhired.com/). Below you will find an overview of the data collection, data cleaning, and exploratory data analysis results. I created this project to help me understand the types of jobs in data science, their qualifications and benefits, locations, and salary ranges.

### Code Used 

**Python Version:** 3.9.7 <br />
**Packages:** numpy, pandas, scipy, matplotlib, seaborn, statsmodels, scikit-learn, selenium, re, ast, <br />
**Requirements:**  ```pip install -r requirements.txt```  

## Files

### scraping/scraper.py

This Python script is used to scrape SimplyHired search results for "data science" job postings with a location set to "California." The output is a dataframe named raw_data.csv which is located in the scraping directory.

### data_cleaning/data_cleaning.py

This Python script cleans the raw_data.csv file. The output of this file are two sets of dataframes. The first set are for EDA without imputation and the second set are for an OLS analysis where the data has been imputed. The first set includes df_benefits.csv, df_qualifications.csv, and df_title_loc_comp_salary.csv, and the second set includes df_modeling.csv, df_modeling_drop_first.csv, and dropped_columns.csv. All dataframes are located in the data_cleaning directory.

### EDA.ipynb

This Jupyter Notebook file contains the exploratory data analysis of the cleaned data (without imputation) and the OLS analysis (of the imputed data).

## Data Collection

The data was collected on December 17, 2021. The postings were from Aug 17, 2021 and Dec 17, 2021. The total number of postings collected was 1342. The number of pages was limited to 99 which corresponds to 1342 postings.

## Data Cleaning

The following changes were made to the scraped data prior to imputation:
* job titles were broken into a "Levels" column (which included experience levels such as "Jr." and "Sr.") and a "Title" column (which included titles such as "Data Scientist" and "Data Analyst"),
* company ratings were removed from the company names,
* job postings which were not specific to California were removed,
* job postings which did not specify a city were assigned an NaN for Location,
* text and symbols were removed from salaries, a single digit salary was calculated where ranges were given, and hourly salaries were converted to annual, and
* benefits and qualifications were seperated from each other, and two binary matrices were created with each column corresponding to a different benefit or qualification.

The non-imputed cleaned dataframes were then exported for EDA.

The following changes were made to the non-imputed dataframes for the OLS analysis:
* missing company, location, and qualifications were imputed using SimpleImputer set to "most_frequent", and
* missing salary was imputed using KNNImputer where the optimal parameters were determined using the non-missing data and KNeighborsRegressor.

## EDA

Below are selected figures from EDA.ipynb:

<div align="center">
<figure>
<img src="images/salary-distribution.jpg"><br/>
  <figcaption>Figure 1: Boxplots for salaries by job title sorted by median in descending order.</figcaption>
</figure>
</div>

</br>
</br>

<div align="center">
<figure>
<img src="images/OLS-results.jpg"><br/>
  <figcaption>Figure 2: Statistically significant predictors from ordinary least squares analysis and their impact on salary.</figcaption>
</figure>
</div>

## Conclusion

## Resources

1. Inspiration: [PlayingNumbers/ds_salary_proj](https://github.com/PlayingNumbers/ds_salary_proj)
2. Data visualizations: Show Me the Numbers (Second Edition) by Stephen Few
3. OLS and multiple testing: An Introduction to Statistical Learning (Second Edition) by Gareth James, Daniela Witten, Trevor Hastie, and Rob Tibshirani
4. Chi-square test diagram: [isixsigma.com](https://www.isixsigma.com/dictionary/chi-square-test/)
