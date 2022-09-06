#Flask Integration
from flask import Flask, request, jsonify

app = Flask(__name__)
#Packages
import pandas as pd
import numpy as np
import scipy as sp
import pickle

#Dataframes

synopsis = pickle.load(open('synopsis_df_copy.pkl', 'rb'))
synopsis_df = pd.DataFrame(synopsis)


item_sim = pickle.load(open('item_sim_small.pkl', 'rb'))
item_sim_df = pd.DataFrame(item_sim)



#Functions for Getting MetaData6
@app.route('/GetAnimeFrame/<anime>')
def GetAnimeFrame(anime = None): 
  if isinstance(anime, int):
    return synopsis_df[synopsis_df.anime_id == anime]
  if isinstance(anime, str):
    return synopsis_df[synopsis_df.Name == anime]

@app.route('/getID')
def getID(anime):
  frame = GetAnimeFrame(anime)
  anime_id = frame.anime_id.values[0]
  return anime_id

@app.route('/getName/<anime>')
def getName(anime = None):
  anime = int(anime)
  frame = GetAnimeFrame(anime)
  Name = frame.Name.values[0]
  return Name

@app.route('/getGenre')
def getGenre(anime):
  anime = int(anime)
  frame = GetAnimeFrame(anime)
  genre = frame.Genres.values[0]
  return genre

@app.route('/getSynopsis')
def getSynopsis(anime):
  anime = int(anime)
  if isinstance(anime, int): # If Anime ID was Given (Integer)
    return synopsis_df[synopsis_df.anime_id == anime].synopsis.values[0]
  if isinstance(anime, str): #If Anime Title was Given (String)
    return synopsis_df[synopsis_df.Name == anime].synopsis.values[0]

@app.route('/getimg/<anime>')
def getimglink(anime): 
  anime = int(anime)
  frame = GetAnimeFrame(anime)
  imgurl = frame.imgurl.values[0]
  return imgurl

def getIDlist():
  anime_list = []
  for i in range(len(synopsis_df)): 
    anime_list.append(str(synopsis_df.iloc[i, 0])) #Get ID and convert it to string
    
  return anime_list

#Functions for Getting All metadata together

@app.route('/getmetadataName/<anime>')
def getmetadataName(anime = None):
    metadata = []

    frame = GetAnimeFrame(anime)
    anime_id = frame.anime_id.values[0]
    Name =  frame.Name.values[0]
    genre = frame.Genre.values[0]
    synopsis = frame.synopsis.values[0]
    imgurl = frame.imgurl.values[0]
    metadata.append({
                 'anime_id': int(anime_id),
                 'Name': str(Name),
                 'Genre': str(genre),
                 'Synopsis':str(synopsis),
                 'imgurl': str(imgurl)
                 })
    return jsonify(metadata)

@app.route('/getmetadataID/<anime>')
def getmetadata(anime = None):
    anime = int(anime)
    metadata = []

    frame = GetAnimeFrame(anime)
    anime_id = getID(anime)
    Name = getName(anime)
    genre = getGenre(anime)
    synopsis = getSynopsis(int(anime_id))
    imgurl = getimglink(anime_id)
    metadata.append({
                 'anime_id': int(anime_id),
                 'Name': str(Name),
                 'Genre': str(genre),
                 'Synopsis':str(synopsis),
                 'imgurl': str(imgurl)
                 })
    return jsonify(metadata)


#Recommender System
@app.route('/recommend/<anime_name>', methods = ['GET'])
def rec_animes(anime_name = None):
    final_list = []

    #Get ID based on Title
    #frame = GetAnimeFrame(int(anime_id))
    #anime_name = frame.anime_id.values[0] #Use the Name to get Similar Animes
    
    #count = 1
    #print('Similar shows to {} include:\n'.format(anime_name))
    for item in item_sim_df.sort_values(by = anime_name, ascending = False).index[1:6]: #index[1:6] it starts in 1 so that it wont recommend itself, and 6 so that it prints animes in the index from 1-6
      #Gets the metadata of each anime and then put them in a dictionary which will be appended to a list so that it can be converted into a json file
      frame = GetAnimeFrame(item)
      anime_id = frame.anime_id.values[0]
      Name =  frame.Name.values[0]
      genre = frame.Genres.values[0]
      synopsis = frame.synopsis.values[0]
      imgurl = frame.imgurl.values[0]
      final_list.append({
                 'anime_id': int(anime_id),
                 'Name': str(Name),
                 'Genres': str(genre),
                 'Synopsis':str(synopsis),
                 'imgurl': str(imgurl)
                 })
    return jsonify(final_list)

@app.route('/getreply')
def getreply(reply = None):
  return jsonify({'Reply': 'Hello'})

if __name__ == '__main__':
    app.run()
