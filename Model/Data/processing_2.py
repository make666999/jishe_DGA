from urllib.parse import urlparse
from collections import Counter
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

import warnings
import os.path
from matplotlib import MatplotlibDeprecationWarning
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)


dga_file= "original_data/dga-domain.txt"
alexa_file= "original_data/top-1m.csv"
def writeData(file):
    print("Loading raw Data...")
    raw_data = pd.read_csv(file, header=None, low_memory=False)
    return raw_data.drop([0])
def load_alexa():

    x=[]
    data = pd.read_csv(alexa_file, sep=",",header=None,names=["Label", "url"])
    data.iloc[:,0]="BENIGN"

    data.to_csv('./Data-clean/top-1m.csv', index=False)

    x=[i[1] for i in data.values]
    return x

def load_dga():
    x=[]
    data = pd.read_csv(dga_file, sep="\t", header=None,
                      skiprows=18)
    data=data.iloc[:, :2]
    data.columns = ["Label", "url"]
    data.to_csv("./Data-clean/dga-domain.csv", index=False)
    # print(Data[0].value_counts())
    x=[i[1] for i in data.values]
    return x

def create_char_vocab(chars):
    char_index_dict = {}
    for index, char in enumerate(chars):
        if char not in char_index_dict:
            char_index_dict[char] = [index]
        else:
            char_index_dict[char].append(index)

    return char_index_dict
def num(chars):
    result = []

    temp = [value if key in chars else [0] for key, value in chars.items()]
    result.append(temp)

    return result


def count_characters_in_column(df, column_name):
    # 提取指定列的数据
    data = df[column_name]

    # 将所有数据拼接成一个长字符串
    all_data = ''.join(data)

    # 使用Counter统计字符出现的次数
    char_counts = Counter(all_data)

    return char_counts
def encode_and_pad_column(df, column_name, L=40):
    # 字符到索引的映射字典
    char_index_dict = {'g': 1, 'o': 2, 'l': 3, 'e': 4, '.': 5, 'c': 6, 'm': 7, 'w': 8, 'f': 9, 'a': 10, 'b': 11,
                       'k': 12,
                       'i': 13, 'r': 14, 's': 15, 't': 16, 'd': 17, 'u': 18, 'n': 19, '4': 20, '-': 21, 'y': 22,
                       'p': 23,
                       'h': 24, 'z': 25, 'v': 26, 'x': 27, '2': 28, '1': 29, '3': 30, 'q': 31, 'j': 32, '0': 33,
                       '5': 34,
                       '9': 35, '6': 36, '8': 37, '7': 38}

    # 对指定列进行编码和填充/截断处理
    encoded_values = []
    for value in df[column_name]:
        encoded_value = []
        for char in value:
            if char in char_index_dict:
                encoded_value.append(char_index_dict[char])
        # 填充或截断处理
        if len(encoded_value) < L:
            encoded_value += [0] * (L - len(encoded_value))
        else:
            encoded_value = encoded_value[:L]
        encoded_values.append(encoded_value)

    # 将处理后的数据存入新列
    new_column_name = f'encoded_{column_name}'
    df[new_column_name] = encoded_values

    return df


def encode_labels_in_df(df, label_column):
    # 创建一个LabelEncoder对象
    # label_encoder = LabelEncoder()

    # 使用LabelEncoder对标签列进行编码
    df[label_column] = (df[label_column] != 0).astype(int)  # BENIGN为0，其余为1

    label_mapping = {"BENIGN": 0, "DGA": 1}  # 定义标签映射关系

    return df, label_mapping



def get_feature_charseq():

    # load_dga()
    # load_alexa()
    # BENIGN = writeData("./Data-clean/top-1m.csv")
    # DGA = writeData("./Data-clean/dga-domain.csv")
    # frame=[BENIGN,DGA]
    # result = pd.concat(frame)
    # counts=result[0].value_counts()
    # invalid_labels = counts[counts < 20].index
    #
    # # 根据条件筛选出现次数大于等于 20 的数据
    # filtered_result = result[~result[0].isin(invalid_labels)]
    # filtered_result.columns = ["Label", "url"]
    # filtered_result.loc[:,"url"]=filtered_result["url"].str.lower()
    #
    # filtered_result = filtered_result.drop_duplicates(subset='url')
    #
    # print(filtered_result["Label"].value_counts())
    # df, class_map = encode_labels_in_df(filtered_result, "Label")
    # print(df["Label"].value_counts())  # num_class 44
    # print(class_map)
    #
    # filtered_result.to_csv("./Data-clean/data_all_2.csv",index=False)

    df = pd.read_csv('./clean_data/data_all.csv')
    df, class_map = encode_labels_in_df(df, "Label")
    # df.to_csv("./Data-clean/data_all_2.csv", index=False)

    # count_characters_in_column: 统计字符出现次数



    # chars=[]
    # # 打印统计结果，编制每个字符的数字索引(字典)
    # for char, _ in char_counts_in_url.items():
    #     chars.append(char)
    # char_to_index = {char: idx+1 for idx, char in enumerate(chars)}
    # print(char_to_index)
    #
    # #统计有多少个字符
    # vocab_size = len(char_to_index.keys())
    # print(vocab_size)#vocab_size 38
    #
    # # 使用LabelEncoder对标签列进行编码，并统计分类总数
    # df , class_map= encode_labels_in_df(df, "Label")
    # print(df["Label"].value_counts())# num_class 44
    # print(class_map)  #{'BENIGN': 0, 'bamital': 1, 'banjori': 2, 'bigviktor': 3, 'chinad': 4, 'conficker': 5, 'cryptolocker': 6, 'dircrypt': 7, 'dyre': 8, 'emotet': 9, 'enviserv': 10, 'feodo': 11, 'fobber_v1': 12, 'fobber_v2': 13, 'gameover': 14, 'gspy': 15, 'locky': 16, 'matsnu': 17, 'murofet': 18, 'mydoom': 19, 'necurs': 20, 'nymaim': 21, 'omexo': 22, 'padcrypt': 23, 'proslikefan': 24, 'pykspa_v1': 25, 'pykspa_v2_fake': 26, 'pykspa_v2_real': 27, 'qadars': 28, 'ramnit': 29, 'ranbyus': 30, 'rovnix': 31, 'shifu': 32, 'shiotob': 33, 'simda': 34, 'suppobox': 35, 'symmi': 36, 'tempedreve': 37, 'tinba': 38, 'tinynuke': 39, 'tofsee': 40, 'vawtrak': 41, 'vidro': 42, 'virut': 43}
    #
    # # 制作label反向索引
    # label_reversed={v:k for k,v in class_map.items()}
    # print(label_reversed)#{0: 'BENIGN', 1: 'bamital', 2: 'banjori', 3: 'bigviktor', 4: 'chinad', 5: 'conficker', 6: 'cryptolocker', 7: 'dircrypt', 8: 'dyre', 9: 'emotet', 10: 'enviserv', 11: 'feodo', 12: 'fobber_v1', 13: 'fobber_v2', 14: 'gameover', 15: 'gspy', 16: 'locky', 17: 'matsnu', 18: 'murofet', 19: 'mydoom', 20: 'necurs', 21: 'nymaim', 22: 'omexo', 23: 'padcrypt', 24: 'proslikefan', 25: 'pykspa_v1', 26: 'pykspa_v2_fake', 27: 'pykspa_v2_real', 28: 'qadars', 29: 'ramnit', 30: 'ranbyus', 31: 'rovnix', 32: 'shifu', 33: 'shiotob', 34: 'simda', 35: 'suppobox', 36: 'symmi', 37: 'tempedreve', 38: 'tinba', 39: 'tinynuke', 40: 'tofsee', 41: 'vawtrak', 42: 'vidro', 43: 'virut'}
    # # 制作url反向索引
    # dict_reversed={v:k for k,v in char_to_index.items()}
    # print(dict_reversed)
    # # {1: 'g', 2: 'o', 3: 'l', 4: 'e', 5: '.', 6: 'c', 7: 'm', 8: 'w', 9: 'f', 10: 'a', 11: 'b', 12: 'k', 13: 'i', 14: 'r', 15: 's', 16: 't', 17: 'd', 18: 'u', 19: 'n', 20: '4', 21: '-', 22: 'y', 23: 'p', 24: 'h', 25: 'z', 26: 'v', 27: 'x', 28: '2', 29: '1', 30: '3', 31: 'q', 32: 'j', 33: '0', 34: '5', 35: '9', 36: '6', 37: '8', 38: '7'}
    #
    # # #过长截断，过短补0
    # # df = encode_and_pad_column(df, 'url')
    # # print(df["encoded_url"])
    # # df.to_csv("./Data-clean/data_all_encode.csv",index=False)
    # # # 打印位置编码的字典
    # #
    #
    #
    # 统计url列的每个数据长度
    url_lengths = df['url'].apply(len)

    # 过滤出长度不超过60的URL
    filtered_lengths = url_lengths[url_lengths <= 60]

    # 创建直方图
    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(filtered_lengths, bins=30, color='skyblue', edgecolor='black')

    # 添加数值标签

    # 设置图表标题和坐标轴标签
    ax.set_title('URL Length Distribution')
    ax.set_xlabel('Length')
    ax.set_ylabel('Count')

    # 添加网格线
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # 使用科学计数法格式化y轴
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.savefig('./test.png')
    plt.show()


    # 计算不同长度范围的占比
    length_ranges = [0, 20, 40, 60]
    count_percentages = pd.cut(filtered_lengths, bins=length_ranges).value_counts(normalize=True) * 100

    # 打印各个范围的百分比
    for interval, percentage in count_percentages.items():
        print(f"Length {interval}: {percentage:.2f}%")





get_feature_charseq()