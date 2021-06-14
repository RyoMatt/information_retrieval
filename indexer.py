import json
import glob
import requests
import collections
import math
from bs4 import BeautifulSoup

dictTop=0
def findPath(root):
    #print(pathList)
    filePath=glob.glob(root+"\\*")
    extractText(filePath)

def ex(soup):
    text=""
    for a in soup.find_all("title"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h1"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h2"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h3"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h4"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h5"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("h6"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("b"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("strong"):
        text+=a.get_text(strip=True)+" "
    for a in soup.find_all("italic"):
        text+=a.get_text(strip=True)+" "

    text = text.replace("\\n", " ")
    text = text.replace("\\r", " ")
    text = text.replace("\\t", " ")
    text = text.replace("\\", " ")
    text = text.replace("\\\\", " ")

    return text

def extractText(pathList):
    global dictTop

    for path in pathList:
        with open(path,"r") as f:
            jsonDict=json.load(f)
            jsonStr=json.dumps(jsonDict)
            soup = BeautifulSoup(jsonStr, "lxml")
            list=tokenize(ex(soup))
            dict=collections.Counter(list)
            #for i in dict:
            #    print(i)
            index(dict)
            print("FINISH "+str(dictTop))
        dictTop+=1

    #tokens = []
    #for text in textList:
    #    tokens.append(tokenize(text))

    #index(tokens)

def tokenize(str):
    symbol = [',', '.', '?', '!', '"', '(', ')', ':', ';', "'", '[', ']', "_", '*', '#', '{', '}','=','<','>','$','^','@','%','`','~','|','/','-']
    stops=['about','above','after','again','against','all','am','an','and','any','are','aret'
        ,'as','at','be','because','been','before','being','below','between','both','but','by'
        ,'cant','cannot','could','couldnt','did','didnt','do','does','doesnt','doing','dont'
        ,'down','during','each','for','few','from','further','had','hadnt','has','hasnt','have'
        ,'havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him'
        ,'himself','his','how','hows','i','id','ill','im','ive','if','in','into','is','isnt','it'
        ,'its','itself','lets','me','more','most','mustnt','my','myself','no','nor','not','of','off'
        ,'on','once','only','or','other','ought','our','ours','ourselves','out','over','own'
        ,'same','shant','she','shed','shell','shes','should','shouldnt','so','same','such'
        ,'than','that','thats','the','their','them','themselves','then','there','they','theyd'
        ,'theyll','theyre','theyve','this','those','through','to','too','under','until','up'
        ,'very','was','wasnt','we','wed','well','were','weve','were','werent','what','whats'
        ,'when','whens','where','wheres','which','while','who','whos','whom','why','whys','with'
        ,'wont','would','wouldnt','you','youd','youll','youre','youve','your','yours','yourself'
        ,'yourselves']

    str = str.lower()
    for sym in symbol:
        str = str.replace(sym, ' ')
    list = str.split(' ')
    list=[a for a in list if a!='']
    list=[i for i in list if len(i)<=14]                 #words longer than 14 unusual words
    list = [i for i in list if i.isnumeric()!=True]           # remove numeric
    list = [i for i in list if i not in stops]

    return  list

def index(dict):
    global dictTop
    az="abcdefzhijklmnopqrstuvwxyz"
    for token in dict:
        flag=0
        c=token[0]
        if c not in az:
            continue
        with open('words\\tfIndex\\'+c+'.txt', 'r', encoding="utf-8") as f:
            list = f.readlines()
            for i in range(len(list)):
                if token == list[i].split(',')[0].strip():
                    list[i] = list[i].strip() + ',' + str(dictTop) + ':' + str(
                        1 + math.log(dict[token], 10)) + '\n'  # 1+log(tf,10)
                    flag=1
                    with open('words\\tfIndex\\' + c + '.txt', 'w', encoding="utf-8") as w:
                        w.writelines(list)
                    break
            if flag == 0:
                list.append(token + ',' + str(dictTop) + ':' + str(1 + math.log(dict[token], 10)) + '\n')
                with open('words\\tfIndex\\' + c + '.txt', 'w', encoding="utf-8") as w:
                    w.writelines(list)



if __name__ == '__main__':
    root="C:\\Users\\RYO\\Downloads\\developer\\DEV"
    pathList = glob.glob(root + "\\*")
    for i in range(len(pathList)):
        findPath(pathList[i])
        print("successful "+str(i)+"\n")
    #print(pathList)