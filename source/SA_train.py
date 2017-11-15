import random
import numpy
fd1 = open('salmon_train.txt','r')
salmon_t = fd1.readlines()
fd1.close()
salmon = []
#-------------------------------------------------------
#SA원래 알고리즘대로 랜덤하게 학습을 해도 오류율이 8%까지 나오긴하나 49%도 종종 나오게된다.
#그래서 한쪽으로 치우치는 값이 100번나오게되면 조금씩 조정을 해주어서 일정한 오류율을 가지는 파라미터값을 구할 수 있도록 했다
#-------------------------------------------------------

#salmon txt파일을 줄단위로 읽는다
for line in salmon_t:
    a=line.split()
    salmon.append([float(a[0]),float(a[1])])

fd2 = open('seabass_train.txt','r')
seabass_t = fd2.readlines()
fd2.close()
seabass = []

#seabass txt파일을 줄단위로 읽는다
for line in seabass_t:
    a=line.split()
    seabass.append([float(a[0]),float(a[1])])

#출력결과를 저장하기 위한 txt파일을 연다
fd3 = open('train_log_1.txt','w')

#초기 parameter값을 지정
parameter = [[2.0,-1.0,-180.0]]

#error율 계산
def errorEval(para):
    count = 0
    for i in range(0,50):
        if (para[0]*salmon[i][0]+para[1]*salmon[i][1]+para[2])>0:
            #salmon 분류 실패
            count +=1
        if (para[0]*seabass[i][0]+para[1]*seabass[i][1]+para[2])<0:
            #seabass 분류 실패
            count +=1
    #분류 실패한 수를 세서 반환        
    return count
    
#Simulated annealing
def SA():
    
    #알고리즘에 사용할 변수 초기화
    #초기 parameter로 에러값 측정
    E_old=errorEval(parameter[0])
    
    E = 0
    E_new = 0
    index = 0
    T = 100
    wrongcount = 0
    sosocount = 0
    
    rand_a = -10.0
    rand_a1 = 10.0
    e_low = [0,0,0]
    e_lowrate = 0
    while T>0.001:
        current = parameter[index]
        
       #탐색지점을 현재 위치에서 인접한 곳 중 랜덤으로 선택한다
        temp = [current[0]+random.uniform(-0.01,0.01),current[1]+random.uniform(-0.01,0.01),current[2]+random.uniform(rand_a,rand_a1)]
        
       #탐색지점의 오류 E계산
        E_new=errorEval(temp)
        
       #에러율이 50이라는 뜻은 아무것도 판변을 성공하지 못한 채 판별선이 한쪽끝으로 몰려있다는 의미이다
       #그래서 한쪽끝으로 몰려있는 수를 세다가 100이 넘으면 랜던값을 조정해준다
        if E_new == 50:
            wrongcount += 1
            if(wrongcount > 100):
                #만약 오른쪽끝으로 몰려있으면 랜덤값이 왼쪽으로 평행이동할 수 있도록 c parameter값의 랜덤시드에 조정을 해준다
                if(-temp[2] > 100):
                    rand_a1 = 10.0
                    rand_a=0
                    wrongcount = 0
                #반대로 왼쪽끝에 몰려있을 경우엔 오른쪽으로 평행이동할 수 있도록 랜덤시드를 조정해준다
                else:
                    rand_a = -10.0
                    rand_a1=0
                    wrongcount = 0
        #위에서 한쪽으로 몰려있는경우에 원하는 방향으로 갈 수 있도록 랜덤값을 조정해줬기때문에 반대로 한쪽끝으로 몰려있지 않은경우도 카운트해서 다시 랜덤하게 움직일 수 있도록 조정해준다
        #즉, 위에서 조정한 값이 계속 유지되지 않도록 다시 랜덤을 조정
        else:
            sosocount +=1
            if(sosocount > 100):
                rand_a = -10.0
                rand_a1= 10.0
                sosocount = 0
                
       #현재 위치와의 오류 차이
        E = E_new - E_old
        if(E_new<E_old):
            e_low=temp
            e_lowrate=E_new
        
       #조정된 랜덤값이 더 좋으면 parameter에 더해준다
        if E <= 0:
            parameter.append(temp)
            index +=1
       #조정된 값이 안좋은 경우에도 랜덤하게 그 값을 선택한다
        else:
            r = random.uniform(0,1)
            if r < numpy.exp(-E/T):
                parameter.append(temp)
                index +=1
        
        T = 0.999*T
        E_old = E_new
        fd3.write('%s%d%s%f%s' %('T = ',T,'    error rate',E_old*0.01,'\n'))
        print '%s%d%s%f' %('T = ',T,'    error rate',E_old*0.01)
    print e_lowrate*0.01
    fd3.write( '%s%f' % ('low error :  ',e_lowrate*0.01))
    return e_low
        
print 'Classify fish train'
g_para=SA()
fd3.write('%s %f%f%f%s' %('train parameter',g_para[0],g_para[1],g_para[2],'\n'))
fd3.close()
print '%s %f%f%f' %('train parameter',g_para[0],g_para[1],g_para[2])
