import threading
x=0
def increament():
    global x
    x+=1

def task_tread(lock):
    for _ in range(10000):
        # print('Call : ',j)
        lock.acquire()
        increament()
        lock.release()
               
def main_fun():
    global x
    x=0
    lock=threading.Lock()
    t1=threading.Thread(target=task_tread,args=(lock,))
    t2=threading.Thread(target=task_tread,args=(lock,))
    t3=threading.Thread(target=task_tread,args=(lock,))
    t4=threading.Thread(target=task_tread,args=(lock,))

    # t1=threading.Thread(target=task_tread)
    # t2=threading.Thread(target=task_tread)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()   



def second_fun():
    print("hetyyyy")
    import time
    a=[]
    b=[]
    # x=0
    for i in range(10):
        main_fun()
        a.append(i)
        b.append(x)
    # print(a,b)
    data=dict(zip(a,b))
    # print(data)
    return {"DATA":data}

