import http

import mysql.connector
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import random



from .models import series,words,season,episode,most_used_words,patterns,game
from .models import registerUser



try: # MYSQL'e bağlantı gerçekleştirdiğimiz bölüm
    mydb = mysql.connector.connect(
                        user='root',
                        password='password',
                        host='localhost',
                        port='3306',
                        database='antelearn'
                    )
    mycursor = mydb.cursor()
    mycursor1 = mydb.cursor()
    mycursor2 = mydb.cursor()
    mycursor3 = mydb.cursor()
    print("SQL'e bağlandı...")
except:
    print("Bağlantı gerçekleşemedi...")
control = False

def loginUser(request):

    #Daha önceden kayıt olmuş bir kullanıcının giriş yapmasını sağlayan komut
    query = "SELECT username From antelearn.movies_registeruser WHERE email = %s and password = %s"

    if request.method == "POST":
        print("POST GERÇEKLEŞTİ")
        email = request.POST["email"]
        password = request.POST["password"]


        val = (email,password)
        mycursor.execute(query,val)
        res = mycursor.fetchone()
        if res:
            global control
            control=True
            return redirect('series')
        else:
            return render(request,"index.html",{
                "error" : "username or password wrong."
            })

    return render(request,"index.html")

def register(request):
    print("girildiabi")
    #Kayıt olan kullanıcının bilgilerini database'e kaydeden fakat username veya email adresi farklı olmalı
    query = "INSERT INTO antelearn.movies_registeruser(username,email,password,telephone_number,repeat_password,role) " \
            "VALUES (%s,%s,%s,%s,%s,%s)"
    query2 = "SELECT id from antelearn.movies_registeruser WHERE EXISTS" \
             "(SELECT 1 FROM antelearn.movies_registeruser WHERE username = %s or email = %s)"

    if request.method=="POST":
        print("girildi")
        username = request.POST["username"]
        email = request.POST["email"]

        telephonenumber = request.POST["telephonenumber"]
        password = request.POST["password"]
        rePassword = request.POST["repassword"]
        role = request.POST["role"]
        if rePassword==password:

            val2=(username,email)
            mycursor.execute(query2,val2)
            result =mycursor.fetchall()
            print(result)
            if result:
                return render(request, "register.html", {
                    "error": "username ya da email daha önce kullanılmış"
                })

            else:
                val=(username,email,password,telephonenumber,rePassword,role)
                mycursor1.execute(query,val)
                mydb.commit()
                print("kayıt gerçekleşti")
                return redirect('login')
        else:
            print("pass aynı değil")
            return render(request, "register.html", {
                "error": "password aynı degil"
            })


    return render(request,"register.html")
def logout(request):
    try:
        del csrf_token
    except:
        return render(request,"index.html")
    return render(request,"index.html")

def price(request):
    return render(request,"price.html")


def ser(request):


    print("İLK BURAYA GİRDİK")
    data = {
        "series": series.objects.all(),
    }

    return render(request,"series.html",data)




def dropdown(request,series_id):
    print("girdin kanks sonunda")
    #Sıralı bir şekilde dizinin id'sine göre sezon numaralarını getiren komut
    query = "SELECT DISTINCT antelearn.movies_season.season_no " \
            "FROM antelearn.movies_season " \
            "inner join antelearn.movies_episode " \
            "on antelearn.movies_episode.season_id = antelearn.movies_season.season_id " \
            "WHERE antelearn.movies_episode.series_id = %s ORDER BY antelearn.movies_season.season_no"
    mycursor.execute(query, (series_id,))
    print("buraya geldik")
    res = mycursor.fetchall()
    dizi = []
    for i in range(len(res)):
        dizi.append(int(''.join(map(str, res[i]))))
    print(dizi)
    if (len(dizi)>0):
        for i in range (len(dizi)):
            print("girdik")
            data = {
                "res": dizi,
                "series_id": series_id,
            }
            render(request,"season.html",data)
        return render(request, "season.html", data)
    else:
        return render(request,"series.html")
    return render(request,"season.html",data)

def episode(request,series_id,season_no):
    #Benzersiz şekilde bölüm numaralarını getiren sql komutu
    query2 = "SELECT DISTINCT antelearn.movies_episode.episode_no " \
             "FROM antelearn.movies_episode " \
             "inner join antelearn.movies_season " \
             "on antelearn.movies_season.season_id = antelearn.movies_episode.season_id " \
             "WHERE antelearn.movies_season.season_no =%s and antelearn.movies_episode.series_id = %s"
    #dizinin id'sine göre dizinin adını gösteren sql komutu
    query = "select series_name from antelearn.movies_series " \
            "where series_id = %s"
    #dizinin id'si ve sezon numarasına göre benzersiz bir biçimde dizinin bölüm isimlerini getiren komut
    query3 = "select distinct episode_name from antelearn.movies_episode " \
             "inner join antelearn.movies_season " \
             "on antelearn.movies_season.season_id = antelearn.movies_episode.season_id " \
             "where antelearn.movies_season.season_no = %s and antelearn.movies_episode.series_id = %s"
    #dizinin id'sine göre fotoğrafları ekrana getiren komut
    query4 = "select distinct movies_episode.episode_img from antelearn.movies_episode where series_id =%s "



    val4 = (series_id,)
    mycursor3.execute(query4,val4)
    epis_img = mycursor3.fetchall()
    val = (season_no, series_id)
    val2 = (series_id,)
    val3 = (season_no,series_id)
    mycursor2.execute(query3,val3)
    episode_name = mycursor2.fetchall()
    mycursor1.execute(query2, val)
    res2 = mycursor1.fetchall()
    mycursor.execute(query,val2)
    series_name = mycursor.fetchall()
    dizi2 = []
    seriesname = series_name[0][0]
    episodename = []
    image = []
    for i in range(len(episode_name)):
        episodename.append(episode_name[i][0])
    for j in range(len(epis_img)):
        image.append(epis_img[j][0])

    print(epis_img[0][0])
    print(series_name[0][0])
    episode_id= []
    print(res2)
    for k in range(len(res2)):
        dizi2.append(int(''.join(map(str, res2[k]))))
        episode_id.append(get_episode_id(int(''.join(map(str, res2[k]))),series_id,season_no))

    data = {
        "episode_id": episode_id,
        "episode": dizi2,
        "series_id": series_id,
        "season_no": season_no,
        "seriesname": seriesname.capitalize(),
        "episodename": episodename,
        "image": image,
    }

    print("episodee: ", episode_id)
    print("season: ", season_no)
    print("series: ", series_id)
    print("data -->",dizi2)
    return render(request,"episode.html",data)

def get_episode_id(episode_no,series_id,season_no): #Bölüm id'sini çağırarak path'e göndermek amacıyla kullanılan komut
    query = "SELECT DISTINCT antelearn.movies_episode.episode_id " \
             "FROM antelearn.movies_episode " \
             "inner join antelearn.movies_season " \
             "on antelearn.movies_season.season_id = antelearn.movies_episode.season_id " \
             "WHERE antelearn.movies_season.season_no =%s and antelearn.movies_episode.series_id = %s and antelearn.movies_episode.episode_no = %s"
    val = (season_no, series_id,episode_no)
    mycursor1.execute(query, val)
    res2 = mycursor1.fetchall()
    print(res2)
    return res2
point=0
true =0
wrong = 0
def series_to_game(request,series_id,season_no,episode_id):#Bölüm id'sine göre alıştırma kısmına geçilen kısım
    print("series_to_game girildi")
    print(episode_id)
    val = (episode_id, series_id, season_no)
    query = "select episode_id from antelearn.movies_episode " \
            "INNER JOIN antelearn.movies_season " \
            "on antelearn.movies_episode.season_id = antelearn.movies_season.season_id " \
            "where episode_no = %s and series_id = %s and season_no =%s"
    mycursor.execute(query, val)
    res = mycursor.fetchall()
    data = {
        "serie": series_id,
        "epis": episode_id,
        "season": season_no,
        "res": res,
    }
    dizi = []
    for i in range(len(res)):
        dizi.append(res[i][i])

    print("episodee: ", episode_id)
    print("season: ", season_no)
    print("series: ", series_id)

    return seriesgame(request, dizi[0])


def seriesgame(request,episode_id): #Dizinin ilgili bölümünün id'sine göre kelimeleri rastgele olmak şartıyla karşımıza çıkaran kısım
    mycursor.execute("DELETE FROM antelearn.movies_game WHERE words_id>0")
    mydb.commit()
    query2 = "INSERT INTO antelearn.movies_game(word,translation,count) VALUES (%s,%s,%s)"
    query = "SELECT antelearn.movies_words.word, antelearn.movies_most_used_words.translation , antelearn.movies_words.count " \
            "FROM antelearn.movies_words " \
            "inner join antelearn.movies_most_used_words " \
            "ON antelearn.movies_most_used_words.word = antelearn.movies_words.word " \
            "WHERE antelearn.movies_words.episode_id = %s";
    mycursor.execute(query,(episode_id,))
    res = mycursor.fetchall()
    jumbbled_words=[]
    if len(res)>20:
        rannums = random.sample(range(0, len(res)), 20)

        for i in range(20):
            unique = rannums[i]
            word = res[unique][0]
            translation = res[unique][1]
            count = res[unique][2]
            mycursor1.execute(query2,(word,translation,count,))
            mydb.commit()
            jumbbled_words.append(word)
        global point
        point = 0
        global true
        true =0
        global wrong
        wrong=0
        """print("dizi*>",jumbbled_words)
        jumbbledGame(jumbbled_words)"""

    else:
        rannums = random.sample(range(0, len(res)), len(res))
        for i in range (len(res)):
            unique = rannums[i]
            word = res[unique][0]

            translation = res[unique][1]
            count = res[unique][2]
            mycursor1.execute(query2,(word,translation,count,))
            mydb.commit()
    data = {
        "games" : game.objects.all()
    }

    return render(request,"seriesgame.html",data)


def homePage(request):
    return render(request,"home-page.html")



def jumbbledGame(request):
    global word,jword,wrong,true
    jumbbled_words =[]
    jwordlist =[]
    query = "SELECT antelearn.movies_game.word FROM antelearn.movies_game"
    mycursor.execute(query)
    res = mycursor.fetchall()
    for i in range(len(res)):
        jumbbled_words.append(res[i][0])
    print("/////",jumbbled_words)
    if len(jumbbled_words)>0:
        word = random.choice(jumbbled_words)
        jumbbled = random.sample(word,len(word))
        jword = "".join(jumbbled)
        for letter in jword:
            jwordlist.append(letter)
        print("***",jwordlist)
    else:
        message = ("Oyun bitti kardeşim, puanın: ",point)
        return render(request,"jumbbledGame.html",{
            "point": point,
            "wrong" : wrong,
            "true" : true,
            "message" : message,
        })
    data = {
        "word" : word,
        "jword" : jwordlist,
        "point" : point,
        "wrong": wrong,
        "true": true,
    }
    print("---",jword)
    return render(request,"jumbbledGame.html",data)

def controlJumbbled(request):
    global jword,word,msg,point,true,wrong
    jumbbled_words=[]

    user_answer = request.GET['answer']
    print(user_answer)
    query = "SELECT antelearn.movies_game.word FROM antelearn.movies_game"
    query2 = "DELETE FROM antelearn.movies_game WHERE antelearn.movies_game.word = %s"
    mycursor.execute(query)
    res = mycursor.fetchall()
    for i in range(len(res)):
        jumbbled_words.append(res[i][0])
    for i in range (len(jumbbled_words)):
        if jumbbled_words[i]==user_answer:
            msg = "Doğru"
            point=point+10
            true=true+1
            mycursor1.execute(query2,(jumbbled_words[i],))
            mydb.commit()
            return jumbbledGame(request)
    point = point-4
    wrong = wrong+1
    if point<=0:
        point=0
    dizi=[]
    for i in range (point):
        dizi.append(i)
    print("scoRe",dizi)

    return render(request,"jumbbledGame.html",{
        'jword' : jword,
        'point' : point,
        'dizi' : dizi,
        'wrong' : wrong,
        'true' : true,
    })
def buttonClick(request):
    btn = request.GET['harfButon']
    print(btn)

def pointtable(request):
    return render(request,"pointtable.html")
def admin(request):
    return render(request,"admin.html")
def hexagongame(request):
    return render(request, "hexagongame.html")






