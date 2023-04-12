from logging import raiseExceptions
import os
import xml.etree.ElementTree as ET

PASCAL_Class_index = {
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "0" : 10,
    "가" : 11,
    "거" : 12,
    "고" : 13,
    "구" : 14,
    "나" : 15,
    "너" : 16,
    "노" : 17,
    "누" : 18,
    "다" : 19,
    "더" : 20,
    "도" : 21,
    "두" : 22,
    "라" : 23,
    "러" : 24,
    "로" : 25,
    "루" : 26,
    "마" : 27,
    "머" : 28,
    "모" : 29,
    "무" : 30,
    "버" : 31,
    "보" : 32,
    "부" : 33,
    "서" : 34,
    "소" : 35,
    "수" : 36,
    "어" : 37,
    "오" : 38,
    "우" : 39,
    "저" : 40,
    "조" : 41,
    "주" : 42,
    "하" : 43,
    "허" : 44,
    "호" : 45,
    "공" : 46,
    "국" : 47,
    "육" : 48,
    "합" : 49,
    "해" : 50,
    "바" : 51,
    "사" : 52,
    "아" : 53,
    "자" : 54,
    "배" : 55,
    "서울_H" : 56,
    "부산_H" : 57,
    "대구_H" : 58,
    "인천_H" : 59,
    "광주_H" : 60,
    "대전_H" : 61,
    "울산_H" : 62,
    "세종_H" : 63,
    "경기_H" : 64,
    "강원_H" : 65,
    "충북_H" : 66,
    "충남_H" : 67,
    "전북_H" : 68,
    "전남_H" : 69,
    "경북_H" : 70,
    "경남_H" : 71,
    "제주_H" : 72,
    "서울_V" : 73,
    "부산_V" : 74,
    "대구_V" : 75,
    "인천_V" : 76,
    "광주_V" : 77,
    "대전_V" : 78,
    "울산_V" : 79,
    "세종_V" : 80,
    "경기_V" : 81,
    "강원_V" : 82,
    "충북_V" : 83,
    "충남_V" : 84,
    "전북_V" : 85,
    "전남_V" : 86,
    "경북_V" : 87,
    "경남_V" : 88,
    "제주_V" : 89,
    "서울_D" : 90,
    "부산_D" : 91,
    "대구_D" : 92,
    "인천_D" : 93,
    "광주_D" : 94,
    "대전_D" : 95,
    "울산_D" : 96,
    "세종_D" : 97,
    "경기_D" : 98,
    "강원_D" : 99,
    "충북_D" : 100,
    "충남_D" : 101,
    "전북_D" : 102,
    "전남_D" : 103,
    "경북_D" : 104,
    "경남_D" : 105,
    "제주_D" : 106,
    "서울_O" : 107,
    "부산_O" : 108,
    "대구_O" : 109,
    "인천_O" : 110,
    "광주_O" : 111,
    "대전_O" : 112,
    "울산_O" : 113,
    "세종_O" : 114,
    "경기_O" : 115,
    "강원_O" : 116,
    "충북_O" : 117,
    "충남_O" : 118,
    "전북_O" : 119,
    "전남_O" : 120,
    "경북_O" : 121,
    "경남_O" : 122,
    "제주_O" : 123,
    "영" : 124,
    "-" : 125,
    "차" : 126,
    "카" : 127,
    "타" : 128,
    "파" : 129,
    "퍼" : 130,
    "코" : 131,
    "포" : 132,
    "추" : 133,
    "투" : 134,
    "느" : 135,
    "스" : 136,
    "즈" : 137,
    "츠" : 138,
    "크" : 139,
    "프" : 140,
    "흐" : 141,
    "으" : 142,
    "태극" : 143,
    "임" : 144,
}

XML_DIRECTORY = "./XML"
TXT_DIRECTORY = "./TXT"

def Write_TXT(file_name,width,height,result):
    file_name = file_name[:-3]+"txt"
    file_path = os.path.join(TXT_DIRECTORY,file_name)
    f = open(file_path,"w")
    for i ,data in enumerate(result) :
        data = f"{data}\n"
        data = data.replace(",","").replace("[","").replace("]","")
        f.write(data)
    f.close()


def Read_XML(file_path,file_name) :
    tree = ET.parse(file_path)
    root = tree.getroot()
    size = root.find("size")
    width = float(size.find("width").text)
    height = float(size.find("height").text)

    result = list()
    for object in root.findall('object'):
        name = object.find("name").text
        class_index = PASCAL_Class_index[name]
        bndbox = object.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)
        bnd_width = round((xmax-xmin)/width,6)
        bnd_height = round((ymax-ymin)/height,6)
        x_center = round((xmax+xmin)/2/width,6)
        y_center = round((ymax+ymin)/2/height,6)
        result.append([class_index,x_center,y_center,bnd_width,bnd_height])
    Write_TXT(file_name=file_name,width=width,height=height,result=result)

def createFolder(directory):
    try :
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error' + directory)

def main():
    if not os.path.isdir(XML_DIRECTORY):
        raise Exception("No XML Dir")
    createFolder(TXT_DIRECTORY)
    for(root,directories,files) in os.walk(XML_DIRECTORY):
        for file in files:
            if '.xml' in file:
                file_path = os.path.join(root,file)
                Read_XML(file_path,file)


if __name__=="__main__":
    main()

        


