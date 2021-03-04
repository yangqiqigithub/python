from multiprocessing import Queue

q=Queue(3)  #指定队列的长度为3 规定了能放几个就能放几个，多放就会卡主

#往队列里放东西 放啥都可以
q.put('first')
q.put('second')
q.put('third')

print(q.get())
print(q.get())
print(q.get())


q.put('fouth')
print(q.get())


