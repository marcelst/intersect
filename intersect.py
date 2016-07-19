import time


# coding: utf-8

# In[1]:

import mmh3,itertools,bisect,sys

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


# In[273]:
size=80000
ratio=float(sys.argv[1])
sparse = sorted([mmh3.hash(str(x)) for x in range(0,size)])[0:size]


# In[285]:

dense = sorted([mmh3.hash(str(x)) for x in range(0,int(size/ratio))])[0:len(sparse)]


# In[286]:

distances_sparse = [y-x for x, y in pairwise(sparse)]


# In[287]:

distances_dense = [y-x for x, y in pairwise(dense)]


# In[288]:

avg_distance_sparse = sum(distances_sparse)/float(len(distances_sparse))


# In[289]:

avg_distance_dense = sum(distances_dense)/float(len(distances_dense))


# In[290]:

avg_distance_sparse, avg_distance_dense


# In[291]:


i=0;j=0;loop=0
intersection=[]
start = time.time()
while i<len(dense) and j<len(sparse):
  loop+=1
  if dense[i] < sparse[j]:
      i+=1
  elif dense[i] > sparse[j]:
      j+=1
  else:
      intersection.append(dense[i])
      i+=1
      j+=1
linear=loop
linear_time=time.time()-start
# In[292]:

len(intersection) == len(set(dense).intersection(set(sparse)))


# In[293]:

idx=1
estimated_index=int((sparse[idx]-dense[idx-1])/avg_distance_dense-1)
dense[estimated_index]-sparse[idx]


# In[294]:

import sys;
def binary_search(a, x, lo=0, hi=None):
    count = 0;
    if hi is None:
        hi = len(a)
    while lo < hi:
        count+=1
        mid = (lo+hi)//2
        midval = a[mid]
        if midval < x:
            lo = mid+1
        elif midval > x: 
            hi = mid
        else:
            return count,mid
    return count, hi
   
i=0;j=0;loop=0;saves=0
intersection=[]
bin_search=[]
start=time.time()
while i<len(dense) and j<len(sparse):
    loop+=1
    if dense[i] < sparse[j]:
        estimated_index_distance=max(1,int((sparse[j]-dense[i])/float(avg_distance_dense)))

        assert estimated_index_distance >= 1
        # find the last index i where dense[i] < sparse[j]
        (c, insertion_point) = binary_search(dense, sparse[j], i+1, min(len(dense),int(i+estimated_index_distance*2)))
        bin_search.append(c)
        loop+=c
        assert dense[insertion_point-1] <= sparse[j]
    #    assert dense[insertion_point+1] >= sparse[j]
        saves+=insertion_point-i-1
            
        assert insertion_point > i
        i=max(i+1,insertion_point-1)
     #   break
    elif dense[i] > sparse[j]:
        j+=1
    else:
        intersection.append(dense[i])
        i+=1
        j+=1
binary_time=time.time()-start

# In[295]:

sorted(list(set(dense).intersection(set(sparse)))) == intersection, len(intersection), len(set(dense).intersection(set(sparse)))


# In[ ]:
binary=loop


print ratio,linear,binary,linear_time, binary_time

# In[ ]:



