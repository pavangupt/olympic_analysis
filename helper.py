# from jupyterfile, we addressed the wrong medal achiever issues by dropping duplicates from certain column
import numpy as np

import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def most_succesfull(df, sport):
    tempo_df = df.dropna(subset=['Medal'])
    if sport != "Overall":
        tempo_df = tempo_df[tempo_df['Sport'] == sport]
    x = tempo_df[['Name', 'Sport', 'Medal', 'region']].value_counts().reset_index().drop_duplicates()
    x.rename(columns={'Name': 'Player', 0: 'Medal_Count'}, inplace=True)
    return x


def yearwise_medal(df, region_name):
    tem_df = df.dropna(subset=['Medal'])
    tem_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == region_name]
    fina_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return fina_df


def country_heatmap(df, country):
    tem_df = df.dropna(subset=['Medal'])
    tem_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = tem_df[tem_df['region'] == country]
    new_df = new_df.pivot_table(index="Sport", columns='Year', values='Medal', aggfunc='count').fillna(0).astype("int")
    return new_df


def mostsuccesfull_countrywise(df, country):
    tempo_df = df.dropna(subset=['Medal'])
    tempo_df = tempo_df[tempo_df['region'] == country]

    x = tempo_df[['Name', 'Sport', 'Medal']].value_counts().reset_index().drop_duplicates()
    x.rename(columns={'Name': 'Player', 0: 'Medal_Count'}, inplace=True)
    return x.head(10)


def weight_v_height(df, sport):
    df_tt = df.drop_duplicates(subset=['Name', 'region'])
    df_tt['Medal'].fillna('No Medal', inplace=True)
    if sport!= 'Overall':
        temp_df = df_tt[df_tt["Sport"] == sport]
        return temp_df
    else:
        return df_tt


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
    
