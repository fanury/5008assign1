#!/usr/bin/env python
# coding: utf-8

# In[1]:


#从input中读取文件
def readtxt(filename):
    f = open(filename)               # 返回一个文件对象 
    #读取第一行
    line = f.readline() 
    for i in line:
        if i=='\n':
            break
        nodesnumber=int(i)
    a=[]
    line = f.readline() 
    while line:
        l1=[]
        for i in line:
            if i=='\n':
                break
            elif i==' ':
                continue
            else:
                l1.append(int(i))
        a.append(l1)
        line = f.readline() 
    return a,nodesnumber


# In[2]:


#统计所有连通图的个数
def graphs(num,nodesnumber):
    graph=[]
    usednodes=[]
    #当不是所有的点都使用过时
    while len(usednodes)!=nodesnumber:
        #找到没有使用过的第一个点i
        for i in range(nodesnumber):
            if i not in usednodes:
                usednodes.append(i)
                g=[i]
                node=[i]
                break
        #如果node中还有节点 则计算与node中相连的节点 并加入到node中
        while len(node)!=0:
            node1=node.pop()
            for i in range(nodesnumber):
                if num[node1][i]==1:
                    if i not in usednodes:
                        node.append(i)
                        g.append(i)
                        usednodes.append(i)
        graph.append(g)
    return graph                   


# In[3]:


#计算与start节点开始的所有点的最短距离 
#修改  处理了有断开图的情况 如果node中没有节点 则直接停止 
#这样即使有多个连通图，在循环每一个点的时候就会分别把每个连通图都遍历到
def countshortestdistence(start,a,nodesnumber):
#初始点为的距离为0，用字典layn来记录
    layn={0:[start]}
    #用来计算的栈
    node=[start]
    #已经计算过的点
    usednode=[start]
    laynum=0
    #计算关于每个点的最小距离字典
    #input：节点个数
    while len(usednode)!=nodesnumber:
        laynum+=1
            #加入到距离字典
        #如果node中没有节点了 则break
        if len(node)==0:
            break
        layn[laynum]=[]
        for i in node:
                #找出与第i个点有连接的点
            for j in range(nodesnumber):
                if a[i][j]==1:
                        #如果该点未被计算过距离
                    if j not in usednode:
                        layn[laynum].append(j)
                        usednode.append(j)
                
        node.remove(i)
        node.extend(layn[laynum])                    
    return layn
#输出layn：离初始点最短距离的字典


# In[4]:


#计算最短距离数
#input ： start: 输入的节点数  disnum：计算出从start开始到其余各点到最短路径的数量
def shortestpathnum(layn,start):
    disnum={start:1}
    l1=list(layn.values())
    for i in range(1,len(l1)):
        #对于每一层的的节点数
        for j in l1[i]:
            #对于上一层的每个节点
            num=0
            for k in l1[i-1]:
                if a[j][k]==1:
                    num=num+disnum[k]
            disnum[j]=num
    return disnum
                


# In[5]:


#计算从start节点开始的betweeness值
def startbetweeness(disnum,layn,nodesnumber):
    edge={}
    #先将存在的边记录下来
    for i in range(nodesnumber):
        for j in range(i,nodesnumber):
            if a[i][j]==1:
                edge[(i,j)]=0
    #通过dege字典和disnum最短路径数计算出betweeness值
    #通过最短路径就可以只求与start在同一个连通图里的betweeness
    #在遍历所有点之后可以将不同连通图对应的betweeness都求出来
    laykey=sorted(layn.keys(),reverse=True)
    #对最远距离的点赋值 i为最远距离点
    for i in layn[laykey[0]]:
        #用一个list记录所有与该点相连的边
        farsetlist=[]
        for j in layn[laykey[1]]:#j为与最远距离点相连的点
            if (i,j) in edge:
                edge[(i,j)]=disnum[j]/disnum[i]
            if (j,i) in edge:
                edge[(j,i)]=disnum[j]/disnum[i]  
    #对于剩下的层数 根据前面统计出的层数进行相加:
    #i为到start点的距离
    for i in laykey[1:-1]:
        #j为距离为i的点
        for j in layn[i]:
            #计算j的子节点的值的和
            num=0
            for k in layn[i+1]:
                if (j,k) in edge:
                    num+=edge[(j,k)]
                if (k,j) in edge:
                    num+=edge[(k,j)]
            num+=1
            #计算到父节点的边的值
            for k in layn[i-1]:
                if (j,k) in edge:
                    edge[(j,k)]=disnum[k]/disnum[j]*num
                if (k,j) in edge:
                    edge[(k,j)]=disnum[k]/disnum[j]*num
    return edge

        


# In[6]:


#遍历所有节点得到总的betweeness值
def betweeness(a,nodesnumber):
    betweeness={}
    #从每一个start开始 计算所有的betweeness
    #graph=graphs(a,nodesnumber)  
    for i in range(nodesnumber):
        start=i
        layn=countshortestdistence(start,a,nodesnumber)
        disnum=shortestpathnum(layn,start)
        edge=startbetweeness(disnum,layn,nodesnumber)
        betweeness[i]=edge
    edge={}
    for i in range(nodesnumber):
        for j in range(i,nodesnumber):
            if a[i][j]==1:
                edge[(i,j)]=0
    for value in betweeness.values():
        for key1 in list(value.keys()):
            edge[key1]+=value[key1]
    for key in list(edge.keys()):
        edge[key]/=2
    return edge


# In[7]:


#节点的度
def nodedegree(a,i):
    n=0
    for j in a[i]:
        if j==1:
            n+=1
    return n

#计算整个图的modularity
def modularity(a,b,nodesnumber):
    #计算所有的边数量
    edgenum=0
    for i in range(nodesnumber):
        for j in range(i,nodesnumber):
            if b[i][j]==1:
                edgenum+=1
    #print(edgenum)
    #统计社区数量
    graph=graphs(a,nodesnumber)
    #对每个社区
    cn=0
    for g in graph:
        #对社区中的每一个元素
        for i in g:
            for j in g:
                aij=b[i][j]
                ki=nodedegree(b,i)
                kj=nodedegree(b,j)
                #print(i,j,aij,ki,kj,aij-ki*kj/(2*edgenum))
                cn+=aij-ki*kj/(2*edgenum)
    cn=cn/(2*edgenum)
    return cn


# In[8]:


a,nodesnumber=readtxt('input.txt')
b,nodesnumber=readtxt('input.txt')

graphnum=0
firstpart=[]
secondpart={}
while len(graphs(a,len(a)))!=len(a):
    nodesnumber=len(a)
    edge=betweeness(a,nodesnumber)
    m=max(edge.values())
    for key in list(edge.keys()):
        #断开所有betweeness最大的值的边
        if edge[key]==m:
            a[key[0]][key[1]],a[key[1]][key[0]]=0,0
    graph=graphs(a,nodesnumber)
    if len(graph)!=graphnum:
        graphnum=len(graphs(a,nodesnumber))
        firstpart.append(tuple(graphs(a,nodesnumber)))
        secondpart[len(graphs(a,nodesnumber))]=[modularity(a,b,nodesnumber)]
        secondpart[len(graphs(a,nodesnumber))].append(tuple(graphs(a,nodesnumber)))
#first part output
print("network decomposition:")
for i in firstpart:
    print(i)
#second part output
for key,value in secondpart.items():
    print("%d clusters: modularity %f"%(key,value[0]))
#optimal structure
print("optimal structure: ",end='')
print(secondpart[max(secondpart,key=secondpart.get)][1])


# In[ ]:




