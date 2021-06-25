import torch
from torch import nn
from pytorch_ctc.nets.net_blocks import MultiscaleRecurrentBlock


def create_vgg_block_2d(in_channels, out_channels, stride=(2,2), layer_count=2, norm='bn'):
    layers = []
    for i in range(layer_count):
        if norm == 'bn':
            layers += [
                nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1),
                torch.nn.BatchNorm2d(out_channels),
                torch.nn.LeakyReLU(),
            ]
        elif norm == 'none':
            layers += [
                nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1),
                torch.nn.LeakyReLU(),
            ]
        else:
            print(f'ERROR: Normalization "f{norm}" is not implemented')
            raise "Unknown norm"

        in_channels = out_channels

    layers += [nn.MaxPool2d(kernel_size=stride, stride=stride)]
    return nn.Sequential(*layers)


class VGG_conv_module(nn.Module):
    def __init__(self, base_channels=16, conv_blocks=4, subsampling=4, in_channels=3, layers_2d=None):
        super(VGG_conv_module, self).__init__()
        if layers_2d is None:
            layers_2d = 16

        if type(layers_2d) is int:
            import torchvision
            vgg = torchvision.models.vgg16(pretrained=True)
            layers_2d = list(vgg.features[:layers_2d])

        start_level = 0
        self.blocks_2d = []
        actual_subsampling_h = 1
        actual_subsampling_v = 1
        for layer in layers_2d:
            if type(layer) == torch.nn.modules.pooling.MaxPool2d:
                if actual_subsampling_h < subsampling:
                    stride = (2, 2)
                else:
                    stride = (2, 1)
                self.blocks_2d += [nn.MaxPool2d(kernel_size=stride, stride=stride)]
                actual_subsampling_h *= stride[1]
                actual_subsampling_v *= stride[0]
                start_level += 1
            else:
                self.blocks_2d.append(layer)
                if type(layer) == torch.nn.modules.conv.Conv2d:
                    in_channels = layer.bias.shape[0]

        print('Pretrained layers')
        print(self.blocks_2d)

        out_channels = in_channels
        for i in range(start_level, conv_blocks):
            out_channels = base_channels*(2**i)
            if actual_subsampling_h < subsampling:
                stride = (2, 2)
            else:
                stride = (2, 1)
            actual_subsampling_h *= stride[1]
            actual_subsampling_v *= stride[0]
            self.blocks_2d += [
                create_vgg_block_2d(in_channels, out_channels, stride=stride, norm='none'),
                torch.nn.BatchNorm2d(out_channels),
                ]
            in_channels = out_channels

        self.blocks_2d = nn.Sequential(*self.blocks_2d)
        self.out_channels = out_channels

    def forward(self, x):
        return self.blocks_2d(x)


class Global_Adaptation(nn.Module):
    def __init__(self, in_channels):
        super(Global_Adaptation, self).__init__()
        self.in_channels = in_channels
        self.counter = 0

        self.projection_layer = nn.Conv1d(self.in_channels, self.in_channels, kernel_size=1, stride=2, padding=0, bias=False)
        self.weight_layer = nn.Conv1d(self.in_channels, self.in_channels, kernel_size=1, stride=1, padding=0, bias=True)
        self.weight_layer.bias.data.fill_(4.0)

    def forward(self, input):
        x = self.projection_layer(input)
        x = nn.functional.softsign(x)
        x = torch.mean(x, dim=2, keepdim=True)
        x = self.weight_layer(x)
        weights = torch.sigmoid(x)
        self.counter += 1
        if self.counter % 200 == 0:
            print('GA1', weights.shape, [x.item() for x in torch.std_mean(weights)])
            print('GA2', [x.item() for x in torch.std_mean(torch.mean(weights, dim=(0, 2)))])
        return input * weights


class NET_VGG_LSTM(nn.Module):
    def __init__(self, num_classes, in_channels=3, base_channels=16, conv_blocks=4,
                 subsampling=4, layers_2d=None, global_adaptation=False, **kwargs):
        super(NET_VGG_LSTM, self).__init__()
        self.num_classes = num_classes
        self.output_subsampling = subsampling
        self.global_adaptation = global_adaptation

        self.blocks_2d = VGG_conv_module(base_channels=base_channels, conv_blocks=conv_blocks, subsampling=subsampling,
                                         in_channels=in_channels, layers_2d=layers_2d)
        rnn_channels = self.blocks_2d.out_channels
        self.recurrent_block = MultiscaleRecurrentBlock(rnn_channels, layers_per_scale=2, scales=3)
        self.output_layer = nn.Conv1d(rnn_channels, num_classes, kernel_size=3, stride=1, padding=1)
        if self.global_adaptation:
            self.global_adaptation1 = Global_Adaptation(rnn_channels)
            self.global_adaptation2 = Global_Adaptation(rnn_channels)

    def forward(self, x, *args, **kwargs):
        out = self.blocks_2d(x)
        out, _ = torch.max(out, 2)
        if self.global_adaptation:
            out = self.global_adaptation1(out)
        out = self.recurrent_block(out)
        if self.global_adaptation:
            out = self.global_adaptation2(out)
        out = self.output_layer(out)
        return out
