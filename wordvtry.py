import re
import json
import pickle
import word2vec
from scipy import spatial

def getWords(data):
    return re.compile('\w+').findall(data)

with open('./Ext-RESCAL/mall/triplet_review.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
a=getWords(data)

with open('./Ext-RESCAL/mall/words','r') as myfile2:
    q=myfile2.readlines()
#print q[0][:-1]
#print q[1][:-1]
model = word2vec.load('./text8.bin')
clusters = word2vec.load_clusters('./text8-clusters.txt')

wordv=[]
print len(q)
for i in range(len(q)):
    #print i
    wordv.append(model[str(q[i][:-1]).lower()])

simil=[]

for i in range(len(q)):
    simil.append([])
    for j in range(len(q)):
        simil[i].append(1 - spatial.distance.cosine(wordv[i], wordv[j]))

#print simil
clustt=[]
alreadyin=[]
for i in range(len(simil)):
    temp=[x for x in simil[i] if x>0.5]
    clustt.append([])
    #print temp
    for j in range(len(temp)):
        tempin=simil[i].index(temp[j])
        if tempin not in alreadyin:
            alreadyin.append(tempin)
            clustt[i].append(tempin)

print len(alreadyin)
print alreadyin
print len(clustt)
print clustt


for i in range(len(clustt)):
    for j in range(len(clustt[i])):
        k=0
        while k<len(a):
            if a[k+1] == q[clustt[i][j]][:-1]:
                a[k+1] = "vec_rel_"+"%d" %i
            k=k+3
print a

temp=0
for i in range(len(clustt)):
    if clustt[i] != []:
        temp=temp+1
print temp
