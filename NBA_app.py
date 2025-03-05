import pandas as pd
import streamlit as st
import plotly.express as px
import lxml

st.title('NBA Player Stats For this Decade So Far (2020-2024)')

st.sidebar.header('User Input Features')
st.sidebar.write('Select the Year, Team, and Position of the Players you want to see stats for.')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2021,2025))))

# Function to load individual season data
@st.cache_data
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    df = df.drop(df[df.Age == 'Age'].index)  # Remove duplicate headers
    df = df.fillna(0)  # Replace NaN values with 0
    df['Year'] = year  # Add a Year column
    playerstats = df.drop(['Rk', 'GS', 'MP', 'Awards', 'PF', '2P', '2PA', 'FT', 'FTA', 'eFG%'], axis=1) # Drop unnecessary columns
    return playerstats

playerstats = load_data(selected_year)

# Convert all values in the 'Team' column to strings
playerstats['Team'] = playerstats['Team'].astype(str)

# Team selection
sorted_unique_team = sorted(playerstats.Team.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Unique positions
unique_pos = ['PG', 'SG', 'SF', 'PF', 'C']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filter data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats')
st.write('Click on Column Headers to Sort Data')
st.dataframe(df_selected_team)


# Load data of NBA players' average stats
# Read the average_stat.csv file
average_stats_path = 'notebooks/average_stats.csv'
average_stats = pd.read_csv(average_stats_path)

# Button to show average stats
st.write('Click the button below to show the averages of the NBA players.')
show_avg_stats = st.button('Show the averages of the NBA players')
if show_avg_stats:
    st.dataframe(average_stats)

st.header('Data Visualization')
st.write('Click the checkboxes below to show the visualizations.')

if st.checkbox('Histogram of Points Per Game'):
    # Histogram of Points Per Game (PTS)
    st.header('Distribution of Points Per Game')
    st.write('Hover over the bars to see the number of players in each bin.')
    fig1 = px.histogram(average_stats, x='PTS', nbins=20, 
                        title='Distribution of Points Per Game (PTS)',
                        labels={'PTS': 'Points Per Game'},
                        opacity=0.8, color_discrete_sequence=['blue'])
    st.plotly_chart(fig1)
    st.write('The histogram "Distribution of Points Per Game (PTS)" shows how spread out the entire NBA averages Points Per Game. It is skewed to the right as there are less players who score 15 or more than the mean which is about 5 PTS.')

# Top 15 players with the highest average points per game
top15_scorers = average_stats[average_stats.PTS == average_stats.PTS].sort_values(by='PTS', ascending=True).tail(15)  

if st.checkbox('Bar Chart: Top 15 Scorers'):
    st.header('Top 15 Players with the Highest Points Per Game')
    st.write('Hover over the bars to see the Points Per Game of each player.')
    # Horizontal bar chart of the top 15 players with the highest points per game
    fig2 = px.bar(top15_scorers, x='PTS', y='Player', 
                  title='Top 15 Players with the Highest Points Per Game',
                  labels={'PTS': 'Points Per Game', 'Player': 'Player Name'},
                  color='PTS', orientation='h')
    st.plotly_chart(fig2)

if st.checkbox('Scatterplot of Efficiency'):
    st.header('Efficiency of Top 15 Scorers')
    st.write('Hover over the points to see the Player Name, Points Per Game, and Field Goal Percentage.')
    # Scatter plot of Points Per Game vs. Field Goal Percentage of Top 15 Scorers
    fig3 = px.scatter(top15_scorers, x='PTS', y='FG%', 
                      title='Points Per Game vs. Field Goal Percentage',
                      labels={'PTS': 'Points Per Game', 'FG%': 'Field Goal Percentage'},
                      size='PTS', hover_name='Player')
    st.plotly_chart(fig3)
    st.write('The scatterplot shows the Points vs. Field Goal Percentage, to show the efficiency of the top 30 scorers. Although, Joel Embiid is the top scorer, he is not the most efficient. The most efficient scorers are Zion Williamson scoring 25.3 PTS on 59.6% of shooting, Nikola Jokic scoring 26.1 PTS on 59.1% of shooting, and then Giannis Antetokounmpo scoring 29.9 PTS on 57.2% of shooting.')


# Top 15 rebounders with the highest average rebounds per game
top15_rebounders = average_stats[average_stats.REB == average_stats.REB].sort_values(by='REB', ascending=False).head(15)

if st.checkbox('Scatterplot of Rebounds'):
    st.header('Rebounds of Top 15 Rebounders')
    st.write('Hover over the points to see the Player Name, Defensive Rebounds, Offensive Rebounds, and Total Rebounds.')
    # Scatter plot of Defensive Rebounds vs. Offensive Rebounds of Top 15 Rebounders
    fig4 = px.scatter(top15_rebounders, x='DRB', y='ORB', 
                      title='Defensive Rebounds vs. Offensive Rebounds',
                      labels={'DRB': 'Defensive Rebounds', 'ORB': 'Offensive Rebounds'},
                      size='REB', hover_name='Player')
    st.plotly_chart(fig4)
    st.write('Above shows the top rebounders in the league, but with the amount of rebounds on either the offensive or defensive side. Rudy Gobert is the top rebounder, but is about 3:1 ratio of defensive to offensive rebounds, which means most of his rebounds come from the defensive side of the floor. The top offensive rebounder is Steven Adams with about 4.5 rebounds, but is ranked number 14 in total rebounds.')


# Top 30 players with the highest 3P% while attempting more than 5 threes a game.
top30_3pt = average_stats[average_stats['3PA'] > 5].sort_values(by='3P%', ascending=False).head(30)

if st.checkbox('Scatterplot of 3P%'):
    st.header('Top 30 Most Efficient 3-Point Shooters')
    st.write('Hover over the points to see the Player Name, 3-Point Attempts Per Game, and 3-Point Percentage.')
    fig5 = px.scatter(top30_3pt, x='3PA', y='3P%', 
                      title='3PT Attempts vs. 3PT Percentage (Shooting More Than 5 3PTs Per Game)',
                      labels={'3PA': '3-Point Attempts Per Game', '3P%': '3-Point Percentage'},
                      size='3PA', hover_name='Player')
    st.plotly_chart(fig5)
    st.wrtie('This shows the effiency of the top 30 three point shooters (in three point field percentages shooting more than 5 threes a game). There seems to be an outlier of this group, it being Stephen Curry with his attempts. He attempts about 11.9 threes a game, but shooting 40.9% from three. While the player who tends to make his threes more often, is Kevin Durant with 42.7% from three, but only shooting about 5.2 threes a game.')


# Top 15 players with the highest average assists per game
top15_playmakers = average_stats[average_stats.AST == average_stats.AST].sort_values(by='AST', ascending=False).head(15)

if st.checkbox('Scatterplot of Assists'):
    st.header('Assists of Top 15 Playmakers')
    st.write('Hover over the points to see the Player Name, Assists Per Game, and Turnovers Per Game.')
    fig6 = px.scatter(top15_playmakers, x='AST', y='TOV', 
                      title='Assists vs. Turnovers (Playmaking Efficiency)',
                      labels={'AST': 'Assists Per Game', 'TOV': 'Turnovers Per Game'},
                      color='Pos', size='AST', hover_name='Player')
    st.plotly_chart(fig6)
    st.write('This shows the assist vs. turnovers, meaning how efficient of a playmaker is. The less of turnovers is the better, but with the increase amount of assists tends to be more turnovers. Typically, the ratio to aim for in assists to turnover is 2:1. Anything less, would usually mean the player is not an elite playmaker, or the designated playmaker for their team. The player with best assist to turnover ratio is Chris Paul with about a 4:1 ratio.')

# Source
st.write('Data Source: [Basketball Reference](https://www.basketball-reference.com/)')