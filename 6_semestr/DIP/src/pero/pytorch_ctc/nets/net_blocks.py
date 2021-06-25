import torch
from torch import nn


class MultiscaleRecurrentBlock(nn.Module):
    def __init__(self, channels, layers_per_scale=2, scales=4):
        super(MultiscaleRecurrentBlock, self).__init__()

        self.layers = nn.ModuleList([torch.nn.LSTM(channels, channels // 2, num_layers=layers_per_scale, bidirectional=True)
                  for scale in range(scales)])

        self.final_layer = torch.nn.LSTM(channels, channels // 2, num_layers=1, bidirectional=True)

    def forward(self, x):
        outputs = []
        for depth, layer in enumerate(self.layers):
            if depth == 0:
                scaled_data = x
            else:
                scaled_data = torch.nn.functional.max_pool1d(scaled_data, kernel_size=2, stride=2)

            out, _ = layer(scaled_data.permute(2, 0, 1))
            out = out.permute(1, 2, 0)
            if depth != 0:
                out = torch.nn.functional.interpolate(out, scale_factor=2**depth, mode='nearest')
            outputs.append(out)

        out = outputs[0]
        for output in outputs[1:]:
            out = out + output

        out, _ = self.final_layer(out.permute(2, 0, 1))

        return out.permute(1, 2, 0)
