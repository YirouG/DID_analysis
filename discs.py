#Yirou Guo
#The code first cleans the data by removing unnecessary columns and replacing spaces in column names. It then performs a series of analyses on the data, including finding the most popular tracks, books, and luxury items chosen by guests, as well as comparing the choices of returning guests. The code also uses the gender_guesser library to guess the gender of each guest based on their first name and explore the gender differences in guests’ choices. Overall, this project provides insights into the preferences of Desert Island Discs guests and how they have changed over time.
#Non-standard modules: pandas, matplotlib, gender_guesser_detector

import pandas as pd
import matplotlib.pyplot as plt
from gender_guesser.detector import Detector


#Most favourited among all guests:
def most_favourited(column):

    return df[column].value_counts().head(10)

#Define a function that guesses the gender of a guest from their first name
def guess_gender(name):
    return d.get_gender(name)


#compare the choices in returning guests' multiple broadcasts and return the changes
def return_changes(re_guest_choices,column,changes):

    re_guest_choices.sort_values(['Castaway','Date_first_broadcast'],inplace=True)
    re_guest_choices[changes]=re_guest_choices.groupby('Castaway').apply(lambda group:group[column].ne(group[column].shift(1)).where(group[column].notnull())).tolist()
    re_guest_choices[changes] = re_guest_choices[changes].map({True: 1, False: 0})
    return re_guest_choices

    # Sort df to original df
    re_guest_choices = re_guest_choices.sort_index()

    # Change the first in each group to 0
    re_guest_choices.loc[re_guest_choices.groupby('Castaway').head(1).index, changes] = 0
    return re_guest_choices






print("""Welcome to the Desert Island Discs Data Analysis Project""")
print("(This is Yirou speaking)\n")


#-------------------------------------------
#Data cleaning

#load and clean empty columns
df = pd.read_csv('episodes.csv')
df.drop(df.columns[df.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)

#replace spaces in column names because they are evil
df.columns=df.columns.str.replace(" ","_")
#drop columns I don't need and set date to datetime
df=df.drop(['URL','Episode_title','Time_first_broadcast'],axis=1)
df.Date_first_broadcast=pd.to_datetime(df.Date_first_broadcast)
#Show all columns
pd.options.display.max_columns = None



#-------------------------------------------
##Data analysis:


#===========================================
#All guests:

#Most favourited tracks:

print("The top favourite tracks chosen by guests over the years are:")
print(most_favourited('Favourite_track'))
favourited_tracks=most_favourited('Favourite_track')
favourited_tracks.plot(x=favourited_tracks.loc(0),y="index")


#Most frequently chosen tracks:

df1=pd.DataFrame(df[["Song_1", "Song_2",'Song_3','Song_4',"Song_5",'Song_6','Song_7','Song_8']])
df1 = pd.DataFrame(df1.melt(var_name='columns', value_name='index'))
print("\nThe top most commonly chosen tracks within the 8 discs selected by guests over the years are:")
common_tracks=df1["index"].value_counts().head(10)
print(common_tracks)
# common_tracks.plot(x=common_tracks.loc(0),y="index")
# plt.show()

#Most frequently chosen artists:

artists=pd.DataFrame(df[["Artist_1", "Artist_2",'Artist_3','Artist_4',"Artist_5",'Artist_6','Artist_7','Artist_8']])
artists = pd.DataFrame(artists.melt(var_name='columns', value_name='index'))
print("\nThe top artists chosen by all guests are:")
common_artists=artists["index"].value_counts().head(10)
print(common_artists)


#Most chosen books:

print("\nThe top favourite books chosen by guests over the years are:")
print(most_favourited('Book'))

#Most chosen luxuries:

print("\nThe top favourite luxuries chosen by guests over the years are:")
print(most_favourited('Luxury'))


#===========================================
#Is there a gender difference in music tastes?

# Create a Gender object
d = Detector()

# Use the apply method to guess the gender of each name
df['gender'] = df['Castaway'].str.split(' ').str[0].apply(d.get_gender)

#Sorry for the gender binarism, I could not find a better module right now, also I'm guessing a lot of non-Christian names are detected as 'unknown'.
print("\nThe top 10 favourite tracks chosen by females and males are: ")
overly_simpified_gender = df['gender'].str.contains('andy')| df['gender'].str.contains('mostly')| df['gender'].str.contains('unknown')
df = df[~overly_simpified_gender]


#Top 10 favs by female and male

gendered_fav=df.groupby('gender')['Favourite_track'].value_counts().groupby(level=0).nlargest(10)
print(gendered_fav)


#===========================================
#Returning guests:


#Generate a dataframe of guests who joins the broadcast more than once
#df=df.loc[:,['Castaway','Date_first_broadcast', 'Book','Luxury','Favourite_track']]
df2=df.sort_values(['Castaway','Date_first_broadcast'],ascending=[False,False])
appearance_count=pd.DataFrame(df2.Castaway.value_counts().reset_index().values, columns=['Castaway', 'appearances'])
returning_guest=appearance_count.loc[appearance_count.appearances>1]
print("In all 3339 episodes archived so far, 172 guests has joined to the program more than once. The returning rate is 0.05.")
print(returning_guest)
re_guest_choices= pd.merge(df,returning_guest , on='Castaway')
#print(re_guest_choices)

#average times of re-appearance
re_guest_choices.appearances=re_guest_choices.appearances.apply(pd.to_numeric)
print("On average, returning guests would show up "+re_guest_choices.appearances.mean().round().astype(int).astype(str)+" times")

#after how long do they return?
re_guest_choices['Diff_time'] = re_guest_choices.groupby('Castaway')['Date_first_broadcast'].diff()
days=-re_guest_choices['Diff_time'].mean()
years = str(round((days.days / 365)))
print("On average, guests return "+years+" years after their first appearance in desert island discs.")


#How did the tastes of returning guests change?

print('\nSome guests who joined the program in the earlier days for the first time did not choose their favourite tracks, comparing the returning guests who left a record of choosing their favourite tracks for multiple times, almost all of them changed their minds, with only 4 guests sticking to their old favourites. ')
re_guest_choices=return_changes(re_guest_choices,'Favourite_track','fav_change')
print(re_guest_choices['fav_change'].value_counts())




