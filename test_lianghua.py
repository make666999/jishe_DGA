import functools
import torch
from torch import nn
from torch.ao.quantization import float_qparams_weight_only_qconfig
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from collections import Counter
import pandas as pd
import numpy as np
from Model.Train_Model.Train_Transformer_R_SKNET import Transformer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import time

# 定义设备
DEVICE = torch.device('cpu')




def load_data(path, L):
    df = pd.read_csv(path)
    char_counts = Counter(''.join(df['url']))
    char2index = {char: idx for idx, char in enumerate(char_counts.keys())}
    vocab_size = len(char2index)
    df['encoded_url'] = df['url'].apply(lambda x: [char2index.get(char, 0) for char in x[:L]] + [0] * (L - len(x)))
    label2idx = {label: idx for idx, label in enumerate(df['Label'].unique())}
    df['encoded_label'] = df['Label'].apply(lambda x: label2idx[x])
    x = np.array(list(df['encoded_url']))
    y = np.array(df['encoded_label'])
    return x, y, vocab_size, len(label2idx)


def evaluate(model, data_loader, device):
    model.eval()
    correct = 0
    total = 0
    start_time = time.time()
    with torch.no_grad():
        for inputs, targets in data_loader:
            inputs, targets = inputs.to(device), targets.to(device, dtype=torch.long)
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += targets.size(0)
            correct += (predicted == targets).sum().item()
    inference_time = time.time() - start_time
    return correct / total, inference_time


BATCH_SIZE = 256
EMBEDDING_DIM = 64
L = 40
model = Transformer()

model.to(device)
model.eval()
path = "./Model/Data/clean_data/data_all.csv"
x, y, vocab_size, labels_size = load_data(path, L)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
train_data = TensorDataset(torch.tensor(x_train, dtype=torch.int32), torch.tensor(y_train, dtype=torch.long))
test_data = TensorDataset(torch.tensor(x_test, dtype=torch.int32), torch.tensor(y_test, dtype=torch.long))
train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, drop_last=True)

