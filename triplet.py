import re
import json
import pickle
import word2vec
from scipy import spatial

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
allother=[]
allotherdump=[]
for i in range(len(b)):
    print i
    print b[i]
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
#for i in range(len(q)):#
#    if q[i][0] in dlist:
#        ie.append((q[i][1] + "_" + q[i][3]).split('_'))

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


#model = word2vec.load('./text8.bin')
#clusters = word2vec.load_clusters('./text8-clusters.txt')

#wordv=[]

#for i in range(len(ie)):
#    wordv.append(model[ie[i][1]])

#simil=[]

#for i in range(len(ie)):
#    simil.append([])
#    for j in range(len(ie)):
#        simil[i].append(1 - spatial.distance.cosine(wordv[i], wordv[j]))

#print


model = word2vec.load('./text8.bin')
clusters = word2vec.load_clusters('./text8-clusters.txt')

wordv=[]
print len(allvb)
for i in range(len(allvb)):
    #print i
    wordv.append(model[str(allvb[i]).lower()])

simil=[]

for i in range(len(allvb)):
    simil.append([])
    for j in range(len(allvb)):
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
clustt = [x for x in clustt if x != []]
print len(alreadyin)
print alreadyin
print len(clustt)
print clustt
json.dump(allvb, open("Ext-RESCAL/mall-help/allvb.txt",'w'))
json.dump(simil, open("Ext-RESCAL/mall-help/simil.txt",'w'))
json.dump(clustt, open("Ext-RESCAL/mall-help/clustt.txt",'w'))
json.dump(str(wordv), open("Ext-RESCAL/mall-help/wordv.txt",'w'))
#f_e_wv = open("Ext-RESCAL/mall-help/wordv.txt",'a+')
#for i in range(len(wordv)):
#    f_e_wv.write(wordv[i])

allvb_new=[]
f_words = open("Ext-RESCAL/mall/words", 'a+')
#z=0
for i in range(len(clustt)):
    flag=0
    for j in range(len(clustt[i])):
        k=0
        while k<len(ie):
            if ie[k][1] == allvb[clustt[i][j]]:
                ie[k][1] = "vec_rel_"+"%d" %i
                flag=1
            k=k+1
    if flag==1:
        f_words.write(str("vec_rel_"+"%d" %i)+'\n')
        allvb_new.append(str("vec_rel_"+"%d" %i))
        #z=z+1

print ie
json.dump(allvb_new, open("Ext-RESCAL/mall-help/allvb_new.txt",'w'))
json.dump(ie, open("Ext-RESCAL/mall/triplet_all_plot.txt",'w'))
f_e_ids = open("Ext-RESCAL/mall/entity-ids",'a+')
for each_nn in allnn:
    f_e_ids.write(str(each_nn)+'\n')


for i in range(len(allvb_new)):
    for j in range(len(ie)):
        if allvb_new[i] == ie[j][1]:
            f_temp = open("Ext-RESCAL/mall/%d-rows" %i, 'a+')
            f_temp.write('%d' %[k for k,x in enumerate(allnn) if x == ie[j][0]][0])
            f_temp.write(" ")
            f_temp = open("Ext-RESCAL/mall/%d-cols" %i, 'a+')
            f_temp.write('%d' %[k for k,x in enumerate(allnn) if x == ie[j][2]][0])
            f_temp.write(" ")
