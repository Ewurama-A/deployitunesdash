#import the necessary packages

from dash import Dash,html,dcc,Input,Output,callback,State

import plotly.express as px

import pandas as pd

#Reading the processed file

df = pd.read_csv(r"https://raw.githubusercontent.com/Ewurama-A/Data-Analysis/main/New_Itunes_data.csv")


# Calculating the mean prices, song size and number of artists for dashboard
import numpy as np

mean_price = np.mean(df['Unit_Price_dollars'])
mean_price = np.around(mean_price,2)

mean_time = np.mean(df['Total_runtime_min'])
mean_time = np.around(mean_time,2)

mean_size = np.mean(df['song_size_Mb'])
mean_size = np.around(mean_size,2)

song_num = df.Song_Track.nunique() 

df_song = df['Artist']


#Creating a histogram using plotly to show the artists in the database
#Each graph from here has update_layout method to change the layout of the graph.

fig3 = px.histogram(df_song, y ='Artist',title = 'Number of Songs Artists have in this database'.upper(), color = 'Artist', color_discrete_sequence=px.colors.qualitative.Bold)

fig3.update_layout(margin=dict(l=20, r=40, t=40, b=40), paper_bgcolor= '#e2e8f0', font_color="black",plot_bgcolor="#e2e8f0",height=1000)

fig3.update_yaxes(color='black',autorange = 'reversed',showticklabels= False,showgrid = False)


#Creating a pie chart to show the total percentage of song-size for each genre.

dff = df[['song_size_Mb','Genre']]

fig = px.pie(dff,values ='song_size_Mb', names ='Genre', title = 'Pie chart of Genres present'.upper(),color_discrete_sequence=px.colors.qualitative.Bold)

fig.update_layout(margin=dict(l=40, r=20, t=40, b=20),paper_bgcolor= '#e2e8f0',font_color="black",legend_title_text="Genre",showlegend=True)

fig.update_traces(dict(marker_line_width=0))


#Creating a scatterplot to show the runtime of each song per the song size.

dff2 = df[['Song_Track','Total_runtime_min','song_size_Mb']]

fig2 = px.scatter(dff2, x= 'song_size_Mb',y = 'Total_runtime_min', color= 'Song_Track', title = 'Total runtime of each song'.upper(),color_discrete_sequence=px.colors.qualitative.Prism)

fig2.update_layout(margin=dict(l=10, r=10, t=40, b=30), paper_bgcolor= '#e2e8f0',font_color="black",plot_bgcolor="#e2e8f0",showlegend = False) #xaxis={"categoryorder":"total descending"})

fig.update_xaxes(color='black')

fig2.update_traces(marker_size = 20)


# Tailwind CSS is set as the default css style. 
# DASH is used to create an html page.

external_script = ["https://tailwindcss.com/", {"src":"https://cdn.tailwindcss.com"}]

app = Dash(__name__, external_scripts=external_script)
server = app.server
app.scripts.config.serve_locally = True


# The dashboard has three main layouts: the h1 heading, the div containing the graphs and KPI's and the bottom part acknowledging the copyright.
# The main html and Dash components here are h1, Div,Span, Dcc and two callbacks. Callback are linked to dropdown menus and sliders to show songs from the artist selected and provide a google search on he artist as well.Tailwind CSS used in each Div is classified as 'ClassName' .

app.layout = html.Div(
    [html.H1("Mused: An Itunes Music Dashboard", id ='h1', className="w-full text-white text-6xl italic font-semibold p-8 text-center bg-[#334155] "),
    html.Div([
        html.P('''This Dashboard showcases the music playlist over a period of 
                  time. It includes the genre, song size, price in dollars and runtime of each song. 
                  Feel free to explore various genres of music with charts and menus. Discover new songs
                  and new paths!''', className = "shadow-md text-black justify-center font-semibold italic text-center rounded-md m-4 p-4 bg-[#e7ecef] shadow-md"),
        
        html.Div([
           
           html.Div(children=[
             html.Span(song_num, className="text-5xl text-center my-2 font-bold"),
             html.Span("Total Number of Songs", className="text-lg fontmedium m-4 text-center"),
         ],className=" flex flex-col justify-center p-4  text-white itemscenter rounded-md bg-[#030712]"),
         
           html.Div(children=[
             html.Span(mean_time, className="text-5xl text-center my-2 font-bold"),
             html.Span("Average Runtime of a Song in minutes", className="text-lg fontmedium ml-4 text-center"),
         ],className=" flex flex-col justify-center p-4  text-white itemscenter rounded-md  bg-[#4a044e]"),
        
            html.Div(children=[
              html.Span(mean_size, className="text-5xl text-center my-2 font-bold"),
              html.Span("Average Size of a Song in megabytes", className="text-lg fontmedium ml-1 text-center"),
         ],className=" flex flex-col justify-center p-4 text-white itemscenter rounded-md bg-[#030712]")],className="flex flex-row justify-center w-auto m-2 space-x-24 bg-[#e7ecef]"),
            
        html.Div([
              html.Div(dcc.Graph(id='genre_graph',figure = fig),className="shadow-md rounded-md shadow-md"),
              html.Div(dcc.Graph(id = 'runtime_graph', figure = fig2),className="shadow-md rounded-md shadow-md"),
              html.Div(dcc.Graph(figure=fig3),className="shadow-md col-span-2 rounded-md shadow-md"),
                        ],className="grid grid-cols-2 grid-row-2 rounded-md  gap-2 m-2 px-4 py-8 bg-[#e7ecef]"),
    
       html.Div([
         html.Div([
           html.P("Pick a Genre",className="flex flex-col p-4 justify-center text-black itemscenter rounded-sm w-full bg-[#f1f5f9]"),
           dcc.Dropdown(options = df['Genre'].unique(),value = "Genre",placeholder = 'Select genre', id = 'genre')],
           className='shadow-md p-4 justify-center text-black itemscenter rounded-md w-full bg-[#f1f5f9] shadow-md'),
           
        
           html.Div([
             html.P("Choose how long you want the song to be!", className="flex flex-col p-4 justify-center text-black itemscenter rounded-sm w-full bg-[#f1f5f9]"),
             dcc.RangeSlider( min=0, max=9,step=1.5,value=[3,7.5], id = 'runtime')],className='shadow-md p-4 justify-center itemscenter rounded-md w-full bg-[#f1f5f9] shadow-md'),
        
           html.Div([
             html.P("Select an Artist",className="flex flex-col p-4 justify-center text-black itemscenter rounded-sm w-full bg-[#f1f5f9]"),
             dcc.Dropdown(options = df['Artist'].unique(), value = 'Artist',id = 'Artist')],className='shadow-md col-span-2 p-4 justify-center text-black itemscenter rounded-md w-full bg-[#f1f5f9] shadow-md'
           )],className="grid grid-cols-2 grid-row-3 gap-2 p-2 space-y-2 justify-center text-black itemscenter rounded-md"),
            
         html.Div([
           html.P("What did you select? Choose from the menus above!",className = "shadow-md flex p-2 font-semibold italic justify-center text-center bg-[#cbd5e1] shadow-md"),
           html.Span(children="Select your favorite song from the dropdown menus", id = 'output', className = "flex p-2 justify-center font-semibold italic  text-center"),
           html.A(children = "Press Me to learn more about the artist! (;>)", href= "www.google.com", id = 'site',className = 'shadow-md flex p-2 justify-center font-semi-bold italic space-y-2 rounded-md text-white text-center bg-[#701a75] shadow-md'),
        ],className = 'flex justify-center rounded-md flex-col gap-y-2 bg-[#f8fafc]'),
        
        ],className = 'shadow-md -mt-4 mx-4 mb-4 p-2 rounded-md bg-[#e7ecef] shadow-md'), 
     
      html.Div(children = "Ama Assiamah. Data Copyright: Apple. @2023", className =" w-full text-white text-md italic p-4 text-center bg-[#334155]")],
        
      className="flex flex-col w-full bg-[#334155] max-w-screen-6xl")

@app.callback(
        Output('output', 'children'),
        Input('genre','value'),
        Input('runtime','value'),
        Input('Artist','value'))

def genregraph(g,r,a):
    dff = df[['Artist','Total_runtime_min','Genre','Song_Track']]
    minnum,maxnum = r
    y = []  
    for x in dff.loc[( (dff["Genre"]==g) & ((dff["Artist"]==a)&(dff['Total_runtime_min']<maxnum))),'Song_Track']:
        y.append(x)
    return "Artist: {0}.\nGenre: {1}.\nThese are the list of songs available for this artist: {2}".format(a,g,y)
    
@app.callback(
        Output('site', 'href'),
        Input('Artist','value'))
def exploremusic(t):
    return "https://www.google.com/search?safe=active&q={}&spell=1&sa=X&ved=2ahUKEwi3-oW5yOz9AhUEgv0HHQZ7CXYQBSgAegQIBxAB&biw=1431&bih=746&dpr=1.25".format(t)

if __name__ == "__main__":
     app.run_server()

