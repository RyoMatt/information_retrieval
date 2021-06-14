import glob
import math

def idfIndex(pathList):
    N=55393
    for path in pathList:
        with open(path, "r", encoding="utf-8") as f:
            list=f.readlines()
        for i in list:
            w=i.split(',')
            df=len(w)-1
            idf=math.log(N/df,10)

            c=path[-5]
            with open('words\\idfIndex\\' + c + '.txt', 'a', encoding="utf-8") as f:
                f.write(w[0]+':'+str(idf)+'\n')

def wtdIndex():
    root = "words\\tfIndex\\*"
    filePath1 = glob.glob(root)
    root = "words\\idfIndex\\*"
    filePath2 = glob.glob(root)



if __name__ == '__main__':
    root="words\\tfIndex\\*"
    filePath = glob.glob(root)
    idfIndex(filePath)
    #wtdIndex()