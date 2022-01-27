#get database
import imdb
imdbInstance=imdb.IMDb()

#person search
def personSearch(personName):
    searchResult=imdbInstance.search_person(personName)
    return searchResult
def getPersonId(persons,personNumber):
    personNumber=int(personNumber)
    return persons[personNumber-1].personID
def getPerson(personId):
    return imdbInstance.get_person(personId)

#movie search
def movieSearch(movieName):
    return imdbInstance.search_movie(movieName)
def getMovieId(movies,movieNum):
    movieNum=int(movieNum)
    return movies[movieNum-1].movieID
def getMovie(movieId):
    return imdbInstance.get_movie(movieId)

#get available informations
def getAvailableInfos(obj):
    return sorted(obj.keys())

#get info
def getInfo(obj,info):
    result=list()
    for res in obj[info]: result.append(res)
    return result

#search methods
def searchMovieByKeyword(keyWord):
    return imdbInstance.get_keyword(keyWord)
def searchTop250ImbdMovies():
    return imdbInstance.get_top250_movies()