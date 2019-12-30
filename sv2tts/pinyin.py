import pypinyin
from pypinyin.constants import (
    PHRASES_DICT, PINYIN_DICT, Style
)
from datetime import datetime
from pathlib import Path
import os
import jieba

class DatasetLog:
    """
    Registers metadata about the dataset in a text file.
    """
    def __init__(self, root, name):
        self.text_file = open(Path(root, "Log_%s.txt" % name.replace("/", "_")), "w")
        self.sample_data = dict()
        
        start_time = str(datetime.now().strftime("%A %d %B %Y at %H:%M"))
        self.write_line("Creating dataset %s on %s" % (name, start_time))
        self.write_line("-----")
        self._log_params()
        
    def _log_params(self):
        from encoder import params_data
        self.write_line("Parameter values:")
        for param_name in (p for p in dir(params_data) if not p.startswith("__")):
            value = getattr(params_data, param_name)
            self.write_line("\t%s: %s" % (param_name, value))
        self.write_line("-----")
    
    def write_line(self, line):
        self.text_file.write("%s\n" % line)
        
    def add_sample(self, **kwargs):
        for param_name, value in kwargs.items():
            if not param_name in self.sample_data:
                self.sample_data[param_name] = []
            self.sample_data[param_name].append(value)
            
    def finalize(self):
        self.write_line("Statistics:")
        for param_name, values in self.sample_data.items():
            self.write_line("\t%s:" % param_name)
            self.write_line("\t\tmin %.3f, max %.3f" % (np.min(values), np.max(values)))
            self.write_line("\t\tmean %.3f, median %.3f" % (np.mean(values), np.median(values)))
        self.write_line("-----")
        end_time = str(datetime.now().strftime("%A %d %B %Y at %H:%M"))
        self.write_line("Finished on %s" % end_time)
        self.text_file.close()
 
 
# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s
 
 
# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, style=Style.TONE3):
        s = s + ''.join(i) + " "
    return s

# 获取文件的内容
def get_contends(path):
    with open(path,encoding='UTF-8') as file_object:
        contends = file_object.read()
    return contends
    
def find_file(file_path, o_post):
    path = '/home/mungo/sv2tts'
    ls = os.listdir(file_path)
    for i in ls:
        son_path = os.path.join(file_path,i)
        if os.path.isdir(son_path):
            find_file(son_path,o_post)
        else:
            file_post = str(i.split('.')[-1])
            # o_post file
            if file_post == o_post:
                #os.rename(son_path,str(son_path.split('.')[0])+'.'+n_post)
                print('找到文件{srcnam}'.format(srcnam=son_path))
                contend = get_contends(son_path)
                print(contend)
                # 分词，注音
                words = list(jieba.cut(contend))
                pinyin = ''
                hanzi = ''
                for word in words:
                    pinyin = pinyin + ''.join(yinjie(word).replace(' ','')) + " "
                    hanzi = hanzi + ''.join(word) + " "

                filename = str(son_path.split('.')[0])+'.lab'
                #filename_cn = str(son_path.split('.')[0])+'.lab'

                with open(filename, 'w', encoding='UTF-8') as file_object:
                    file_object.write(pinyin)

                #with open(filename_cn, 'a', encoding='UTF-8') as file_object:
                #   file_object.write(hanzi)
               

datasets_root = "/media/mungo/新加卷/ST-CMDS-20170001_1-OS"

if __name__ == "__main__":
    #print(pinyin("忠厚传家久"))
    find_file(datasets_root,"txt")

    #print(yinjie("世道乱了哈哈熊孩子们"))