import word2vec
from scipy import spatial

model = word2vec.load('./text8.bin')
clusters = word2vec.load_clusters('./text8-clusters.txt')
print clusters['dog']
indexes, metrics = model.cosine('kidnapped')
print model.vocab[indexes]
indexes, metrics = model.cosine('wounded')
print model.vocab[indexes]
a=model['kidnapped']
b=model['wounded']
print a, b
result = 1 - spatial.distance.cosine(a, b)
print result
