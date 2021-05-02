import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.widgets import Cursor
import random
import array

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


def init_annotate():
    """
    Initialize annotate to use matplotlib
    """
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
    """
    Annotation update  when hover mouse
    """
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
    """
    Event tracking on mouse hover. This function will be triggered when there is a mouse cursor in any area.
    """
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


def generate_password():
    """
    Generate password according to properties given  in Q1
    """
    numbers = ['0', '1', '2', '3', '4', '5'] 
    chars = ["A", "B", "C", "D", "E"]
    temp_passs = ""
    temp_pass = ""

    for i in range(4):
        rand_num = random.choice(numbers)
        temp_pass += temp_pass.join(rand_num)
        # rand_chars = random.choice(chars)
    for i in range(4):
        rand_chars = random.choice(chars)
        temp_passs += temp_passs.join(rand_chars)
    return(temp_pass + "-" + temp_passs)


def duplicated(list):
    """
    Get duplicate values in list

    Args:
        list (list): The given list

    Returns:
        list: Duplicate values
    """
    u, c = np.unique(list, return_counts=True)
    dup = u[c > 1]
    return dup


def sum(dup):
    return len(dup)


def unique_passwords(websites):
    """
    Generate password for each one website
    
    Args:
        websites (list): Websites list
    Returns:
        DataFrame: DataFrame contains website and It's password
    """
    temp_df = pd.DataFrame()
    password_list = []

    for website in websites:
        password = generate_password()
        while password in password_list:
            password = generate_password()
        password_list.append(password)
        data = {"Website":website, "Password":password}
        temp_df = temp_df.append(data, ignore_index=True)
    return temp_df


def create_genre_group_val(row):
    """
    Create genre group for dataframe according to 'genre' value

    Args:
        row (pandas.core.series.Series): Row of the dataframe

    Returns:
        [str]: genre group value
    """
    if 'pop' in row['genre']:
        return 'pop'
    elif 'hip hop' in row['genre']:
        return 'hip hop'
    else:
        return 'other genre'


def Q1():
    print("\n====================================================================")
    print("[Q1] Rastgele şifre oluşturma".upper())
    print("====================================================================\n")
    print(generate_password())
    print("\n====================================================================\n")


def Q2():
    print("\n====================================================================")
    print("[Q2] Çoğaltılmış şifre sayısı".upper())
    print("====================================================================\n")

    pass_list = [generate_password() for _ in range(10000)]
    print(sum(duplicated(pass_list)))
    print("\n====================================================================\n")


def Q3():
    print("\n====================================================================")
    print("[Q3] Web site ve şifresini oluşturma".upper())
    print("====================================================================\n")
    website_list = []

    [website_list.append("Website_" + str(i)) for i in range(10000)]
    passwords10000df = unique_passwords(website_list)
    print(sum(duplicated(passwords10000df['Password'])))


def Q4():
    print("\n====================================================================")
    print("[Q4] Herbir türde kaç şarkı var?".upper())
    print("====================================================================\n")
    global df
    res = df.groupby('genre')['genre'].count().reset_index(name='count').sort_values(['count'], ascending=False).head(5)
    print(res)


def Q5():
    print("\n====================================================================")
    print("[Q5] En populer sanatçılar".upper())
    print("====================================================================\n")
    f = {'pop': 'mean', 'year':'count'}
    comp = df.groupby(['artist', 'year'], as_index=False).agg(f)
    comp = comp[comp['year'] >= 3]
    comp = comp[comp['pop'] > 75]
    res = comp.sort_values('pop', ascending=False)
    res.rename(columns={'pop':'mean_popularity', 'year':'number_of_song'}, inplace=True)
    print(res)


def Q6():
    print("\n====================================================================")
    print("[Q6] 2018-2019 en iyi 5 tür".upper())
    print("====================================================================\n")
    global found_genres
    mask = (df['year'] > 2017) & (df['year'] <= 2019)
    found_genres = df.loc[mask]['genre'].drop_duplicates()
    print(found_genres.head(5))


def Q7():
    print("\n====================================================================")
    print("[Q7] 'genre' Enerji Ortalaması Tablosu".upper())
    print("====================================================================\n")
    global found_genres
    fig1 = plt.figure(1)
    dd = df.loc[df['genre'].isin(found_genres)]
    dd = dd.loc[(dd['year'] > 2017) & (dd['year'] <= 2019)]
    engry_mean = dd.groupby('genre')['nrgy'].mean()
    engry_mean.plot.bar(title="2018-2019 Genre Energy Mean")


def Q8():
    print("\n====================================================================")
    print("[Q8] 'genre_group' oluştur".upper())
    print("====================================================================\n")
    from matplotlib.lines import Line2D
    init_annotate()
    global ax
    global fig
    global sc
    global names

    fig2 = plt.figure(2)
    new_df = df

    values = ['hip hop', 'other genre', 'pop']
    new_df['genre_group'] = new_df.apply(create_genre_group_val, axis=1)

    print(new_df.head(5))
    
    # print(len(new_df[new_df['genre_group'] == 'pop']))
    # print(len(new_df[new_df['genre_group'] == 'hip hop']))
    # print(len(new_df[new_df['genre_group'] == 'other genre']))

    red = '#F08080'
    green = '#90ee90'
    blue = '#47a2fb'
    colors = {'hip hop':red, 'other genre': green, 'pop': blue}
    # labels, index = np.unique(df["genre_group"], return_inverse=True)

    ax.set_title('Danceability vs Popularity by Genre Group', loc='left')
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


Q1()
Q2()
Q3()
Q4()
Q5()
Q6()
Q7()
Q8()
plt.show()
