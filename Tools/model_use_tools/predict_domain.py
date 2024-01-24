
import os
from collections import Counter
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from Model.Train_Model.Train_Transformer_R_SKNET import Transformer
name = "Transformer+R_SKNET"  ###准确率最高

model_path = os.path.abspath(os.path.join("Model", "Model_File","Transformer+R_SKNET.pth"))
png_path = f"./png/{name}.png"
logpath = f"./log/{name}.csv"
embedding_dim = 64  # 嵌入词向量的纬度
L = 40
loss_all = []
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
label2idx = {'BENIGN': 0, 'banjori': 1, 'bigviktor': 2, 'chinad': 3, 'conficker': 4, 'cryptolocker': 5,
             'dircrypt': 6, 'dyre': 7, 'emotet': 8, 'enviserv': 9, 'feodo': 10, 'fobber_v1': 11, 'fobber_v2': 12,
             'gameover': 13, 'locky': 14, 'matsnu': 15, 'murofet': 16, 'necurs': 17, 'nymaim': 18, 'pykspa_v1': 19,
             'pykspa_v2_fake': 20, 'pykspa_v2_real': 21, 'qadars': 22, 'ramnit': 23, 'ranbyus': 24, 'rovnix': 25,
             'shifu': 26, 'shiotob': 27, 'simda': 28, 'suppobox': 29, 'symmi': 30, 'tinba': 31, 'vawtrak': 32,
             'virut': 33}
idx2label={v:k for k,v in label2idx.items()}
char_index_dict = {'f': 0, 'i': 1, 'l': 2, 'e': 3, '2': 4, '.': 5, 'n': 6,
              'g': 7, 'r': 8, 'c': 9, 'o': 10, 'm': 11, 'w': 12, 'q': 13,
              'u': 14, 'a': 15, 'v': 16, 'd': 17, 's': 18, 'b': 19, 'x': 20,
              '1': 21, 'h': 22, 't': 23, 'p': 24, '4': 25, '8': 26, '0': 27,
              '7': 28, '-': 29, '5': 30, '9': 31, 'k': 32, '3': 33, 'j': 34,
              'y': 35, 'z': 36, '6': 37}

model = Transformer(38, embedding_dim, 34)
model.to(device)
def encode_domain(domain, L, char_index_dict):
    # 对单个域名进行编码和填充/截断处理
    encoded_value = []
    for char in domain:
        if char in char_index_dict:
            encoded_value.append(char_index_dict[char])

    # 填充或截断处理
    if len(encoded_value) < L:
        encoded_value += [0] * (L - len(encoded_value))
    else:
        encoded_value = encoded_value[:L]
    return encoded_value
def predict_domain(model,domain):
    domain = encoder(domain,L)
    model.eval()
    with torch.no_grad():
        X = domain.clone().detach().long().view(1, -1).to(device)
        y_pred = model(X)
        output_softmax = F.softmax(y_pred, dim=1)
        predicted_labels = torch.argmax(output_softmax, dim=1)
        predicted_classes = idx2label[predicted_labels.item()]
        return predicted_classes
def encoder(domain,L):
    domain=np.array(encode_domain(domain,L,char_index_dict))

    domain=torch.from_numpy(domain).to(torch.int32)

    return domain
def Predict_Domain():
    # 模型构建

    if os.path.exists(model_path):
        model.eval()
        model.load_state_dict(torch.load(model_path,device))
        return model

    else:
        return "REEOR"
# url=input()
# while(url!="\n"):
#
#     print(Predict_Domain(url))
#     url = input()





