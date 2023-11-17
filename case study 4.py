import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
import texttable as tt

url = 'https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/'

def scrap_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    data = []

    data_iterator = iter(soup.find_all('td'))

    while True:
        try:
            country = next(data_iterator).text
            confirmed = next(data_iterator).text.replace(',', '')  # Remove commas
            deaths = next(data_iterator).text.replace(',', '')  # Remove commas
            continent = next(data_iterator).text

            data.append((country, int(confirmed), int(deaths), continent))
        except StopIteration:
            break

    return data

data = scrap_data(url)

df = pd.DataFrame(data, columns=['country', 'Number of cases', 'Deaths', 'Continent'])

df.sort_values(by='Number of cases', ascending=False, inplace=True)

df['Death_rate'] = (df['Deaths'] / df['Number of cases']) * 100

rcParams['figure.figsize'] = 15, 10

# Pairplot
sns.pairplot(df, hue='Continent')

# Bar plot of number of cases by country
sns.barplot(x='country', y='Number of cases', data=df.head(10))

# Regression plot of deaths vs. number of cases
sns.regplot(x='Deaths', y='Number of cases', data=df)

# Scatterplot of number of cases vs. deaths, colored by continent
sns.scatterplot(x='Number of cases', y='Deaths', hue='Continent', data=df)

# Boxplot of deaths by country, colored by continent
sns.boxplot(x='country', y='Deaths', data=df.head(10), hue='Continent')

# Grouped data by continent
dfg = df.groupby(by='Continent', as_index=False).agg({'Number of cases': sum, 'Deaths': sum})

df1 = dfg.sort_values(by='Number of cases', ascending=False)

df1['Death_rate'] = (df1['Deaths'] / df1['Number of cases']) * 100

# Barplot of death rate by continent
sns.barplot(x='Continent', y='Death_rate', data=df1.sort_values(by='Death_rate', ascending=False))

# Print the data as a table
table = tt.Texttable()
table.add_rows([('Country', 'Number of cases', 'Deaths', 'Continent')] + data)
table.set_cols_align(('c', 'c', 'c', 'c'))
print(table.draw())
sns.pairplot(df, hue='Continent')
plt.show()
