import mysql.connector


class Database():
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        try:
                self.mydb = mysql.connector.connect(
                    user='root',
                    password='password',
                    host='localhost',
                    port='3306',
                    database='antelearn'
                )
                self.mycursor = self.mydb.cursor()
                print("Bağlandı")

        except:
            print("Bağlantı Gerçekleşmedi")
    def series_select(self):
        query = "SELECT * FROM antelearn.movies WHERE series_id='7';"
        self.mycursor.execute(query)
        y = self.mycursor.fetchall()
        print(y)
    def most_used_words(self,word,translation):# İngilizcede en çok kullanılan 1000 kelimeyi eklemek amacıyla yapılan SQL komutu
        query = "INSERT INTO antelearn.most_used_words(word,translation) VALUES(%s,%s)"
        val=(word,translation)
        self.mycursor.execute(query,val)
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted.")
    """
    #dizi ekleme bölümü 
    def series_insert(self,series_name):
        query = "INSERT INTO antelearn.movies(series_id,series_name) VALUES (%s,%s)"
        val=(series_name)
        self.mycursor.execute(query,(val,))
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted.")"""


    def patterns_split(self,patterns,translation,definition):#ingilizce kalıp ekleme bölümü
        query = "INSERT INTO antelearn.movies_patterns(movies_patterns,movies_translation,movies_definition) VALUES (%s,%s,%s)"
        val=(patterns,translation,definition)
        self.mycursor.execute(query,val)
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted")
    def patterns_counter(self,counter): #İngilizce kalıpları saydırmak amacıyla kullanılan bölüm
        query = "SELECT patterns FROM antelearn.movies_patterns WHERE patterns_id =%s"

        self.mycursor.execute(query,(counter,))
        result = self.mycursor.fetchone()
        if result:
            return result
        else:
            return False
    def patterns_total_number(self):
        query ="SELECT COUNT(movies_patterns_id) FROM antelearn.movies_patterns"
        self.mycursor.execute(query)
        result = self.mycursor.fetchone()
        return result
    def save_a_series_db(self,series_name,description):
        query =" INSERT INTO antelearn.movies_movies_series(series_name) VALUES (%s)"

        self.mycursor.execute(query,(series_name,description,))
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted: ",series_name)

    def season_control_db(self,series_name,season_no): #Sezon numarası daha önce eklenmiş mi diye kontrol ediyor.
        query = "SELECT season_no FROM antelearn.movies_season WHERE season_no= " \
                "ANY(SELECT season_no FROM antelearn.movies_season WHERE series_name = %s and season_no=%s)"
        self.mycursor.execute(query, (series_name,season_no,))
        result = self.mycursor.fetchone()
        if result:
            return result
        else:
            return False
    def save_a_season_db(self,series_name,season_no):#Sezonu database'e ekliyoruz
        query = "INSERT INTO antelearn.movies_season(series_name,season_no) VALUES(%s,%s)"
        val = (series_name,season_no)
        self.mycursor.execute(query, val)
        self.mydb.commit()
        print(self.mycursor.rowcount, " record inserted: ", series_name+" sezon : "+season_no)

    def series_control_db(self,series_name):#Eklenecek olan dizi database'de var mı diye kontrol gerçekleştiriliyor.
        query ="SELECT series_name FROM antelearn.movies_series WHERE series_name = " \
               "ANY(SELECT series_name FROM antelearn.movies_series WHERE series_name = %s);"
        self.mycursor.execute(query,(series_name,))
        result = self.mycursor.fetchone()
        if result:
            return result
        else:
            return False
    def save_a_episode_db(self,series_id,season_id,episode_name,episode_no,episode_filepath):#Bölüm ekleme
        query = "INSERT INTO antelearn.movies_episode(series_id,season_id,episode_name,episode_no,episode_filepath) VALUES(%s,%s,%s,%s,%s)"
        val=(series_id,season_id,episode_name,episode_no,episode_filepath)
        self.mycursor.execute(query,val)
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted: ",episode_name)
    def series_to_episode(self,series_name):
        query = "SELECT series_id FROM antelearn.movies_series WHERE series_name=%s"
        self.mycursor.execute(query,(series_name,))
        result = self.mycursor.fetchone()
        return result
    def save_a_word_db(self,series_id,season_id,episode_id,word,count,translation):#Text dosyasından gelen tüm kelimeleri database'e eklemeyi sağlıyor
        query = "INSERT INTO antelearn.movies_words(series_id,season_id,episode_id,word,count,translation) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (series_id,season_id,episode_id,word,count,translation)
        self.mycursor.execute(query,val)
        self.mydb.commit()
        print(self.mycursor.rowcount," record inserted",word+" :"+translation)
    def filepath_control(self,filepath):
        query = "SELECT series_id,season_id,episode_id FROM antelearn.movies_episode WHERE episode_filepath = " \
                "ANY(SELECT episode_filepath FROM antelearn.movies_episode WHERE episode_filepath = %s);"
        self.mycursor.execute(query, (filepath,))
        result = self.mycursor.fetchone()
        resArr = []
        if result:
            for res in result:
                resArr.append(res)
            return resArr
        else:
            return False
    def most_used_words_with_words(self): #dizinin içinde geçmiş olan kelimeleri en çok kullanılan 1000 kelimede de geçiyor mu diye bakan kod
        query = "SELECT antelearn.movies_words.word, antelearn.movies_most_used_words.translation , antelearn.movies_words.count" \
                " FROM antelearn.movies_words " \
                "INNER JOIN antelearn.movies_most_used_words " \
                "on antelearn.movies_most_used_words.word = antelearn.movies_words.word";
        self.mycursor.execute(query)
        res = self.mycursor.fetchall()
        print(res[0][0])
        self.mydb.commit()
        return res
    def wordgame(self):
        query = "SELECT episode_id FROM antelearn.movies_words GROUP BY episode_id"
        self.mycursor.execute(query)
        res = self.mycursor.fetchall()
        self.mydb.commit()
        return res
    def wordgame_db_select(self,episode_id):
        query ="SELECT antelearn.movies_words.word FROM antelearn.movies_words WHERE episode_id = %s"
        self.mycursor.execute(query,(episode_id,))
        res = self.mycursor.fetchall()
        self.mydb.commit()
        return res


