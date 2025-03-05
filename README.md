# Basketball_proj

## Basic Description
For this project in Sprint 4 for TripleTen, I was tasked to develop and deploy a web application to a cloud service so that it is accessible to the public. Originally was given a dataset on car sales advertisements, but I chose to look elsewhere as I was not interested in this certain topic. I chose to do NBA stats instead. I could have made a broad dataset of when the NBA first created to now, but I wanted a deeper dive into this generations best players. I chose to the dataset of 2020s decade, starts from the 2020-2021 season to 2023-2024 season. I am unable to add this season (2024-2025) as it is still currently going on. 

## Instructions
 1. Have Git downloaded
 2. Clone the repository in terminal:$ git clone https://github.com/SKhamtean/Basketball_proj.git
    - To get the url, there will be a green drop down button on the top right corner that says "<> Code"
    - Then copy the url that it presents.
 3. Then change directory to the repository name:$ cd Basketball_proj
 4. Install dependencies:$ pip install -r requirements.txt
 5. Setup Environment
 6. Have Streamlit installed:# install streamlit
 6. Then run application:$ streamlit run NBA_app.py
 7. Output should link to a URL that will host a webpage. 

## Explanation of what is simulated
When you run the NBA_app.py application through Render, it will display the title __"NBA Player Stats For this Decade So Far (2020-2024)"__. Below will be stats of the NBA players of a certain year of the user's choosing. How you choose a year will be off to the left side with a bar that says __"User Input Features"__. From there you can choose which year (2021-2024) to see the stats of the players. Along with the Year selectbox, we have two different multiselect options: Team and Position. With these, you can choose which team(s) and which position(s) you would like to display. Then, moving down from the main individual year player stats, there is a button that says __"Show the averages of the NBA players"__. If clicked, it will present the combined averages of each player from the season 2020-2021 to 2023-2024. To pair up with the averages, there are some data visuals with checkboxes below the button to show data of efficiency and who is the top players in their respective category. To view the the data visuals, click the corresponding checkboxes. 

## Libraries
 - pandas==2.2.3
 - streamlit==1.42.0
 - plotly==5.24.1
 - lxml==5.3.0

## Library Explanation
With the use of Streamlit, I was able build a web app. It helped me create some user interactives, which creates a more flowy and open environment. Also, with Pandas it helped me read the html url dataset from our source __Basketball-Reference__. Then with the help of Plotly.express, I created some data visuals, which works really well combined with some Streamlit interactives.

 ## Source
https://www.basketball-reference.com