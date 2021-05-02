import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.widgets import Cursor
import seaborn as sns

df = pd.read_csv("top10s.csv")
found_genres = None
coord = []
annot = None
fig = None
ax = None
sc = None

norm = plt.Normalize(1, 4)
cmap = plt.cm.RdYlGn

names = []


def init():
    global fig
    global ax
    global annot
    fig, ax = plt.subplots()

    # Defining the cursor
    cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                    color='r', linewidth=1)

    # Creating an annotating box
    annot = ax.annotate("", xy=(0, 0), xytext=(-40, 40), textcoords="offset points",
                        bbox=dict(boxstyle='round4', fc='linen', ec='k', lw=1),
                        arrowprops=dict(arrowstyle='-|>'))
    annot.set_visible(False)


def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    # data = [str(names[n]) for n in ind["ind"]]
    for n in ind["ind"]:
        data = names[n]
    text = "dnce: " + data['dnce'] + "\npop: " + data['pop'] + "\ngenre_group: " + data['genre_group'] + "\n" + data['artist'] + "\n" + data['title'] + "\n" + data['year'] + "\n"
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor('#47a2fb')
    # annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    global coord
    global fig
    global annot
    vis = annot.get_visible()

    if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()


def Q4():
    global df
    res = df.groupby('genre')['genre'].count().reset_index(name='count').sort_values(['count'], ascending=False).head(5)
    print(res)


def Q5():
    f = {'pop': 'mean', 'year':'count'}
    comp = df.groupby(['artist', 'year'], as_index=False).agg(f)
    comp = comp[comp['year'] >= 3]
    comp = comp[comp['pop'] > 75]
    res = comp.sort_values('pop', ascending=False)
    print(res)


def Q6():
    global found_genres
    mask = (df['year'] > 2017) & (df['year'] <= 2019)
    found_genres = df.loc[mask]['genre'].drop_duplicates()
    print(found_genres)


def Q7():
    global found_genres
    fig1 = plt.figure(1)
    dd = df.loc[df['genre'].isin(found_genres)]
    dd = dd.loc[(dd['year'] > 2017) & (dd['year'] <= 2019)]
    engry_mean = dd.groupby('genre')['nrgy'].mean()
    engry_mean.plot.bar(title="2018-2019 Genre Energy Mean")


def Q8():
    from matplotlib.lines import Line2D
    init()
    global ax
    global fig
    global sc
    global names

    fig2 = plt.figure(2)
    new_df = df
    conditions = [
        (new_df['genre'] == 'pop'),
        (new_df['genre'] == 'hip hop'),
        (new_df['genre'] != 'pop') | (new_df['genre'] != 'hip hop')
    ]

    values = ['hip hop', 'other genre', 'pop']
    new_df['genre_group'] = np.select(conditions, values)
    
    print(len(new_df[new_df['genre_group'] == 'pop']))
    print(len(new_df[new_df['genre_group'] == 'hip hop']))
    print(len(new_df[new_df['genre_group'] == 'other genre']))

    red = '#F08080'
    green = '#90ee90'
    blue = '#47a2fb'
    colors = {'hip hop':red, 'other genre': green, 'pop': blue}
    labels, index = np.unique(df["genre_group"], return_inverse=True)

    sc = ax.scatter(new_df['dnce'], new_df['pop'], marker='.', c=[colors[r] for r in new_df['genre_group']])
    custom_lines = [Line2D([0], [0], color=red, lw=4),
                Line2D([0], [0], color=green, lw=4),
                Line2D([0], [0], color=blue, lw=4)]   
    ax.legend(custom_lines, values)
    
    for index, row in new_df.iterrows():
        d = {"dnce":str(row['dnce']), "pop":str(row['pop']), 'genre_group':row['genre_group'], 'artist':row['artist'], 'title':row['title'], 'year':str(row['year'])}
        names.append(d)

    # for key,group in df.groupby('genre_group'):
    #     group.plot(ax=ax, kind='scatter', x='dnce', y='pop', marker = 'o', label=key, color=colors[key])

    # sns.scatterplot(x="dnce", y="pop", data=new_df, hue="genre_group")

    fig.canvas.mpl_connect('motion_notify_event', hover)


Q4()
Q5()
Q6()
Q7()
Q8()
plt.show()
