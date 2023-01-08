from antelearn_web.python import DbHelper
import random
import string
db = DbHelper.Database()

def same_letters(string1, string2):
    # Create frequency maps for each string
    map1 = {}
    map2 = {}
    for ch in string1:
        if ch in map1:
            map1[ch] += 1
        else:
            map1[ch] = 1
    for ch in string2:
        if ch in map2:
            map2[ch] += 1
        else:
            map2[ch] = 1
    # Compare the maps
    if len(map1) != len(map2):
        return False
    for ch in map1:
        if ch not in map2 or map1[ch] != map2[ch]:
            return False
    return True

def generate_random_string():
  # Get all the ASCII lowercase letters and digits
  characters = string.ascii_lowercase
  # Generate a random string of 6 characters
  random_string = ''.join(random.choices(characters, k=6))
  return random_string

# Generate a random string and print it
random_string_list =[]
wordcount1=0
def check_word(word, letters):
    clear_letters=[]
    for i in letters:
        clear_letters.append(i)
      # Initialize a count for the number of matching letters
    count = 0
  # Iterate through each letter in the word
    for letter in word:
    # Check if the letter is in the set of letters
        if letter in clear_letters:
            clear_letters.remove(letter)
      # If it is, increment the count
            count += 1
        else :
            count=-5
    global wordcount1
  # Return True if the count is at least 3, False otherwise
    if count >=3:
        if len(word)<7:
            wordcount1=wordcount1+1

genelcount=0
control =0
myList= []

random_str_list =[]
wordcount =0
episode_id_list = []

episode_id_list.append(db.wordgame())

x=[]
word_list = []

def random_set_of_letters(list):
    global genelcount,myList,random_str_list,word_count,episode_id_list,wordcount,wordcount1,control
    for word in list:
        myList.append(''.join(map(str,word)))
    print(myList)
    if len(myList)>100:


        while(genelcount<10):
            random_str =generate_random_string()
            if wordcount==0:
                random_str_list.append(random_str)
                wordcount=wordcount+1
            else:
                for ran in random_str_list:
                    if same_letters(ran, random_str):
                        control += 1
                        break
                if control != 0:
                    pass
                    """print(ran + " ile " + random_str + " aynı.")"""
                else:
                    random_str_list.append(random_str)
                    wordcount += 1

                control=0

                for k in range (len(myList)):
                    check_word(myList[k],random_str)

                if wordcount1>7:
                    print("Dizi : ", random_str, " kelime sayisi: ", wordcount1)
                    genelcount=genelcount+1
                wordcount1=0
        genelcount=0
        myList.clear()

for i in range (len(episode_id_list[0])):
    x.append(episode_id_list[0][i])
    print("Episode id: ",''.join(map(str,x[i])))
    random_set_of_letters(db.wordgame_db_select(''.join(map(str,x[i]))))