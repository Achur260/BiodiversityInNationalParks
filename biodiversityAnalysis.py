
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import seaborn as sns
import scipy.stats as stats

# What is the distribution of conservation_status for animals?
# Are certain types of species more likely to be endangered?
# Are the differences between species and their conservation status significant?
# Which species were spotted the most at each park?

observations = pd.read_csv('observations.csv')
species = pd.read_csv('species_info.csv')

# species = species.drop_duplicates(subset=['scientific_name'])
print(species.describe())

# What is the distribution of conservation_status for animals?

print(species.conservation_status.dtype)
conservation = species.dropna(subset=['conservation_status'])
conservation = conservation.drop_duplicates(subset=['scientific_name'])
plt.hist(conservation['conservation_status'])
plt.title("Conservation Status")
plt.xlabel("Conservation Status")
plt.ylabel("Frequency")
plt.show()
plt.clf()

prev = 0

plt.figure(figsize=(10,10))
colors = ['blue', 'red', 'green', 'yellow']
count=0
print(conservation.conservation_status.unique())
for status in conservation.conservation_status.unique():
    prop = pd.DataFrame()
    prop['category'] = conservation['category']
    prop['scientific_name'] = conservation['scientific_name']
    prop['proportion'] = prop.category.apply(lambda row: len(conservation[(conservation['category'] == row) & (conservation['conservation_status'] == status)]) / len(conservation[conservation['category'] == row]))
    thePlot = plt.bar(prop['category'], 100-prev,color=colors[count],label=status)
    prev += 100*prop['proportion']
    count += 1
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.xlabel("Category")
plt.ylabel("Percentage")
plt.title("Conservation Status Distribution (in percent) by Animal Category")
plt.show()
plt.clf()
# Are certain types of species more likely to be endangered?
endangered = pd.DataFrame()
s = species.drop_duplicates(subset=['scientific_name'])
endangered['category'] = conservation['category'].unique()
endangered['proportion'] = endangered.category.apply(lambda row: 100*len(conservation[(conservation['category'] == row)&(conservation['conservation_status']=='Endangered')]) / len(s[s['category'] == row]))
print(endangered)
figure = plt.figure(figsize = (10,10))
mplt = sns.barplot(data=endangered, x='category', y='proportion', hue='category')
plt.title("Percent of species in each Animal Category that are Endangered")
plt.xlabel("Category")
plt.ylabel("Percent Endangered")

mplt.set_xticklabels(mplt.get_xticklabels(), rotation=45)
plt.show()
plt.clf()

# Are the differences between species and their conservation status significant?

conservation = s


conservation=conservation.fillna("Inapplicable")
print(pd.crosstab(conservation['category'],conservation['conservation_status'])['Inapplicable'])
print(stats.chi2_contingency(pd.crosstab(conservation['category'],conservation['conservation_status']))[0:2])

# Which species were spotted the most at each park?

species = species.drop_duplicates(subset=['scientific_name'])

for park in observations.park_name.unique():
    plt.figure(figsize = (10,10))
    dx = plt.subplot(1, 1, 1)
    obs = observations[observations['park_name'] == park]
    parkObs = pd.merge(obs, species, on="scientific_name",how='inner')
    categoryCounts = pd.DataFrame()
    categoryCounts["category"] = parkObs['category'].unique()
    categoryCounts["count"] = categoryCounts['category'].apply(lambda x: parkObs[parkObs.category==x].observations.sum())
    categoryCounts["category"] = categoryCounts.category.apply(lambda x: "Vasc. Plant" if(x=="Vascular Plant") else x)
    categoryCounts["category"] = categoryCounts.category.apply(lambda x: "Nonvasc. Plant" if(x=="Nonvascular Plant") else x)

    seaborn.barplot(data=categoryCounts,x="category",y="count",hue="category")
    dx.set_xticklabels(dx.get_xticklabels(), rotation=45)
    plt.title("Observation Counts of each Animal Category at " + park)
    plt.xlabel("Category")
    if(park != "Yellowstone National Park"):
        plt.ylabel("Number of Observations")
    else:
        plt.ylabel("Number of Observations (in Millions)")
    plt.show()


