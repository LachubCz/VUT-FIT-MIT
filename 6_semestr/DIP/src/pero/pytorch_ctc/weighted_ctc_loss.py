import torch
from torch.nn.modules.loss import _Loss


class WeightedCTCLoss(_Loss):
    def __init__(self, blank=0, zero_infinity=True):
        super().__init__(reduction='none')
        self.blank = blank
        self.zero_infinity = zero_infinity
        self.ctc_loss = torch.nn.CTCLoss(blank=self.blank, reduction='none', zero_infinity=self.zero_infinity)

    def forward(self, log_probs, targets, input_lengths, target_lengths, weights):
        return self.ctc_loss(log_probs, targets, input_lengths, target_lengths) * weights


if __name__ == '__main__':
    import torch
    # Target are to be padded
    T = 50      # Input sequence length
    C = 20      # Number of classes (including blank)
    N = 16      # Batch size
    S = 30      # Target sequence length of longest target in batch (padding length)
    S_min = 10  # Minimum target length, for demonstration purposes

    # Initialize random batch of input vectors, for *size = (T,N,C)
    input = torch.randn(T, N, C).log_softmax(2).detach().requires_grad_()

    # Initialize random batch of targets (0 = blank, 1:C = classes)
    target = torch.randint(low=1, high=C, size=(N, S), dtype=torch.long)

    input_lengths = torch.full(size=(N,), fill_value=T, dtype=torch.long)
    target_lengths = torch.randint(low=S_min, high=S, size=(N,), dtype=torch.long)

    ctc_loss = WeightedCTCLoss(zero_infinity=True)

    weights = torch.empty(N).uniform_(0, 1)

    loss = ctc_loss(input, target, input_lengths, target_lengths, weights)
    loss.mean().backward()
