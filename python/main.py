from antelearn_web.python import DbHelper
import word_insert
word_insert = word_insert.WordInsert
db = DbHelper.Database()
"""
#burası metin dosyasından noktalama 
işaretlerini kaldırmak için çağırılan class yapısı 
buraya rastgele istenilen dosya gelecek#
"""

"""filepath= input("düzenlenecek bir dosya adresi girin: ")
remove_punctuations.Remove_punctuation(filepath)
"""
#print(db.most_used_words_with_words())
"""
verilen text dosyasını hazır hale getiren kod"""
word_insert("howimetyourmothers1e3.txt")






















