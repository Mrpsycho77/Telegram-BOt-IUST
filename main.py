#libs
import requests
import time
from myimdblib import *

#token
myToken='bot5153473021:AAGDH7MF5JLwbMXWhDbWACsuupkCKLhxSC4'
myBot='https://api.telegram.org/'+myToken+'/'

#get update
def getAllUpdate():
    result=requests.get(myBot+'getUpdates')
    return result.json()
def getAllMessages():
    allUpdates=getAllUpdate()
    res=list()
    for i in allUpdates['result']:
        res.append(list([i['message']['chat']['id'],i['message']['text']]))
    return res

#send update
def sendMessage(chatId,messText):
    requests.get(myBot+'sendMessage?chat_id='+str(chatId)+'&text='+messText)
    return None

#main
chatNo=1
chat=''
searchMet=1
#del pervius updates
requests.get(myBot+'getUpdates?offset='+str(getAllUpdate()['result'][len(getAllUpdate()['result'])-1]['update_id']))
print('Checking',end='')
try:
    while True:
        time.sleep(1)
        print('.',end='')
        #get chat
        try:
            chat=getAllMessages()[chatNo]
            chatNo+=1
            print()
            print(chat)
        except: continue
        chat[1]=chat[1].lower()
        #/start
        if chat[1]=='/start':
            sendMessage(chat[0],'Welcome to Movie Finder Bot.\nDo you want search for [person] or [movie]?')
            print('Welcome to Movie Finder Bot.\nDo you want search for [person] or [movie]?')
        #person
        elif chat[1]=='person':
            sendMessage(chat[0], 'Please write the person name.')
            print('Please write the persons name.')
            searchMet=1
        elif chat[1]=='movie':
            sendMessage(chat[0], 'Do you want to search by [name] or [keyword] or want to see [top250] imdb movies?')
            print('Do you want to search by [name] or [keyword] or want to see [top250] imdb movies?')
            searchMet=2
        elif chat[1]=='reset':
            searchMet=1
            sendMessage(chat[0],'Welcome to Movie Finder Bot.\nDo you want search for [person] or [movie]?')
            print('Welcome to Movie Finder Bot.\nDo you want search for [person] or [movie]?')
            continue
        #searching
        else:
            #person
            if searchMet==1:
                res=''
                persons=personSearch(chat[1])
                counter=1
                for i in persons:
                    if counter>10: break
                    res=res+'\n'+str(counter)+'- '+i['name']
                    counter+=1
                res+='\nPlease write the number of person who you want to know.'
                sendMessage(chat[0], res)
                print(res)
                searchMet=12
            elif searchMet==12:
                person=getPerson(getPersonId(persons,chat[1]))
                res='Birth day: '
                try:
                    for i in getInfo(person,'birth date'):
                        res+=i
                except: res=''
                res+='\nMini biography:\n'
                for i in getInfo(person,'mini biography'):
                    res+=i
                res+='\nFilmography:\n'
                for job in person['filmography'].keys():
                    if job!='actor' and job !='director': continue
                    res=res+'-Job: '+job+'\n'
                    for movie in person['filmography'][job]:
                        res=res+movie['title']+' role: '+str(movie.currentRole)+'\n'
                ans=list([''])
                for i in res:
                    ans[len(ans)-1]+=i
                    if len(ans[len(ans)-1])>=4000: ans.append('')
                for i in ans:
                    sendMessage(chat[0], i)
                    print(i)
                searchMet=1
                res='Done!\nDo you want search for [person] or [movie]?'
                sendMessage(chat[0], res)
                print(res)
            #movie
            elif searchMet==2:
                if chat[1]=='name':
                    res='Please write the movies name.'
                    searchMet=21
                    sendMessage(chat[0], res)
                    print(res)
                elif chat[1]=='keyword':
                    res='Please write your keyword.'
                    searchMet=22
                    sendMessage(chat[0], res)
                    print(res)
                elif chat[1]=='top250':
                    movies=searchTop250ImbdMovies()
                    ans=list()
                    ans.append('')
                    counter=1
                    for i in movies:
                        ans[len(ans)-1]+=str(counter)+'-'+i['title']+'\n'
                        counter+=1
                        if counter%100==0: ans.append('')
                    for i in ans:
                        sendMessage(chat[0], i)
                        print(i)
                    searchMet=2
                    res='Done!\nDo you want search for [person] or [movie]?'
                    sendMessage(chat[0], res)
                    print(res)
            elif searchMet==22:
                movies=searchMovieByKeyword(chat[1])
                ans=list()
                ans.append('')
                counter=1
                for i in movies:
                    ans[len(ans)-1]+=str(counter)+'-'+i['title']+'\n'
                    counter+=1
                    if counter%100==0: ans.append('')
                for i in ans:
                    sendMessage(chat[0], i)
                    print(i)
                searchMet=2
                res='Done!\nDo you want search for [person] or [movie]?'
                sendMessage(chat[0], res)
                print(res)
            elif searchMet==21:
                movies=movieSearch(chat[1])
                counter=1
                res=''
                for i in movies:
                    if counter>10: break
                    res=res+'\n'+str(counter)+'- '+i['title']
                    counter+=1
                res+='\nPlease write the number of movie which you want to know.'
                sendMessage(chat[0], res)
                print(res)
                searchMet=212
            elif searchMet==212:
                movie=getMovie(getMovieId(movies,chat[1]))
                res='Year: '+str(movie['year'])+'\nDirectors:\n'
                for i in getInfo(movie,'directors'):
                    res+=i['name']+'\n'
                res+='Cast:\n'
                for i in getInfo(movie,'cast'):
                    res+=i['name']+': '+str(i.currentRole)+'\n'
                ans=list()
                ans.append('')
                for i in res:
                    ans[len(ans)-1]+=i
                    if len(ans[len(ans)-1])>=4000: ans.append('')
                for i in ans:
                    sendMessage(chat[0], i)
                    print(i)
                res='Done!\nDo you want search for [person] or [movie]?'
                searchMet=2
                sendMessage(chat[0], res)
                print(res)
except:
    res='Wrong input. Please [reset] the bot.'
    print(res)
    sendMessage(chat[0], res)