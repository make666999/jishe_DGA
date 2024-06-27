import math
import os
import time
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.ao.quantization import QConfigMapping, \
    float_qparams_weight_only_qconfig, default_dynamic_qconfig, get_default_qconfig, default_dynamic_qat_qconfig, \
    default_embedding_qat_qconfig, get_default_qat_qconfig

from torch.ao.quantization.quantize_fx import prepare_fx, convert_fx, prepare_qat_fx

from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
from collections import Counter
import pandas as pd
import numpy as np
from torchnet import meter
import copy


# 统计字符函数
def count_characters_in_column(df, column_name):
    data = df[column_name]
    all_data = ''.join(data)
    char_counts = Counter(all_data)
    return char_counts


# 编码和填充函数
def encode_and_pad_column(df, column_name, L, char_index_dict):
    encoded_values = []
    for value in df[column_name]:
        encoded_value = [char_index_dict.get(char, 0) for char in value]
        if len(encoded_value) < L:
            encoded_value += [0] * (L - len(encoded_value))
        else:
            encoded_value = encoded_value[:L]
        encoded_values.append(encoded_value)
    new_column_name = f'encoded_{column_name}'
    df[new_column_name] = encoded_values
    df[new_column_name] = df[new_column_name].apply(lambda x: [float(i) for i in x])
    return df


def train(model, train_loader, criterion, optimizer, epochs, device):
    model.train()
    for epoch in range(epochs):
        for i, (inputs, labels) in enumerate(train_loader):
            print(i)
            inputs, labels = inputs.to(device), labels.to(device).long().view(-1)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (i + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{epochs}], Step [{i + 1}/{len(train_loader)}], Loss: {loss.item():.4f}')


# 测试函数
def test(model, test_loader):
    model.eval()
    total_correct = 0
    total_samples = 0
    start_time = time.time()
    with torch.no_grad():
        for inputs, labels in test_loader:
            labels = labels.long().view(-1).to(device)
            outputs = model(inputs.to(device))
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)

            total_correct += (predicted == labels).sum().item()

    end_time = time.time()
    accuracy = 100 * total_correct / total_samples
    elapsed_time = end_time - start_time
    print(f'Accuracy on test data: {accuracy:.2f}%')
    print(f'Time taken for testing: {elapsed_time:.4f} seconds')


# 测试量化模型函数
def test_quantized(model, test_loader):
    model.eval()
    total_correct = 0
    total_samples = 0
    start_time = time.time()
    with torch.no_grad():
        for inputs, labels in test_loader:
            labels = labels.view(-1)

            inputs.contiguous()

            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)

            total_correct += (predicted == labels).sum().item()

    end_time = time.time()
    accuracy = 100 * total_correct / total_samples
    elapsed_time = end_time - start_time
    print(f'Accuracy on test data: {accuracy:.2f}%')
    print(f'Time taken for testing: {elapsed_time:.4f} seconds')


# 数据加载函数
def load_data():
    df = pd.read_csv(path)

    char_counts_in_url = count_characters_in_column(df, 'url')

    chars = []
    # 打印统计结果，编制每个字符的数字索引(字典)
    for char, _ in char_counts_in_url.items():
        chars.append(char)
    char2index = {char: idx for idx, char in enumerate(chars)}

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
    return x, y, vocab_size, labels_size


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

        x = x + self.pe[:, :256].requires_grad_(False)

        return self.dropout(x)


# 定义Transformer模型
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
        y = x
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
                nn.ReLU(inplace=False)
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
            nn.ReLU(inplace=False)
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

        self.relu = nn.ReLU(inplace=False)
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
def conv_bn1X1(inp, oup, stride=1, leaky=0, padding=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 1, stride, bias=False, padding=padding),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=False)
    )
def conv_bn3X3(inp, oup, padd=0, stride=1, leaky=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 3, stride, padding=padd, bias=False),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=False)
    )


def conv_bn5X5(inp, oup, padd=1, stride=1, leaky=0):
    return nn.Sequential(
        nn.Conv1d(inp, oup, 5, stride, padding=padd, bias=False),
        nn.BatchNorm1d(oup),
        nn.LeakyReLU(negative_slope=leaky, inplace=False)
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

        # up4 = nearest_neighbor_upsample_1d(output_4, 10,10/3)
        up4 = F.interpolate(output_4, size=[output_3.size(2)], mode="nearest")

        up4 = self.channel_4(up4)
        output_3 = output_3 + up4

        output_3 = self.nerge_3(output_3)

        # up3 = nearest_neighbor_upsample_1d(output_3, 20,20/8)

        up3 = F.interpolate(output_3, size=[output_2.size(2)], mode="nearest")

        up3 = self.channel_5(up3)
        output_2 = output_2 + up3

        output_2 = self.nerge_2(output_2)
        # print(22, output_2.shape)
        # up2 = nearest_neighbor_upsample_1d(output_2, 40,40/18)
        #
        up2 = F.interpolate(output_2, size=[output_1.size(2)], mode="nearest")

        up2 = self.channel_6(up2)
        output_1 = output_1 + up2
        output_1 = self.nerge_1(output_1)
        # print(33, output_1.shape)
        out = torch.cat((output_1, output_2, output_3, output_4), dim=2)

        return out


class TransFlexNet(nn.Module):
    def __init__(self, vocab_size, embedding_dim, num_class, feedforward_dim=256, num_head=8,
                 num_layers=1, dropout=0.1, max_len=256):
        super(TransFlexNet, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.positional_encoding = PositionalEncoding(embedding_dim, dropout, max_len)
        self.SKNET = ResNet(SKUnit, [2, 2, 2, 2])
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

        self.fpn_3 = FPN([64, 128, 256, 512], 128, 1)
    def forward(self, x):
        x = x.transpose(0, 1)  # [128, 32]
        x = x.int().contiguous()
        x = self.embedding(x)
        x = self.positional_encoding(x)
        x = self.transformer(x)
        x = x.permute(1, 2, 0)  # torch.Size([256, 64, 40])
        # print(1, x.shape)
        x = self.SKNET(x)
        x = self.fpn_3(x)
        x = self.dropout(x)
        x = self.mlp(x)
        # print(x.shape)
        return x


# 训练函数


# 主函数
if __name__ == '__main__':
    label2idx = {'BENIGN': 0, 'banjori': 1, 'bigviktor': 2, 'chinad': 3, 'conficker': 4, 'cryptolocker': 5,
                 'dircrypt': 6, 'dyre': 7, 'emotet': 8, 'enviserv': 9, 'feodo': 10, 'fobber_v1': 11, 'fobber_v2': 12,
                 'gameover': 13, 'locky': 14, 'matsnu': 15, 'murofet': 16, 'necurs': 17, 'nymaim': 18, 'pykspa_v1': 19,
                 'pykspa_v2_fake': 20, 'pykspa_v2_real': 21, 'qadars': 22, 'ramnit': 23, 'ranbyus': 24, 'rovnix': 25,
                 'shifu': 26, 'shiotob': 27, 'simda': 28, 'suppobox': 29, 'symmi': 30, 'tinba': 31, 'vawtrak': 32,
                 'virut': 33}
    # 设定超参数
    BATCH_SIZE = 256
    EMBEDDING_DIM = 64
    L = 40
    seq_length = L
    input_dim = EMBEDDING_DIM  # 输入维度

    learning_rate = 1e-3
    epochs = 10
    criterion = nn.CrossEntropyLoss()
    loss_meter = meter.AverageValueMeter()
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device("cpu")
    path = "../Data/clean_data/data_all.csv"
    model_path = '../Model_File/TransFlexNet.pth'
    quantized_model_path = "../Model_File/TransFlexNet_PTQ.pth"

    x, y, vocab_size, labels_size = load_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    x_train = torch.from_numpy(x_train).to(torch.float32)
    y_train = torch.from_numpy(y_train).to(torch.float32)
    x_test = torch.from_numpy(x_test).to(torch.float32)
    y_test = torch.from_numpy(y_test).to(torch.float32)

    train_data = TensorDataset(x_train, y_train)
    test_data = TensorDataset(x_test, y_test)

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, drop_last=True)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False, drop_last=True)

    model = TransFlexNet(vocab_size, EMBEDDING_DIM, labels_size).to(device)
    # model.load_state_dict(torch.load(model_path))
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    if os.path.exists(model_path):
        print("Model file found. Loading model and testing...")
        model.load_state_dict(torch.load(model_path))
        test(model, test_loader)
    else:
        print("Model file not found. Training model...")
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        train(model, train_loader, criterion, optimizer, epochs, device)
        torch.save(model.state_dict(), model_path)
        print('Model saved to', model_path)
    device = torch.device("cpu")
    default_static_qconfig = get_default_qconfig('fbgemm')

    qconfig_mapping = (QConfigMapping()
                       # .set_global(default_dynamic_qconfig)
                       .set_object_type(nn.Embedding, default_dynamic_qconfig)
                       .set_object_type(nn.Transformer, default_static_qconfig)
                       .set_object_type(nn.Linear, default_dynamic_qconfig)
                       .set_object_type(nn.Conv1d, default_static_qconfig)
                       .set_object_type(nn.ReLU, default_static_qconfig)
                       .set_object_type(nn.LeakyReLU, default_static_qconfig)
                       .set_object_type(nn.BatchNorm1d, default_static_qconfig)
                       )
    # qconfig_mapping = QConfigMapping().set_global(torch.ao.quantization.default_dynamic_qconfig)
    model_copy = copy.deepcopy(model)
    # model_copy.eval()
    example_inputs = (torch.randint(0, 40, (256, 40)),)

    prepared_model = prepare_fx(model_copy, qconfig_mapping, example_inputs)

    print("训练")
    # train(prepared_model, train_loader, criterion, optimizer, epochs, device)
    def calibrate(model, data_loader):
        model.eval()
        with torch.no_grad():
            for image, target in data_loader:
                model(image)


    calibrate(prepared_model, test_loader)  # 确保模型在评估模式
    prepared_model.to("cpu")
    quantized_model = convert_fx(prepared_model)

    # test_quantized(quantized_model, test_loader)
    torch.jit.save(torch.jit.script(quantized_model), quantized_model_path)  # 保存量化后的模型
    print('Quantized model saved to', quantized_model_path)
    loaded_quantized_model = torch.jit.load(quantized_model_path)


    test_quantized(loaded_quantized_model, test_loader)


    def print_size_of_model(model):
        torch.save(model.state_dict(), "temp.p")
        print('Size (MB):', os.path.getsize("temp.p") / 1e6)
        os.remove('temp.p')


    print_size_of_model(model)
    print_size_of_model(loaded_quantized_model)
