# -*- coding: utf-8 -*-
import  pandas  as pd
import xlrd
import openpyxl
import ast
from tqdm import tqdm

def get_department():
    hospital=pd.read_excel('data.xlsx')
    df=pd.read_excel('data.xlsx', sheet_name=1)
    data=hospital.values
    '''
    科室过滤
    '''
    #print("读取指定行的数据：\n{0}".format(data))
    df2 = df.groupby(['一级科室', '二级科室'])[['医院名称']].first()
    #print("读取指定行的数据：\n{0}".format(df2))
    df2.to_csv("data.csv", encoding='GBK')

    #print("输出行号列表",df.index.values)
    #data=df.ix[1,].values
    #print("读取指定行的数据：\n{0}".format(data))
    #for index in hospital.index.values:
    #    pass

def print_xls(path):
    print('数据格式化......')
    workbook = xlrd.open_workbook(path)
    hospitals = workbook.sheet_by_name('data')
    department_sheet = workbook.sheet_by_name('department')
    #out = workbook.sheet_by_name('out')
    nrows = hospitals.nrows
    out_data = []
    result = []
    for i in tqdm(range(nrows)):
        hospital = hospitals.row_values(i)
        if i != 0:
            # 科室
            # ["泌尿外科","性功能障碍诊疗区","前列腺诊疗区","生殖感染科","生殖整形科","不孕不育诊疗区"]
            department = ast.literal_eval(hospital[11])
            for strdep in department:
                temp = ''
                # 查找一级科室
                major_department = []
                for j in range(department_sheet.nrows):
                    # 对应二级科室
                    minor_department = department_sheet.row_values(j)[1]
                    # 如果存在一级科室
                    if strdep == minor_department:
                        major_department.append(department_sheet.row_values(j)[0])
                    else:
                        #不存在
                        pass
                # 追加一级科室，二级科室
                major = set(major_department)
                temp = hospital + ['--'.join(major),strdep]
                result.append(temp)
        else:
            # 标题
            out_data = out_data + hospital + ['一级科室','二级科室']
            result.append(out_data)
    save_to_csv(result)
    #print(result)

def save_to_csv(data):
    df = pd.DataFrame(data=data)
    df.to_csv('hospital.csv',encoding='GBK')

if __name__ == "__main__":
    print_xls('data.xlsx')