import textgrid
import os

def parse_Interval(IntervalObject):
    start_time = ""
    end_time = ""
    P_name = ""

    ind = 0
    str_interval = str(IntervalObject)
    # print(str_interval)
    for ele in str_interval:
        if ele == "(":
            ind = 1
        if ele == " " and ind == 1:
            ind = 2
        if ele == "," and ind == 2:
            ind = 3
        if ele == " " and ind == 3:
            ind = 4

        if ind == 1:
            if ele != "(" and ele != ",":
                start_time = start_time + ele
        if ind == 2:
            end_time = end_time + ele
        if ind == 4:
            if ele != " " and ele != ")":
                P_name = P_name + ele

    st = float(start_time)
    et = float(end_time)
    pn = P_name

    return {pn: (st, et)}

def parse_Interval_key(IntervalObject):
    start_time = ""
    end_time = ""
    P_name = ""

    ind = 0
    str_interval = str(IntervalObject)
    # print(str_interval)
    for ele in str_interval:
        if ele == "(":
            ind = 1
        if ele == " " and ind == 1:
            ind = 2
        if ele == "," and ind == 2:
            ind = 3
        if ele == " " and ind == 3:
            ind = 4

        if ind == 1:
            if ele != "(" and ele != ",":
                start_time = start_time + ele
        if ind == 2:
            end_time = end_time + ele
        if ind == 4:
            if ele != " " and ele != ")":
                P_name = P_name + ele

    st = float(start_time)
    et = float(end_time)
    pn = P_name

    return pn, (st, et)


def parse_textgrid(filename):
    tg = textgrid.TextGrid.fromFile(filename)
    list_words = tg.getList("words")
    words_list = list_words[0]

    for ele in words_list:
        d = parse_Interval(ele)
        print(d)

def parse_textgrid_line(filename):
    tg = textgrid.TextGrid.fromFile(filename)
    list_words = tg.getList("words")
    words_list = list_words[0]

    word = ','
    time = ''
    for ele in words_list:
        w,t = parse_Interval_key(ele)
        if w!='None':
            word = word + ''.join(w)+','
        time = time + ''.join(str(t[1])) + ',' 

    #print(word) 
    #print(time) 
    return os.path.split(filename)[-1].split(".")[0], word, time

def parse(file_path, o_post):
    ls = os.listdir(file_path)
    for i in ls:
        son_path = os.path.join(file_path,i)
        if os.path.isdir(son_path):
            parse(son_path,o_post)
        else:
            file_post = str(i.split('.')[-1])
            # o_post file
            if file_post == o_post:
                #os.rename(son_path,str(son_path.split('.')[0])+'.'+n_post)
                print('找到文件{srcnam}'.format(srcnam=son_path))
                contend = parse_textgrid_line(son_path)
                
                filename = '20170001P00001.alignment.txt'
                
                with open(filename, 'a', encoding='UTF-8') as file_object:
                    contends = file_object.writelines(contend[0] + ' "'+ contend[1] + '" "' + contend[2] + '"\n')

if __name__ == "__main__":
    #parse_Interval('Interval(13.63000, 13.78000, ah0)')
    #parse_textgrid("D:/dataset/aligned_output/ST-CMDS-20170001_1-OS/20170001P00001A0001.TextGrid")
    #print(parse_textgrid_line("D:/dataset/aligned_output/ST-CMDS-20170001_1-OS/20170001P00001A0001.TextGrid"))
    parse("D:/dataset/aligned_output/ST-CMDS-20170001_1-OS","TextGrid")