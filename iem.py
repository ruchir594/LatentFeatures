import re
import json
def getWords(data):
    return re.compile('\w+').findall(data)

with open('data/output_pos.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
a=getWords(data)
b=[] # b has all the tagger output
for i in range(len(a)):
    b.append(a[i].split('_'))
#print b
q=[] #q has dependencies
with open('data/output_dep.txt','r') as myfile2:
    p=myfile2.readlines()
for i in range(len(p)):
    if p[i][0] != ' ' and p[i][0] != '(' and p[i] != '\n':
        q.append(re.findall(r"[\w':]+", p[i]))
print len(p), len(q)
#pre processing
allvb=[]
vbdump=[]
allnn=[]
nndump=[]
for i in range(len(b)):
    if b[i][1] == "NN" or b[i][1] == "NNP":
        if b[i][0] not in nndump:
            nndump.append(b[i][0])
            allnn.append(b[i][0])
    if b[i][1] == "VBN" or b[i][1] == "VBZ" or b[i][1] == "VBG" or b[i][1] == "VB":
        if b[i][0] not in vbdump:
            vbdump.append(b[i][0])
            allvb.append(b[i][0])
#print allvb
#print allnn
print " "
# Now q only has dependencies....
dlist=['nmod:poss','nsubjpass','amod','nsubj','compound']
ie=[]
#print q
#for i in range(len(q)):
#    if q[i][0] in dlist:
bdump=[]
qsave=[]
for i in range(len(q)):
    if q[i][0] in dlist:
        ie.append((q[i][1] + "_" + q[i][3]).split('_'))

bdump=[]
for i in range(len(allnn)):
    #print allnn[i]
    #print " "
    for j in range(len(q)):
        #print q[j]
        #print " "
        if allnn[i] == q[j][1] and q[j][3] in allvb:
            for k in range(len(q)):
                #print q[k]
                if j!=k and q[j][3] == q[k][3] and q[k][1] in allnn:
                    ie.append((q[j][1] + "_" + q[k][3] + "_"  +  q[k][1]).split('_'))
                if j!=k and q[j][3] == q[k][1] and q[k][3] in allnn:
                    ie.append((q[j][1] + "_" + q[k][1] + "_"  +  q[k][3]).split('_'))
        if allnn[i] == q[j][3] and q[j][1] in allvb:
            for k in range(len(q)):
                #print q[k]
                if j!=k and q[j][1] == q[k][3] and q[k][1] in allnn:
                    ie.append((q[j][3] + "_" + q[k][3] + "_"  + q[k][1]).split('_'))
                if j!=k and q[j][1] == q[k][1] and q[k][3] in allnn:
                    ie.append((q[j][3] + "_" + q[k][1] + "_"  +  q[k][3]).split('_'))

print " "
print ie
print " "
info={}
for i in range(len(ie)):
    if ie[i][0] in allnn:
        if info.has_key(ie[i][0])==True:
            if ie[i][1] not in info[ie[i][0]]:
                info[ie[i][0]].append(ie[i][1])
        else:
            info.setdefault(ie[i][0],[])
            info[ie[i][0]].append(ie[i][1])
    if ie[i][1] in allnn:
        if info.has_key(ie[i][1])==True:
            if ie[i][0] not in info[ie[i][1]]:
                info[ie[i][1]].append(ie[i][0])
        else:
            info.setdefault(ie[i][1],[])
            info[ie[i][1]].append(ie[i][0])
for i in range(len(info)):
    print info.items()[i]
json.dump(info, open("data/ie.txt",'w'))
