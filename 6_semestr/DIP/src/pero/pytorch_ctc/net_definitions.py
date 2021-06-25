from functools import partial
from pytorch_ctc.nets.net_michal import NET_VGG_LSTM


net_definitions = {
    'VGG_LSTM_B64_L17_S4_CB4': partial(
        NET_VGG_LSTM, base_channels=64, conv_blocks=4, subsampling=4, layers_2d=17)
}
