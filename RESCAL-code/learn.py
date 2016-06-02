import csv
import numpy
import math
import re
import word2vec
from scipy import spatial
def sigmoid(x):
  return 1 / (1 + math.exp(-x))
def getWords(data):
    return re.compile('\w+').findall(data)




#with open('./mall-help/clustt.txt','r') as myfile:
#    data=myfile.read().replace('\n', '')
#clustt=getWords(data)

with open('./tiny-example/words','r') as myfile2:
    q=myfile2.readlines()


with open('./tiny-example/entity-ids','r') as myfile2:
    p=myfile2.readlines()

for i in range(len(p)):
    p[i]=p[i][:-1]
for i in range(len(q)):
    q[i]=q[i][:-1]

with open('./tiny-example/triplet_review.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
a=getWords(data)

print " "

print a,"\n"

n_of_latent_feat=2
n_of_relations=3
n_of_entities=4

e_s=[] #Latent Features of each entiry
r_s=[] #Weight Matrix for each Relation
w_s=[]
k=0 #number of relations
i=0
with open('entity.embeddings.csv', 'rU') as f:
    f1 = csv.reader(f, delimiter= ' ')
    for f11 in f1:
        e_s.append(f11)
#print e[0]
e=numpy.array(e_s)
e=e.astype(numpy.float)
et=e.transpose()
print "e_shae",e.shape
print et.shape
#print e[4]
with open('latent.factors.csv', 'rU') as fd:
    f2 = csv.reader(fd, delimiter= ' ')
    for f22 in f2:
        r_s.append(f22)
#print r[9]
r=numpy.array(r_s)
r=r.astype(numpy.float)
rt=r.transpose()
print "r shape",r.shape
while k < n_of_relations:
    w_s.append([])
    for j in range(n_of_latent_feat):
        w_s[k].append(r_s[i])
        i=i+1
    k=k+1
w=numpy.array(w_s)
w=w.astype(numpy.float)
print "w shape",w.shape
print w[0].shape

y=numpy.zeros((n_of_relations, n_of_entities, n_of_entities))
print y.shape
for i in range(n_of_relations):
    temp = numpy.dot(e, w[i])
    y[i] = numpy.dot(temp, et)
print "y shape",y.shape

#print y

count=0
for i in range(n_of_relations):
    for j in range(n_of_entities):
        for k in range(n_of_entities):
            if y[i][j][k] != 0:
                count=count+1
print "total values", n_of_entities*n_of_entities*n_of_relations
print "number of non zero values",count
i=0
while i<len(a):
    print i
    print a[i], a[i+1], a[i+2]
    if a[i+1] in q:
        ind1=q.index(a[i+1])
    else:
        i=i+3
        continue;
    if a[i] in p:
        ind2=p.index(a[i])
    else:
        i=i+3
        continue;
    if a[i+2] in p:
        ind3=p.index(a[i+2])
    else:
        i=i+3
        continue;
    print y[ind1][ind2][ind3]
    print sigmoid(y[ind1][ind2][ind3])
    i=i+3
print y
