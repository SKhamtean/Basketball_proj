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

if st.checkbox('Histogram of Points Per Game'):
    # Histogram of Points Per Game (PTS)
    st.header('Distribution of Points Per Game')
    fig1 = px.histogram(average_stats, x='PTS', nbins=20, 
                        title='Distribution of Points Per Game (PTS)',
                        labels={'PTS': 'Points Per Game'},
                        opacity=0.8, color_discrete_sequence=['blue'])
    st.plotly_chart(fig1)

# Top 15 players with the highest average points per game
top15_scorers = average_stats[average_stats.PTS == average_stats.PTS].sort_values(by='PTS', ascending=True).tail(15)  

if st.checkbox('Bar Chart: Top 15 Scorers'):
    st.header('Top 15 Players with the Highest Points Per Game')
    # Horizontal bar chart of the top 15 players with the highest points per game
    fig2 = px.bar(top15_scorers, x='PTS', y='Player', 
                  title='Top 15 Players with the Highest Points Per Game',
                  labels={'PTS': 'Points Per Game', 'Player': 'Player Name'},
                  color='PTS', orientation='h')
    st.plotly_chart(fig2)

if st.checkbox('Scatterplot of Efficiency'):
    st.header('Efficiency of Top 15 Scorers')
    # Scatter plot of Points Per Game vs. Field Goal Percentage of Top 15 Scorers
    fig3 = px.scatter(top15_scorers, x='PTS', y='FG%', 
                      title='Points Per Game vs. Field Goal Percentage',
                      labels={'PTS': 'Points Per Game', 'FG%': 'Field Goal Percentage'},
                      size='PTS', hover_name='Player')
    st.plotly_chart(fig3)


# Top 15 rebounders with the highest average rebounds per game
top15_rebounders = average_stats[average_stats.REB == average_stats.REB].sort_values(by='REB', ascending=False).head(15)

if st.checkbox('Scatterplot of Rebounds'):
    st.header('Rebounds of Top 15 Rebounders')
    # Scatter plot of Defensive Rebounds vs. Offensive Rebounds of Top 15 Rebounders
    fig4 = px.scatter(top15_rebounders, x='DRB', y='ORB', 
                      title='Defensive Rebounds vs. Offensive Rebounds',
                      labels={'DRB': 'Defensive Rebounds', 'ORB': 'Offensive Rebounds'},
                      size='REB', hover_name='Player')
    st.plotly_chart(fig4)


# Top 30 players with the highest 3P% while attempting more than 5 threes a game.
top30_3pt = average_stats[average_stats['3PA'] > 5].sort_values(by='3P%', ascending=False).head(30)

if st.checkbox('Scatterplot of 3P%'):
    st.header('Top 30 Most Efficient 3-Point Shooters')
    fig5 = px.scatter(top30_3pt, x='3PA', y='3P%', 
                      title='3PT Attempts vs. 3PT Percentage (Shooting More Than 5 3PTs Per Game)',
                      labels={'3PA': '3-Point Attempts Per Game', '3P%': '3-Point Percentage'},
                      size='3PA', hover_name='Player')
    st.plotly_chart(fig5)


# Top 15 players with the highest average assists per game
top15_playmakers = average_stats[average_stats.AST == average_stats.AST].sort_values(by='AST', ascending=False).head(15)

if st.checkbox('Scatterplot of Assists'):
    st.header('Assists of Top 15 Playmakers')
    fig6 = px.scatter(top15_playmakers, x='AST', y='TOV', 
                      title='Assists vs. Turnovers (Playmaking Efficiency)',
                      labels={'AST': 'Assists Per Game', 'TOV': 'Turnovers Per Game'},
                      color='Pos', size='AST', hover_name='Player')
    st.plotly_chart(fig6)