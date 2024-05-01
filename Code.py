import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# Data Collection and Preparation
stats = pd.read_excel("data.xlsx")
stats.head()
stats.info()
stats.describe()
stats.isna().sum()

# Data Transformation and Analysis
stats['Mins Per Match'] = (stats['Mins'] / stats['Matches']).astype(int)
stats['Goals Per Match'] = round((stats['Goals'] / stats['Matches']).astype(float),2)
stats

# Penalty plot
print("Total Goals Scored in EPL 2020/21 is:", stats['Goals'].sum())
print("Total Penalty Goals Scored in EPL 2020/21 is:", stats['Penalty_Goals'].sum())
print("Total Penalty Attempts in EPL 2020/21 is:", stats['Penalty_Attempted'].sum())

plt.figure(figsize=(3,5))
penalties_missed = stats['Penalty_Attempted'].sum() - stats['Penalty_Goals'].sum()
penalties_scored = stats['Penalty_Goals'].sum()
data = [penalties_missed,penalties_scored]
label = ['Missed Penalties','Scored Penalties']
color = sns.color_palette('tab10')
plt.pie(data, labels=label, colors=color, autopct='%.1f%%')
plt.title('Penalty Distribution Plot')
plt.show()

# Unique positions
pd.DataFrame(stats['Position'].unique())

# 'FW' players
stats[stats['Position'] == 'FW']

# Number of nationalities
print("Different nations players are from: ",np.size(stats['Nationality'].unique()))

nations = stats.groupby('Nationality').size().sort_values(ascending=False)
nations.head(10).plot(kind='bar', figsize=(7,5), color=sns.color_palette('viridis'))
plt.title('Player Nationality Representation\n')
plt.ylabel('Number of players')

# Clubs with maximum players in squad
stats['Club'].value_counts().nlargest(5).plot(kind='bar', figsize=(7,5), color=sns.color_palette('magma'))
plt.title('Clubs with maximum number of players in squad\n')
plt.ylabel('Number of players')

# Clubs with minimum players in squad
stats['Club'].value_counts().nsmallest(5).plot(kind='bar', figsize=(7,5), color=sns.color_palette('mako'))
plt.title('Clubs with minimum number of players in squad\n')
plt.ylabel('Number of players')

# Players' age distribution
U_20 = stats[stats['Age'] < 20]
A_20_25 = stats[(stats['Age'] >= 20) & (stats['Age'] < 25)]
A_25_30 = stats[(stats['Age'] >= 25) & (stats['Age'] <= 30)]
A_30 = stats[stats['Age'] > 30]

plt.figure(figsize=(3,5))
data = np.array([U_20['Age'].count(),A_20_25['Age'].count(),A_25_30['Age'].count(),A_30['Age'].count()])
label = ['Under 20','Between 20 and 25','Between 25 and 30','Above 30']
color = sns.color_palette('husl')
plt.title("Players' Age Distribution\n")
plt.pie(data, labels=label, colors=color, autopct="%.1f%%")
plt.show()

# Number of U-20 players in each club
data = stats[stats['Age'] < 20]
data['Club'].value_counts().plot(kind='bar', figsize=(7,5), color=sns.color_palette('hls'))
plt.title('U-20 Player distribution by club\n')
plt.ylabel('Number of players')

# List of U-20 players in each club
data = stats[stats['Age'] < 20].sort_values(by='Club')
print("Total number of U-20 players in league:",len(data))
print("Total number of clubs with atleast one U-20 player:",np.size(data['Club'].unique()),"\n")

for i in data['Club'].unique():
    print(i,":",sep="")
    for j in data[data['Club']==i]['Name'].tolist():
        print(j)
    print("\n")

# Average age of players in each club
data = stats.groupby('Club')['Age'].mean()
data.plot(kind='bar', figsize=(7,5), color=sns.color_palette('crest'))
plt.title('Average player age by club\n')
plt.ylabel('Number of players')

plt.figure(figsize=(7,5))
sns.boxplot(x='Club', y='Age', data=stats.sort_values('Club'))
plt.xticks(rotation=90)
plt.title('Player age distribution (Box Plot)\n')

data = (stats.groupby('Club')['Age'].sum()/stats.groupby('Club').size())
data.sort_values(ascending=False)

# Total number of assists from each club
assists_by_club = pd.DataFrame(stats.groupby('Club', as_index=False)['Assists'].sum())
sns.set_theme(style='whitegrid', color_codes=True)
ax = sns.barplot(x='Club', y='Assists', data=assists_by_club.sort_values(by='Assists'), palette='Set2')
ax.set_xlabel('Club', fontsize=15)
ax.set_ylabel('Assists', fontsize=15)
plt.xticks(rotation=90)
plt.rcParams['figure.figsize'] = (20,8)
plt.title("Clubs vs Total Assists\n", fontsize=15)

# Top 10 Assisters
top_10_assists = stats[['Name','Club','Assists','Matches']].nlargest(n=10, columns='Assists')
top_10_assists

# Total number of goals from each club
goals_by_club = pd.DataFrame(stats.groupby('Club', as_index=False)['Goals'].sum())
sns.set_theme(style='whitegrid', color_codes=True)
ax = sns.barplot(x='Club', y='Goals', data=goals_by_club.sort_values(by='Goals'), palette='rocket')
ax.set_xlabel('Club', fontsize=15)
ax.set_ylabel('Goals', fontsize=15)
plt.xticks(rotation=75)
plt.rcParams['figure.figsize'] = (20,8)
plt.title("Clubs vs Total Goals\n", fontsize=15)

# Top 10 Goalscorers
top_10_goals = stats[['Name','Club','Goals','Matches']].nlargest(n=10, columns='Goals')
top_10_goals

# Goals per match
top_10_goals_per_match = stats[['Name','Goals Per Match','Matches','Goals']].nlargest(n=10, columns='Goals Per Match')
top_10_goals_per_match

# Goals with & without assists (Pie Chart)
plt.figure(figsize=(3,5))
goals = stats['Goals'].sum()
assists = stats['Assists'].sum()
data = [goals - assists, assists]
label = ['Goals without assist', 'Goals with assist']
color = sns.color_palette('Set1')
plt.pie(data, labels=label, colors=color, autopct="%.1f%%")
plt.title('Goals distribution with and without assists')
plt.show()

# Yellow cards data
yellow = stats.sort_values(by='Yellow_Cards', ascending=False)[:10]
plt.figure(figsize=(10,5))
plt.title("Players with most yellow cards\n")
text = yellow['Name'] + ' (' + yellow['Club'] + ')'
plot = sns.barplot(x=text, y=yellow['Yellow_Cards'], label='Players', color='Yellow')
plt.xlabel('Players (Clubs)')
plt.ylabel('Number of Yellow Cards')
plot.set_xticklabels(plot.get_xticklabels(), rotation=60)
plot
