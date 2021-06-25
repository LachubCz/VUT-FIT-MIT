import torch
import torch.nn as nn
import torch.nn.functional as F


class softmax_cross_entropy_with_logits(nn.Module):
    """tf.nn.softmax_cross_entropy_with_logits"""
    def __init__(self):
        super(softmax_cross_entropy_with_logits, self).__init__()

    def forward(self, logits, labels, mask=None):
        if not labels.is_same_size(logits):
            raise ValueError("Target size ({}) must be the same as input size ({})".format(labels.size(), logits.size()))

        logits = F.softmax(logits)
        loss = -torch.sum(labels * torch.log(logits), 1)
        if mask is not None:
            loss = torch.unsqueeze(loss, 1)
            mask /= torch.mean(mask)
            mask = torch.unsqueeze(mask, 1)
            loss = torch.mul(loss, mask)

        return torch.mean(loss)


if __name__ == '__main__':
    logits = [[4.0, 2.0, 1.0], [0.0, 5.0, 1.0]]
    labels = [[1.0, 0.0, 0.0], [0.0, 0.8, 0.2]]

    loss = softmax_cross_entropy_with_logits()
    print(loss(torch.tensor(logits), torch.tensor(labels)))

    import tensorflow as tf
    print(tf.math.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=labels, logits=logits)))
