import csv
import numpy
import math
import re
def sigmoid(x):
  return 1 / (1 + math.exp(-x))
def getWords(data):
    return re.compile('\w+').findall(data)


n_of_latent_feat=5
n_of_relations=15
n_of_entities=39
e_s=[] #Latent Features of each entiry
r_s=[] #Weight Matrix for each Relation
w_s=[]
k=0 #number of relations
i=0
with open('./m1/entity.embeddings.csv', 'rU') as f:
    f1 = csv.reader(f, delimiter= ' ')
    for f11 in f1:
        e_s.append(f11)
#print e[0]
e=numpy.array(e_s)
e=e.astype(numpy.float)
et=e.transpose()
print e.shape
print et.shape
#print e[4]
with open('./m1/latent.factors.csv', 'rU') as fd:
    f2 = csv.reader(fd, delimiter= ' ')
    for f22 in f2:
        r_s.append(f22)
#print r[9]
r=numpy.array(r_s)
r=r.astype(numpy.float)
print r.shape
while k < n_of_relations:
    w_s.append([])
    for j in range(n_of_latent_feat):
        w_s[k].append(r_s[i])
        i=i+1
    k=k+1
w=numpy.array(w_s)
w=w.astype(numpy.float)
print w.shape
print w[0].shape

y=numpy.zeros((n_of_relations, n_of_entities, n_of_entities))
print y.shape
for i in range(n_of_relations):
    temp = numpy.dot(e, w[i])
    y[i] = numpy.dot(temp, et)
print y.shape
for i in range(15):
    for j in range(39):
        for k in range(39):
            if y[i][j][k] != 0:
                #print i,j,k, y[i][j][k]
                a1=1


with open('./mall-help/allvb_new.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
allvb_new=getWords(data)

with open('./mall-help/allvb.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
allvb=getWords(data)

with open('./mall-help/clustt.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
clustt=getWords(data)

with open('./mall/entity-ids','r') as myfile2:
    p=myfile2.readlines()
print p

with open('./m2/triplet.txt','r') as myfile:
    data=myfile.read().replace('\n', '')
a=getWords(data)

print " "


print " "

print a

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

#print "spock - playedin - startrek"
#print y[0][0][2]
#print sigmoid(y[0][0][2])
#print "spock - playedin - guiness"
#print sigmoid(y[0][0][6])
#print "startrek(2) - genre (3) - scifi (4)"
#print y[3][2][4]
#print sigmoid(y[3][2][4])
#print "obi chatin startrek"
#print y[2][5][2]
#print sigmoid(y[3][2][4])
#print "obi charin starwars"
#print y[2][5][3]
#print sigmoid(y[3][2][4])
