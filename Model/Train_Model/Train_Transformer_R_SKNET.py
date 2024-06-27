import os
from collections import Counter
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import torchmetrics
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import TensorDataset
from sklearn.model_selection import train_test_split
from torch import optim, Tensor
from torchnet import meter
import matplotlib.pyplot as plt
import warnings
from matplotlib import MatplotlibDeprecationWarning
from torchinfo import summary

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)
def loss_value_plot(losses):
    # 画出loss变化趋势图
    plt.plot([i for i in range(1, epochs + 1)], losses, label='Training Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Iterations')
    plt.legend()
    plt.savefig(png_path)
    plt.show()


def count_characters_in_column(df, column_name):
    # 提取指定列的数据
    data = df[column_name]

    # 将所有数据拼接成一个长字符串
    all_data = ''.join(data)

    # 使用Counter统计字符出现的次数
    char_counts = Counter(all_data)

    return char_counts


def use_model_data(url, char2index):
    encode = encode_oneurl(url, char2index)

    x = np.array([sent for sent in encode])
    x = torch.from_numpy(x).to(torch.int32).to(device).unsqueeze(0)

    output_ = model(x)
    probabilities = F.softmax(output_, dim=1)
    predicted_indices = torch.argmax(probabilities, dim=1)

    # 根据对照表获取真实数值
    predicted_classes = [idx2label[idx.item()] for idx in predicted_indices]

    # 输出真实数值
    print(predicted_classes[0])


def encode_oneurl(url, char2index):
    encoded_value = []
    for char in url:
        if char in char2index:
            encoded_value.append(char2index[char])
    # 填充或截断处理
    if len(encoded_value) < L:
        encoded_value += [0] * (L - len(encoded_value))
    else:
        encoded_value = encoded_value[:L]
    return encoded_value


def encode_and_pad_column(df, column_name, L, char_index_dict):
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


# 字符索引
# "{'g': 1, 'o': 2, 'l': 3, 'e': 4, '.': 5, 'c': 6, 'm': 7, 'w': 8, 'f': 9, 'a': 10, 'b': 11, 'k': 12, 'i': 13, 'r': 14, 's': 15, 't': 16, 'd': 17, 'u': 18, 'n': 19, '4': 20, '-': 21, 'y': 22, 'p': 23, 'h': 24, 'z': 25, 'v': 26, 'x': 27, '2': 28, '1': 29, '3': 30, 'q': 31, 'j': 32, '0': 33, '5': 34, '9': 35, '6': 36, '8': 37, '7': 38}"
# 反向索引
# {1: 'g', 2: 'o', 3: 'l', 4: 'e', 5: '.', 6: 'c', 7: 'm', 8: 'w', 9: 'f', 10: 'a', 11: 'b', 12: 'k', 13: 'i', 14: 'r', 15: 's', 16: 't', 17: 'd', 18: 'u', 19: 'n', 20: '4', 21: '-', 22: 'y', 23: 'p', 24: 'h', 25: 'z', 26: 'v', 27: 'x', 28: '2', 29: '1', 30: '3', 31: 'q', 32: 'j', 33: '0', 34: '5', 35: '9', 36: '6', 37: '8', 38: '7'}

# 38个字符
# 44个标签


def load_data():
    df = pd.read_csv(path)

    char_counts_in_url = count_characters_in_column(df, 'url')

    chars = []
    # 打印统计结果，编制每个字符的数字索引(字典)
    for char, _ in char_counts_in_url.items():
        chars.append(char)
    char2index = {char: idx for idx, char in enumerate(chars)}
    print(char2index)
    # 字符索引数目
    vocab_size = len(char2index.keys())  # 38
    # 反向字符索引
    index2char = {v: k for k, v in char2index.items()}
    # 标签类别数目
    labels_size = len(label2idx.keys())  # 44
    # 反向标签索引
    idx2label = {v: k for k, v in label2idx.items()}
    # 对url进行编码
    df = encode_and_pad_column(df, "url", L, char2index)
    x = np.array([sent for sent in df["encoded_url"]])

    y = np.array([[sent] for sent in df["Label"]])
    return x, y, vocab_size, labels_size, index2char, idx2label, char2index


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=128):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        # 初始化Shape为(max_len, d_model)的PE (positional encoding)
        pe = torch.zeros(max_len, d_model)
        # 初始化一个tensor [[0, 1, 2, 3, ...]]
        position = torch.arange(0, max_len).unsqueeze(1)  # shape[128,1]
        # 这里就是sin和cos括号中的内容，通过e和ln进行了变换
        diev_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))

        # 计算PE(pos, 2i)
        pe[:, 0::2] = torch.sin(position * diev_term)
        pe[:, 1::2] = torch.cos(position * diev_term)
        # 在pe的最外边添加一个batch纬度
        pe = pe.unsqueeze(0)  # shape[1, 128, 64]
        # 如果一个参数不参与梯度下降，但又希望保存model的时候将其保存下来
        # 这个时候就可以用register_buffer
        self.register_buffer('pe', pe, persistent=False)  # 特殊点在于训练模型中register_buffer 定义的参数不能被更新

    def forward(self, x):
        # 将x和位置编码进行相加

        x = x + self.pe[:, :x.size(1)].requires_grad_(False)

        return self.dropout(x)


class CBAMLayer(nn.Module):
    def __init__(self, channel, reduction=16, spatial_kernel=7):
        super(CBAMLayer, self).__init__()

        # channel attention 压缩H,W为1
        self.max_pool = nn.AdaptiveMaxPool1d(1)
        self.avg_pool = nn.AdaptiveAvgPool1d(1)

        # shared MLP
        self.mlp = nn.Sequential(
            # Conv2d比Linear方便操作
            # nn.Linear(channel, channel // reduction, bias=False)
            nn.Conv1d(channel, channel // reduction, 1, bias=False),
            # inplace=True直接替换，节省内存
            nn.ReLU(inplace=True),
            # nn.Linear(channel // reduction, channel,bias=False)
            nn.Conv1d(channel // reduction, channel, 1, bias=False)
        )

        # spatial attention
        self.conv = nn.Conv1d(2, 1, kernel_size=spatial_kernel,
                              padding=spatial_kernel // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        max_out = self.mlp(self.max_pool(x))

        avg_out = self.mlp(self.avg_pool(x))

        channel_out = self.sigmoid(max_out + avg_out)
        # print(x.shape) #torch.Size([256, 128, 38])
        # print(channel_out.shape) #torch.Size([256, 1, 1])
        x = channel_out * x
        # print(x.shape) #torch.Size([256, 128, 38])
        max_out, _ = torch.max(x, dim=1, keepdim=True)

        avg_out = torch.mean(x, dim=1, keepdim=True)

        # torch.Size([512, 1, 38])
        cat = self.conv(torch.cat([max_out, avg_out], dim=1))
        spatial_out = self.sigmoid(cat)
        x = spatial_out * x

        return x


# class BiLSTM_Attention(nn.Module):
#     def __init__(self, input_size, hidden_size, num_class, num_layers=1):
#         super(BiLSTM_Attention, self).__init__()
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#
#         # LSTM
#         self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True,
#                             bidirectional=True)
#         # Dropout层
#         self.dropout = nn.Dropout(p=0.3)
#         # 全连接层
#         self.fc = nn.Linear(in_features=hidden_size * 2, out_features=num_class)
#
#     def self_attention(self, lstm_output):
#         attn_weights = torch.bmm(lstm_output, lstm_output.transpose(1, 2))
#         soft_attn_weights = nn.functional.softmax(attn_weights, dim=1)
#         new_hidden_state = torch.bmm(soft_attn_weights, lstm_output)
#         return new_hidden_state
#
#     def forward(self, x):
#         lstm_out, _ = self.lstm(x)
#
#         attn_output = self.self_attention(lstm_out)
#
#         return attn_output


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, stride=stride, padding=kernel_size // 2)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, padding=kernel_size // 2)
        self.bn2 = nn.BatchNorm1d(out_channels)
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_channels, out_channels, kernel_size=1, stride=stride),
                nn.BatchNorm1d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet1D(nn.Module):
    def __init__(self, input_channels, num_blocks, num_filters, kernel_size, num_classes):
        super(ResNet1D, self).__init__()
        self.conv1 = nn.Conv1d(input_channels, num_filters, kernel_size, padding=kernel_size // 2)
        self.bn1 = nn.BatchNorm1d(num_filters)
        self.blocks = self._make_blocks(num_blocks, num_filters, kernel_size)
        self.global_pooling = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(num_filters, num_classes)

    def _make_blocks(self, num_blocks, num_filters, kernel_size):
        blocks = []
        for _ in range(num_blocks):
            blocks.append(ResidualBlock(num_filters, num_filters, kernel_size))
        return nn.Sequential(*blocks)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.blocks(out)
        out = self.global_pooling(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


def conv_bn3X3(inp, oup, padd=0, stride=1, leaky=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 3, stride, padding=padd, bias=False),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=True)
    )


def conv_bn5X5(inp, oup, padd=1, stride=1, leaky=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 5, stride, padding=padd, bias=False),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=True)
    )


def conv_bn1X1(inp, oup, stride=1, leaky=0, padding=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 1, stride, bias=False, padding=padding),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=True)
    )


class FPN(nn.Module):
    def __init__(self, in_channels_list, out_channels, padd=0):
        super(FPN, self).__init__()
        leaky = 0
        self.channel_0 = EfficientChannelAttention(in_channels_list[0])
        self.channel_1 = EfficientChannelAttention(in_channels_list[1])
        self.channel_2 = EfficientChannelAttention(in_channels_list[2])
        self.channel_3 = EfficientChannelAttention(in_channels_list[3])
        self.channel_4 = EfficientChannelAttention(in_channels_list[2])
        self.channel_5 = EfficientChannelAttention(in_channels_list[1])
        self.channel_6 = EfficientChannelAttention(in_channels_list[0])
        # self.cbam_1 = CBAMLayer(channel=in_channels_list[0], reduction=4, spatial_kernel=7)
        # self.cbam_2 = CBAMLayer(channel=in_channels_list[1], reduction=4, spatial_kernel=7)
        # self.cbam_3 = CBAMLayer(channel=in_channels_list[2], reduction=4, spatial_kernel=7)
        # self.cbam_4 = CBAMLayer(channel=in_channels_list[0], reduction=4, spatial_kernel=7)
        # self.cbam_5 = CBAMLayer(channel=in_channels_list[0], reduction=4, spatial_kernel=7)
        self.output_1 = conv_bn1X1(in_channels_list[0], out_channels, stride=1, leaky=leaky)
        self.output_2 = conv_bn1X1(in_channels_list[1], out_channels, stride=1, leaky=leaky)
        self.output_3 = conv_bn1X1(in_channels_list[2], out_channels, stride=1, leaky=leaky)
        self.output_4 = conv_bn1X1(in_channels_list[3], out_channels, stride=1, leaky=leaky)
        self.pool1 = nn.MaxPool1d(kernel_size=3, stride=2, padding=1)
        self.pool2 = nn.AvgPool1d(kernel_size=3, stride=4, padding=1)
        self.pool3 = nn.AvgPool1d(kernel_size=3, stride=8, padding=1)
        self.nerge_1 = conv_bn3X3(out_channels, out_channels, leaky=leaky)
        self.nerge_2 = conv_bn3X3(out_channels, out_channels, leaky=leaky)
        self.nerge_3 = conv_bn3X3(out_channels, out_channels, leaky=leaky)

        self.nerge_4 = conv_bn3X3(out_channels, out_channels, leaky=leaky)
        """0 torch.Size([256, 128, 40])
            1 torch.Size([256, 128, 20])
            2 torch.Size([256, 128, 10])
            3 torch.Size([256, 128, 5])"""
    def forward(self, input):

        output_1 = self.output_1(self.channel_0(input[0]))  # torch.Size([256, 128, 40])
        # print(0,output_1.shape)
        output_2 = self.output_2(self.channel_1(input[1]))  # torch.Size([256, 128, 40])
        output_2 = self.pool1(output_2)
        # print(1, output_2.shape)
        output_3 = self.output_3(self.channel_2(input[2]))  # orch.Size([256, 128, 36])
        output_3 = self.pool2(output_3)
        # print(2, output_3.shape)
        output_4 = self.output_4(self.channel_3(input[3]))
        output_4 = self.pool3(output_4)
        # print(3, output_4.shape)
        output_4=self.nerge_4(output_4)
        up4 = F.interpolate(output_4, size=[output_3.size(2)], mode="nearest")
        up4 = self.channel_4(up4)
        output_3 = output_3 + up4

        output_3 = self.nerge_3(output_3)
        # print(11, output_3.shape)
        up3 = F.interpolate(output_3, size=[output_2.size(2)], mode="nearest")
        up3 = self.channel_5(up3)
        output_2 = output_2 + up3

        output_2 = self.nerge_2(output_2)
        # print(22, output_2.shape)
        up2 = F.interpolate(output_2, size=[output_1.size(2)], mode="nearest")
        up2 = self.channel_6(up2)
        output_1 = output_1 + up2
        output_1 = self.nerge_1(output_1)
        # print(33, output_1.shape)
        out = torch.cat((output_1, output_2, output_3, output_4), dim=2)

        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        self.conv1 = conv_bn1X1(inplanes, planes)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = conv_bn3X3(planes, planes, stride)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = conv_bn1X1(planes, planes * self.expansion)
        self.bn3 = nn.BatchNorm2d(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class BasicBlock_3(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, padd, stride=1, downsample=None):
        super(BasicBlock_3, self).__init__()
        self.conv1 = conv_bn3X3(inplanes, planes, padd, stride)
        self.bn1 = nn.BatchNorm1d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv_bn3X3(planes, planes, padd)
        self.bn2 = nn.BatchNorm1d(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)

        out = self.bn2(out)
        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class BasicBlock_5(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, padd, stride=1, downsample=None):
        super(BasicBlock_5, self).__init__()
        self.conv1 = conv_bn5X5(inplanes, planes, padd, stride)
        self.bn1 = nn.BatchNorm1d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv_bn5X5(planes, planes, padd)
        self.bn2 = nn.BatchNorm1d(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)

        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)
        return out


class EfficientChannelAttention(nn.Module):  # Efficient Channel Attention module
    def __init__(self, c, b=1, gamma=2):
        super(EfficientChannelAttention, self).__init__()
        t = int(abs((math.log(c, 2) + b) / gamma))
        k = t if t % 2 else t + 1

        self.max_pool = nn.AdaptiveMaxPool1d(1)
        self.avg_pool = nn.AdaptiveAvgPool1d(1)
        self.conv1 = nn.Conv1d(1, 1, kernel_size=k, padding=int(k / 2), bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        y=x
        max_pool = self.max_pool(x)
        # torch.Size([256, 64, 1])
        x = max_pool
        x = self.conv1(x.transpose(-1, -2)).transpose(-1, -2)
        out = self.sigmoid(x)
        out = y * out
        return out


class sknet_att(nn.Module):  # Efficient Channel Attention module
    def __init__(self, c, b=1, gamma=2):
        super(sknet_att, self).__init__()
        t = int(abs((math.log(c, 2) + b) / gamma))
        k = t if t % 2 else t + 1
        #
        # self.max_pool = nn.AdaptiveMaxPool1d(1)
        # self.avg_pool = nn.AdaptiveAvgPool1d(1)
        self.conv1 = nn.Conv1d(1, 1, kernel_size=k, padding=int(k / 2), bias=False)
        # self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # max_pool = self.max_pool(x)
        # avg_pool = self.avg_pool(x)
        # torch.Size([256, 64, 1])
        # x=max_pool+avg_pool
        x = self.conv1(x.transpose(-1, -2)).transpose(-1, -2)
        # out = self.sigmoid(x)

        return x


class SKConv(nn.Module):
    def __init__(self, features, M=2, r=16, stride=1, L=32):
        """ Constructor
        Args:
            features: input channel dimensionality.
            M: the number of branchs.
            G: num of convolution groups.
            r: the ratio for compute d, the length of z.
            stride: stride, default 1.
            L: the minimum dim of the vector z in paper, default 32.
        """

        super(SKConv, self).__init__()
        d = max(int(features / r), L)
        self.M = M
        self.features = features
        self.convs = nn.ModuleList([])
        # self.skatt_1 = sknet_att(sknet_att)
        # self.skatt_2 = sknet_att(sknet_att)
        for i in range(M):
            self.convs.append(nn.Sequential(
                nn.Conv1d(features, features, kernel_size=3, stride=stride, padding=1 + i, dilation=1 + i,
                          groups=features,
                          bias=False),
                nn.BatchNorm1d(features),
                nn.ReLU(inplace=True)
            ))
        self.avgpool = nn.AdaptiveAvgPool1d(1)


        self.fcs = nn.ModuleList([])
        for i in range(M):
            self.fcs.append(
                sknet_att(features)

            )
        self.softmax = nn.Softmax(dim=1)


    def forward(self, x):
        res_x = x
        attention_vectors = []
        batch_size = x.shape[0]

        feats = [conv(x) for conv in self.convs]
        feats = torch.cat(feats, dim=1)

        feats = feats.view(batch_size, self.M, self.features, feats.shape[2])

        feats_U = torch.sum(feats, dim=1)
        # print(2,feats_U.shape)

        feats_A_OUT = self.avgpool(feats_U)
        # feats_M_OUT = self.fc(self.maxpool(feats_U))
        # for fc in self.fcs:
        #     attention_vectors.append(fc(feats_A_OUT) + fc(feats_M_OUT))

        attention_vectors = [fc(feats_A_OUT) for fc in self.fcs]

        attention_vectors = torch.cat(attention_vectors, dim=1)

        attention_vectors = attention_vectors.view(batch_size, self.M, self.features, 1)

        attention_vectors = self.softmax(attention_vectors)

        feats_V = torch.sum(feats * attention_vectors, dim=1)

        return feats_V + res_x


class SKUnit(nn.Module):
    expansion = 1

    def __init__(self, in_features, out_features, M=3, r=16, stride=1, L=32):

        """ Constructor
        Args:
            in_features: input channel dimensionality.
            out_features: output channel dimensionality.
            M: the number of branchs.
            G: num of convolution groups.
            r: the ratio for compute d, the length of z.
            mid_features: the channle dim of the middle conv with stride not 1, default out_features/2.
            stride: stride.
            L: the minimum dim of the vector z in paper.
        """
        super(SKUnit, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv1d(in_features, out_features, 1, stride=1, bias=False),
            nn.BatchNorm1d(out_features),
            nn.ReLU(inplace=True)
        )

        self.conv2_sk = SKConv(out_features, M=M,
                               r=r, stride=stride, L=L)
        self.conv3 = nn.Sequential(
            nn.Conv1d(out_features, out_features, 1, stride=1, bias=False),
            nn.BatchNorm1d(out_features)
        )
        self.conv4_sk = SKConv(out_features, M=M,
                               r=r, stride=stride, L=L)
        self.conv5 = nn.Sequential(
            nn.Conv1d(out_features, out_features, 1, stride=1, bias=False),
            nn.BatchNorm1d(out_features)
        )

        if in_features == out_features:  # when dim not change, input_features could be added diectly to out
            self.shortcut = nn.Sequential()
        else:  # when dim not change, input_features should also change dim to be added to out
            self.shortcut = nn.Sequential(
                nn.Conv1d(in_features, out_features, 1, stride=stride, bias=False),
                nn.BatchNorm1d(out_features)
            )

        self.relu = nn.ReLU(inplace=True)
        # self.cbam=CBAMLayer(channel=out_features, reduction=4, spatial_kernel=7)

        self.channel = EfficientChannelAttention(out_features)

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.conv2_sk(out)

        out = self.conv3(out)
        out = self.conv4_sk(out)
        out = self.conv5(out)


        return self.relu(out + self.shortcut(residual))


class ResNet(nn.Module):

    def __init__(self, block, layers):
        super(ResNet, self).__init__()

        self.inplanes = 64
        # self.conv2 = nn.Conv1d(64, 128, kernel_size=3, stride=2, padding=1)
        # self.conv3 = nn.Conv1d(128, 256, kernel_size=3, stride=2, padding=1)
        # self.conv4 = nn.Conv1d(256, 512, kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=1)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=1)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=1)
        # self.avgpool = nn.AdaptiveAvgPool1d((1, 1))

        for m in self.modules():

            if isinstance(m, nn.Conv1d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

            # Zero-initialize the last BN in each residual branch,
            # so that the residual branch starts with zeros, and each residual block behaves like an identity.
            # This improves the model by 0.2~0.3% according to https://arxiv.org/abs/1706.02677

    def _make_layer(self, block, planes, blocks, stride=1, padd=1):
        downsample = None
        # if stride != 1 or self.inplanes != planes * block.expansion:
        #
        #     downsample = nn.Sequential(
        #         conv_bn1X1(self.inplanes, planes * block.expansion, stride,padd),
        #         nn.BatchNorm1d(planes * block.expansion),
        #     )

        layers = []
        # def __init__(self, in_features,  out_features, M=2, r=16, stride=1, L=32):
        layers.append(block(self.inplanes, planes))
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        """x_1torch.Size([256, 128, 40])
    x_2torch.Size([256, 256, 40])
    x_3torch.Size([256, 512, 40])"""
        y = self.layer1(x)
        # x = self.pool1(y)

        x_1 = self.layer2(y)
        # x_1_po = self.pool2(x_1)

        x_2 = self.layer3(x_1)

        # x_2_po = self.pool3(x_2)

        x_3 = self.layer4(x_2)

        return [y, x_1, x_2, x_3]


class Transformer(nn.Module):
    def __init__(self, vocab_size, embedding_dim, num_class, feedforward_dim=256, num_head=4,
                 num_layers=1, dropout=0.1, max_len=256, conv_channels=64, num_blocks=3):
        super(Transformer, self).__init__()
        # 嵌入层
        # 词典大小；每个词需要多少个纬度表示
        # embedding的编号是从0开始,字的编号也要从0开始

        self.fpn_3 = FPN([64, 128, 256, 512], 128, 1)
        # self.fpn_5 = FPN([128, 256, 512], 128, 2)
        self.SKNET = ResNet(SKUnit, [2, 2, 2, 2])

        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        # 位置编码层
        self.positional_encoding = PositionalEncoding(embedding_dim, dropout, max_len)
        # 编码层
        # feedforward_dim表示全连接层隐藏层维度
        self.encoder_layer = nn.TransformerEncoderLayer(embedding_dim, num_head, feedforward_dim, dropout,
                                                        batch_first=True)

        self.transformer = nn.TransformerEncoder(self.encoder_layer, num_layers)
        self.dropout = nn.Dropout(0.5)

        self.mlp = nn.Sequential(
            nn.Conv1d(128, num_class, 1, bias=False),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
        )

    def forward(self, x):

        x = x.transpose(0, 1)
        # 将输入的数据进行词嵌入，得到数据的维度为[序列长度,批次,嵌入向量]
        x = x.contiguous()
        x = self.embedding(x)

        # 加入位置编码
        x = self.positional_encoding(x)

        # 将数据代入到transformer模型中
        x = self.transformer(x)

        x = x.permute(1, 2, 0)  # torch.Size([256, 64, 40])


        x_3 = self.SKNET(x)

        fpn_out_3 = self.fpn_3(x_3)  # torch.Size([256, 128, 38])

        x = self.dropout(fpn_out_3)  # torch.Size([256, 128, 76])

        x = self.mlp(x)

        return x


def test(model):
    model.eval()

    with torch.no_grad():
        iter = 0
        loss_sum = 0
        metric_collection = torchmetrics.MetricCollection({
            'acc': torchmetrics.Accuracy(task="multiclass", num_classes=34, average=average),
            'prec': torchmetrics.Precision(task="multiclass", num_classes=34, average=average),
            'rec': torchmetrics.Recall(task="multiclass", num_classes=34, average=average),
            "F1": torchmetrics.F1Score(task="multiclass", num_classes=34, average=average)
        }).to(device)

        for i, (inputs, labels) in enumerate(test_loader):

            y_label = labels.to(device).view(-1)

            X = inputs.to(device)

            y_pred = model(X)
            # print(y_label[0])
            loss = criterion(y_pred, y_label.long())

            output_softmax = F.softmax(y_pred, dim=1)
            predicted_labels = torch.argmax(output_softmax, dim=1)
            metric_collection.update(predicted_labels, y_label)

            loss_sum += loss.item()
            iter += 1

        val_metrics = metric_collection.compute()
        print(f"Metrics on all data: {val_metrics}")

        idx2label = {idx: label for label, idx in label2idx.items()}
        print(idx2label)
        label_counts = {idx2label[idx]: count for idx, count in output_counts.items()}
        print(label_counts)
        df =pd.DataFrame()
        index={
            'BENIGN': 55000,
            'banjori': 2500,
            'bigviktor': 1000,
            'chinad': 1000,
            'conficker': 495,
            'cryptolocker': 1000,
            'dircrypt': 742,
            'dyre': 1000,
            'emotet': 2500,
            'enviserv': 500,
            'feodo': 247,
            'fobber_v1': 299,
            'fobber_v2': 300,
            'gameover': 2500,
            'locky': 1158,
            'matsnu': 908,
            'murofet': 2500,
            'necurs': 2500,
            'nymaim': 330,
            'pykspa_v1': 2500,
            'pykspa_v2_fake': 800,
            'pykspa_v2_real': 200,
            'qadars': 2000,
            'ramnit': 2500,
            'ranbyus': 2500,
            'rovnix': 2500,
            'shifu': 2500,
            'shiotob': 2500,
            'simda': 2500,
            'suppobox': 2234,
            'symmi': 2500,
            'tinba': 2500,
            'vawtrak': 828,
            'virut': 2500
        }
        df['Label'] = index.keys()
        df['Count'] = index.values()
        for index, (label, count) in enumerate(idx2label.items()):
            print(f"Label: {label}, Count: {count}")

            for index,(metric_name, values) in enumerate(val_metrics.items()):
                df[metric_name] = [round(value, 4) for value in values.tolist()]

        df.to_excel('output.xlsx', index=False)

        metric_collection.reset()
        avg_loss = loss_sum / iter

        print("Average Loss:", avg_loss)


def train(model, optimizer, loss_meter, epochs, path):
    losses = []

    model.train()
    metric_collection = torchmetrics.MetricCollection({
        'acc': torchmetrics.Accuracy(task="multiclass", num_classes=34, average=average),
        'prec': torchmetrics.Precision(task="multiclass", num_classes=34, average=average),
        'rec': torchmetrics.Recall(task="multiclass", num_classes=34, average=average),
        "F1": torchmetrics.F1Score(task="multiclass", num_classes=34, average=average)
    }).to(device)
    for epoch in range(epochs):
        epoch_acc_count = 0

        loss_meter.reset()  # 重置设置的参数，清空里面的数据
        train_count = 0
        for i, (inputs, labels) in enumerate(train_loader):

            y_label = labels.to(device).view(-1)
            x_input = inputs.to(device)

            optimizer.zero_grad()

            output_ = model(x_input)

            loss = criterion(output_, y_label.long())

            loss.backward()  # 反向传播
            optimizer.step()  # 参数更新
            with torch.no_grad():

                loss_meter.add(loss.item())
                # 数据分类，计算一个批次正确次数epoch_acc_count
                output_softmax = F.softmax(output_, dim=1)
                predicted_labels = torch.argmax(output_softmax, dim=1)

                epoch_acc_count += (predicted_labels == y_label)

                metric_collection.update(predicted_labels, y_label.long())
                train_count += len(x_input)
                if (i % 50 == 0):
                    epoch_acc = epoch_acc_count.sum().item() / train_count
                    print('训练精度为%s' % (str(epoch_acc * 100)[:5]) + '%')
                    epoch_acc_count = 0
                    train_count = 0
        losses.append(loss_meter.mean)

        print(f"epoch：{epoch} ------------------")
        print('训练损失为%s' % (str(loss_meter.mean)))
        val_metrics = metric_collection.compute()
        l_acc.append(val_metrics['acc'].tolist())
        l_prec.append(val_metrics['prec'].tolist())
        l_rec.append(val_metrics['rec'].tolist())
        l_f1.append(val_metrics['F1'].tolist())
        loss_all.append(loss_meter.mean)
        # 多列表存储数据到csv
        df = pd.DataFrame({'acc': l_acc, 'prec': l_prec, 'rec': l_rec, 'F1': l_f1, "loss": loss_all})

        df.to_csv(path)
        print(epoch, f"Metrics on all data: {val_metrics}")
        metric_collection.reset()
        scheduler.step()
    return losses




if __name__ == '__main__':
    datalist=[]
    average="weighted" #weighted
    name = "Transformer+R_SKNET"  ###准确率最高
    model_path = f"../Model_File/{name}.pth"
    png_path = f"./png/{name}.png"
    path = f"../Data/clean_data/data_all.csv"
    logpath = f"./log/{name}.csv"
    epochs = 100
    batch_size = 256  # 每个批次样本数量的大小
    embedding_dim = 64  # 嵌入词向量的纬度
    lr = 1e-3
    L = 40
    l_acc = []
    l_prec = []
    l_rec = []
    l_f1 = []
    loss_all = []
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    label2idx = {'BENIGN': 0, 'banjori': 1, 'bigviktor': 2, 'chinad': 3, 'conficker': 4, 'cryptolocker': 5,
                 'dircrypt': 6, 'dyre': 7, 'emotet': 8, 'enviserv': 9, 'feodo': 10, 'fobber_v1': 11, 'fobber_v2': 12,
                 'gameover': 13, 'locky': 14, 'matsnu': 15, 'murofet': 16, 'necurs': 17, 'nymaim': 18, 'pykspa_v1': 19,
                 'pykspa_v2_fake': 20, 'pykspa_v2_real': 21, 'qadars': 22, 'ramnit': 23, 'ranbyus': 24, 'rovnix': 25,
                 'shifu': 26, 'shiotob': 27, 'simda': 28, 'suppobox': 29, 'symmi': 30, 'tinba': 31, 'vawtrak': 32,
                 'virut': 33}
    output_counts = {
        0: 55000, 13: 2500, 26: 2500, 30: 2500, 27: 2500, 17: 2500, 16: 2500, 33: 2500,
        24: 2500, 23: 2500, 28: 2500, 19: 2500, 31: 2500, 25: 2500, 8: 2500, 1: 2500,
        29: 2234, 22: 2000, 14: 1158, 5: 1000, 3: 1000, 7: 1000, 2: 1000, 15: 908,
        32: 828, 20: 800, 6: 742, 9: 500, 4: 495, 18: 330, 12: 300, 11: 299, 10: 247, 21: 200
    }
    x, y, vocab_size, labels_size, index2char, idx2label, char2index = load_data()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # 转化为tensor
    x_train = torch.from_numpy(x_train).to(torch.int32)
    y_train = torch.from_numpy(y_train).to(torch.float32)
    x_test = torch.from_numpy(x_test).to(torch.int32)
    y_test = torch.from_numpy(y_test).to(torch.float32)

    # 形成训练数据集、测试数据集
    train_data = TensorDataset(x_train, y_train)
    test_data = TensorDataset(x_test, y_test)

    # 使用dataloader进行分批打包
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True, drop_last=True)
    test_loader = torch.utils.data.DataLoader(test_data, batch_size=batch_size, shuffle=False, drop_last=True)

    # 模型构建
    model = Transformer(vocab_size, embedding_dim, labels_size)
    # 优化器
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=20, gamma=0.5)
    # 多项式分类损失函数
    criterion = nn.CrossEntropyLoss()

    model.to(device)
    # 能够计算所有数的平均值和标准差
    loss_meter = meter.AverageValueMeter()

    best_acc = 0  # 保存最好的准确率
    best_model = None  # 保存最好准确率对应的模型参数

    if os.path.exists(model_path):
        model.eval()
        model.load_state_dict(torch.load(model_path))
        # input_url = input("输入域名进行检测")
        #
        # input_url = use_model_data(input_url, char2index)


    else:
        losses = train(model, optimizer, loss_meter, epochs, logpath)
        torch.save(model.state_dict(), model_path)

        loss_value_plot(losses)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params}")


    summary(model)
    test(model)
