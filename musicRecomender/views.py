from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#import requests
from .models import *


# load data from db

music = Music.objects.all()


# convert data to a dataframe

data = music.values('Title', 'Artist', 'Genre',
                    'Beats_per_minute', 'Danceability', 'music_id')
dataFrame = pd.DataFrame.from_records(data)


# create a list with all relative string in it for comparison

def combine_data(data):
    new_list = []
    for i in range(0, data.shape[0]):
        new_list.append(data['Title'][i] + " " + data['Artist'][
                        i] + " " + data['Genre'][i] + " " + str(data['Beats_per_minute'][i]) + " " + str(data['Danceability'][i]) + " " + str(data['music_id'][
                            i]))
    return new_list


# find the song by its title

def get_music_id_from_title(request):
    title = get_name(request)
    try:
        return dataFrame[dataFrame.Title == title]['music_id'].values[0]
    except:
        return ["song not in database"]


# sort the list of similarity index in desending order

def sort_the_list(music_id):
    try:
        sorted_list = list(enumerate(cosine_sim[music_id],))
        sorted_list = sorted(
            sorted_list, key=lambda x: x[1], reverse=True)
        sorted_list = sorted_list[1:]
        return sorted_list
    except:
        return "song not in database"


# get recommendation

def get_recommended(music_id):
    sorted_list = sort_the_list(music_id)
    if (sorted_list == "song not in database"):
        return ["song not in database"]
    else:
        recomendation_list = []
        for i in sorted_list:
            if i[0] == 7:
                break
            title = dataFrame[dataFrame.music_id == i[0]]['Title'].values[0]
            artist = dataFrame[dataFrame.music_id == i[0]]['Artist'].values[0]
            recomendation_list.append(title + " by " + artist)
        return recomendation_list


# create a new colum in the dataframe

dataFrame['features'] = combine_data(dataFrame)


# find the count vector of the new colum

count_vector = CountVectorizer().fit_transform(dataFrame['features'])


# find the cosine similarity of the count vector

cosine_sim = cosine_similarity(count_vector)


# Create your views here.


def get_name(request):
    try:
        name = request.POST['name']
    except:
        name = ""
    return name


def setMessage(request):
    if(get_recommended(get_music_id_from_title(request)) == ["song not in database"]):
        response = " "
        return response
    else:
        response = "Because you like " + \
            get_name(request) + " we recommend these:"
        return response


def indexView(request):

    context = {


    }
    return render(request, 'musicRecomender/index.html', context)


def recommendView(request):
    context = {
        'data': get_recommended(get_music_id_from_title(request)),
        'name': get_name(request),
        'message': setMessage(request)
    }
    return render(request, 'musicRecomender/recomend.html', context)


def songListView(request):
    context = {
        'data': music

    }
    return render(request, 'musicRecomender/songlist.html', context)
