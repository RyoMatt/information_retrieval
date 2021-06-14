import sys
import collections
import time
import math

def tokenize(str):
    symbol = [',', '.', '?', '!', '"', '(', ')', ':', ';', "'", '[', ']', "_", '*', '#', '{', '}','=','<','>','$','^','@','%','`','~','|','/','-']
    stops=['a','about','above','after','again','against','all','am','an','and','any','are','aret'
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

def engine(inputList):
    wt = collections.Counter(inputList)
    inputList=[]
    for key in wt:
        inputList.append(key)
    print(inputList)

    docList=[]
    idfValues=[]
    for q in inputList:
        c=q[0]
        with open('words\\idfIndex\\' + c + '.txt', 'r', encoding="utf-8") as f:
            idf=f.readlines()
            for word in idf:
                v=word.split(':')
                if v[0]==q:
                    idfValues.append(float(v[1].strip()))
                    break
        with open('words\\tfIndex\\' + c + '.txt', 'r', encoding="utf-8") as f:
            index=f.readlines()
            for word in index:
                t=word.split(',')
                if q == t[0]:
                    dict={}
                    list=word[word.find(',')+1:].strip().split(',')
                    for d in list:
                        temp=d.split(':')
                        dict[int(temp[0])]=float(temp[1])
                    docList.append(dict)
                    break
    if len(docList)==0:
        print("No result")
        return 0

    if len(docList)==1:
        d=docList[0]
        result = sorted(d.items(), key=lambda x:x[1], reverse=True)
        #print(result)
        printUrl(result)
        return 0

    list1=[]
    c=1
    docList=sorted(docList,key=len)
    """
    for i in docList:
        print(len(i))
    """
    for doc in docList[0]:
        for i in range(1,len(docList)):
            if doc in docList[i]:
                c+=1
        if c==len(docList):
            list1.append(doc)
        c=1
    #print(docList, list1)
    docList=weightList(docList,idfValues)
    result=score(docList,list1)
    if len(result) == 0:
        print("No result")
        return inputList
    printUrl(result)
    return 0

def weightList(docList, idf):
    wdList=[]
    for i in range(len(docList)):
        dict = {}
        for key in docList[i]:
            dict[key]=docList[i][key]*idf[i]
        wdList.append(dict)
    return wdList

def score(docList,list1):
    #print(len(list))
    dict={}
    for i in range(len(list1)):
        dict[list1[i]]=0
    for i in range(len(list1)):
        den=0
        for doc in docList:
            dict[list1[i]]+=doc[list1[i]]
            den+=math.pow(doc[list1[i]],2)
        den=math.log(den,10)
        dict[list1[i]]/=den
            #print(dict)

    result = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    #print(result)
    return result

def printUrl(result):
    count=1
    with open('url.txt', 'r', encoding="utf-8") as f:
        l=f.readlines()
        for i in result:
            if count>5:
                break
            #print(i)
            url=l[i[0]][l[i[0]].find(',')+1:].strip()
            print(str(count)+'. '+url)
            count+=1

if __name__ == '__main__':
    while True:
        print("Enter 'endSearch' to exit")
        print("Enter: ", end='')
        inp = input()
        if inp=='endSearch':
            break
        start_time = time.time()
        inputList=tokenize(inp)
        while True:
            returnList=engine(inputList)
            if returnList == 0:
                break
            returnList.pop(-1)
            inputList=[]
            inputList=returnList
        print()
        print("--- %s milliseconds ---" % ((time.time() - start_time) * 1000))
