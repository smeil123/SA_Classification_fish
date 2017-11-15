import matplotlib.pyplot as plt
import numpy as np

#salmon txt파일 오픈
fd1 = open('salmon_test.txt','r')
salmon_t = fd1.readlines()
fd1.close()
    
#seabass txt파일 오픈
fd2 = open('seabass_test.txt','r')
seabass_t = fd2.readlines()
fd2.close()
   
#출력값 저장하기위한 txt파일 오픈
fd3 = open('test_output.txt','w')

salmon = []
c_salmon = []
m_salmon = []

seabass = []
c_seabass = []
m_seabass = []

#train을 통해 학습한 prameter값을 세팅
parameter = [2.450267,-1.307926,-179.750256]  
x_coefficient = -(parameter[0]/parameter[1])
x_constant =(parameter[2]/parameter[1])

#읽어들인 txt파일을 줄단위로 읽어들여서 list에 저장한다    
for line in salmon_t:
    a=line.split()
    salmon.append([float(a[0]),float(a[1])])

for line in seabass_t:
    a=line.split()
    seabass.append([float(a[0]),float(a[1])])
 
print 'Classify fish train'

#분류시작 ,출력값을 출력하고 txt파일에 적는다
#이때, 그림으로 분류성공과 분류실패를 나타내기위해서 성공했을때와 실패했을때를 분류해서 list에 저장해둔다
for i in range(0,50):
    if (parameter[0]*salmon[i][0]+parameter[1]*salmon[i][1]+parameter[2])>0:
        #분류실패
        print '%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  fail')
        fd3.write('%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  fail\n'))
        m_salmon.append(salmon[i])
    else:
        #분류성공
        print '%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  correct')
        fd3.write('%s%d%s%d%s' %('salmon =',salmon[i][0],', ',salmon[i][1],' =>  correct\n'))
        c_salmon.append(salmon[i])
        
for i in range(0,50):        
    if (parameter[0]*seabass[i][0]+parameter[1]*seabass[i][1]+parameter[2])<0:
        #분류실패
        print '%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  fail')
        fd3.write('%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  fail\n'))
        m_seabass.append(seabass[i])
    else:
        #분류성공
        print '%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  correct')
        fd3.write('%s%d%s%d%s' %('seabass =',seabass[i][0],', ',seabass[i][1],' =>  correct\n'))
        c_seabass.append(seabass[i])

#위에서 계산한 결과로 error율을 저장해둔다
errorrate = (len(m_salmon)+len(m_seabass))*0.01
fd3.write('%s%f' % ('errorrate => ',errorrate))

if __name__ == '__main__':
    fig, ax = plt.subplots()
    
    xList = []
    yList = []
    
    #분류성공한 salmon은 초록색삼각형으로 그린다
    for data in c_salmon:
        x,y = data
        xList.append(x)
        yList.append(y)
    ax.plot(xList,yList,'g^',Label='salmon')
    
    xList = []
    yList = []
    
    #분류성공한 seabass는 노란색사각형으로 그린다
    for data in c_seabass:
        x,y = data
        xList.append(x)
        yList.append(y)
    ax.plot(xList,yList,'ys',Label='seabass')
    
    xList = []
    yList = []
    
    #분류실패한 salmon은 빨간색삼각형으로 그린다
    for data in m_salmon:
        x,y = data
        xList.append(x)
        yList.append(y)
    ax.plot(xList,yList,'r^',Label='salmon')
    
    xList = []
    yList = []
    
    #분류실패한 seabass는 빨간색사각형으로 그린다
    for data in m_seabass:
        x,y = data
        xList.append(x)
        yList.append(y)
    ax.plot(xList,yList,'rs',Label='seabass')
    
    ax.grid(True)
    ax.legend(loc='upper right')
    ax.set_xlabel('Length of body')
    ax.set_ylabel('Length of tail')
    ax.set_xlim((None,None))
    ax.set_ylim((None,None))
    
    #분류자를 빨간색 점선으로 그린다
    a = np.arange(0.0,120.0,0.01)
    ax.plot(a,x_coefficient*a-x_constant,'r--')
    
    plt.savefig('test_output.png')
    plt.show()
    
 
fd3.close()
