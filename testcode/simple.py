import sys
import os
import torch
import numpy as np
import yaml
import math

home_path = ""

def yolov5_detect():
    img = './130509_P_T18.jpg'        
    if (len(sys.argv) > 1) : img = sys.argv[1]  
    print( f'파일명 : {img}')
    
    with open('./data1.yaml') as f :
        CodeClass = yaml.load(f,Loader=yaml.FullLoader)
#        print(CodeClass)
    
    model = torch.hub.load('../yolov5/', 'custom' , '../yolov5/best_car.pt' , source='local' )
# 추론 
    results = model(img)
    icnt = len(results.xyxy[0])
    car_code =  np.zeros((icnt,8),dtype='float')
    iseq = 0
    for i in results.xyxy[0].tolist():
#        print(f'x {i[0]} y {i[1]} x1 {i[2]} y1 {i[3]} class: {i[5]} ')
        for j in range(0,6) : car_code[iseq][j] = float(i[j])
        iseq = iseq + 1
        
# 번호판의 영역을 구분하기 위해서는 세로좌표(인덱스:1)를 위아래로 구분을 한 다음에 왼쪽순서대로 찍어주면 된다. 
    fSum = 0
    for i in range(icnt) :
        fSum = fSum + car_code[i][1]
    fAvg = fSum / icnt    
# 표준편차를 처리해야한다. 약 20을 기준으로하여 미만이면 한줄 번호판으로 처리한다.
    fsd = 0
    for i in range(icnt) :
        fsd = fsd + (car_code[i][1]-fAvg)*(car_code[i][1]-fAvg)
    fsd = math.sqrt(fsd)
    print(f'표준편차 = {fsd}')

# 평균을 구한 다음에 평균이하는 좌표상 상단으로 구분하고, 평균이상은 하단으로 구분한다.    
# 표준편차를 기준으로 약 20 미만이면 한줄 번호판으로 처리한다.
# 두줄이라고 판단되면 하단줄 숫자에 10을 추가하여 전체순서를 뒤로 미룬다.
    if (fsd > 20) :
        for i in range(icnt) :
            if (car_code[i][1] > fAvg) : car_code[i][6] = 1
        
# 현재 6번째 컬럼에 0으로 설정된 부분은 상단이며, 1로 설정된 부분은 하단이다.         
# 데이터의 순서는 Sx , Sy , Ex , Ey , 정확도 , 클래스 , 상하 , 순서
    for i in range(icnt) :
        if (car_code[i][6] == 1) : car_code[i][7] = 10
        
# 같은 행에 대하여 가로좌표를 기준으로 자신보다 작은아이템의 숫자만큼 1 을 더한다.  왼쪽부터 낮은숫자로 세팅된다.        
    for i in range(icnt) :
        for j in range(icnt) :
            if (car_code[i][6] == car_code[j][6]) : 
                if (car_code[i][0] > car_code[j][0]) : car_code[i][7] = car_code[i][7] + 1
    print('\tSx\tSy\t\tEx\t\tEy\t정확도\t\t클래스\t상하구분\t좌우순서\t')
    print(car_code)   

    print("Result Class and Position")        
    print(results.pandas().xyxy[0])
  
# 클래스에 등록된 명칭에 따라서 숫자화된 분류를 라벨명칭으로 대체한다.   
# Confidence 값이 0.7 이상인 값들만 출력하는것으로 한다. 
# 7번째 인자는 순서를 정하는 값이며, 4번째 인자는 신뢰도이다. 
    retStr = '' 
    for i in range(20) :  # 최대숫자라고 가정을 한다.
        for j in range(icnt) :
            if (car_code[j][7]==i and car_code[j][4] > 0.7) : retStr = retStr + CodeClass['names'][int(car_code[j][5])] + ' , '
#            if (car_code[j][7]==i) : retStr = retStr + str(car_code[j][5]) + ' , '
    print('Final CarNumber = ' + retStr) 

if __name__ == '__main__':    
    curpath = os.getcwd()
    print(__file__)
    homepath = curpath.rsplit('/',1)
    print(f'path = { curpath } ')
    home_path = homepath[0]
    yolov5_detect()
    
    