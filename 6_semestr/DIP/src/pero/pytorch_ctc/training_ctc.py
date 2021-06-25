import torch
import os
import numpy as np

from pytorch_ctc.net_definitions import net_definitions
from pytorch_ctc.weighted_ctc_loss import WeightedCTCLoss
from pytorch_ctc.softmax_cross_entropy_with_logits import softmax_cross_entropy_with_logits


class CTCModelWrapper:
    @staticmethod
    def build_model(net, num_output_symbols, input_height, input_channels, dropout_rate=0.0, num_embeddings=None,
                    normalization_scale_std=0.1):
        net = net_definitions[net](
            num_classes=num_output_symbols + 1,
            in_height=input_height,
            in_channels=input_channels,
            dropout_rate=dropout_rate,
            num_embeddings=num_embeddings,
            normalization_scale_std=normalization_scale_std
        )
        return net

    def __init__(self, net, optimizer=None, loss='classic'):
        self.net = net
        self.num_classes = net.num_classes
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if os.environ["CUDA_VISIBLE_DEVICES"] != "":
            print("DEVICE", self.device, torch.cuda.get_device_name(0))
        self.net = self.net.to(self.device)
        if loss == 'classic':
            self.loss = torch.nn.CTCLoss(blank=self.num_classes - 1, reduction='none', zero_infinity=True).to(self.device)
        elif loss == 'weighted':
            self.loss = WeightedCTCLoss(blank=self.num_classes - 1, zero_infinity=True).to(self.device)
        elif loss == 'alignment':
            self.loss = softmax_cross_entropy_with_logits()
            self.test_loss = torch.nn.CTCLoss(blank=self.num_classes - 1, reduction='none', zero_infinity=True).to(self.device)
        self.loss_type = loss
        self.optimizer = optimizer

    def set_train(self):
        self.net = self.net.train()

    def set_eval(self):
        self.net = self.net.eval()

    def train_step(self, batch):
        self.optimizer.zero_grad()
        out, loss = self.forward_pass(batch, loss_batch_ratio=0.99)
        loss.mean().backward()
        self.optimizer.step()
        return out, loss

    def test_step(self, batch):
        out, loss = self.forward_pass(batch, test_step=True)
        return out, loss

    def forward_pass(self, batch, loss_batch_ratio=1, test_step=False):
        inputs = batch['images']
        labels_orig = batch['labels']
        labels = batch['labels_concatenated']
        labels_lengths = batch['labels_lengths']
        ids_embedding = batch['ids_embedding']

        inputs = torch.from_numpy(inputs).to(self.device).float()
        inputs /= 255.0
        labels = torch.from_numpy(labels).type(torch.int32).to(self.device)
        labels_lengths = torch.from_numpy(labels_lengths).type(torch.int32).to(self.device)
        output_lengths = torch.full((inputs.shape[0],), inputs.shape[3] // self.net.output_subsampling,
                                    dtype=torch.int32, device=self.device)
        logits = self.net.forward(inputs, torch.LongTensor(ids_embedding).to(self.device))
        out = torch.nn.functional.log_softmax(logits, dim=1)

        if self.loss_type == 'classic' or (self.loss_type == 'alignment' and test_step):
            if self.loss_type == 'alignment':
                loss = self.test_loss(out.permute(2, 0, 1), labels, output_lengths, target_lengths=labels_lengths)
            else:
                loss = self.loss(out.permute(2, 0, 1), labels, output_lengths, target_lengths=labels_lengths)

            k = max(1, int(loss_batch_ratio * inputs.shape[0]))
            if k < inputs.shape[0]:
                val, _ = torch.kthvalue(loss.detach(), k)
                loss = loss * ((loss < val).float() + 0.05)
            return out, loss

        elif self.loss_type == 'weighted':
            occurences = batch['occurences']
            weights = batch['weights']
            weights = torch.from_numpy(np.array(weights)).to(self.device).float()

            # CTC needs T,N,C, out is N,C,T
            occ = torch.tensor(occurences).long().to(self.device)

            rep_log_probs = torch.repeat_interleave(out.permute(2, 0, 1), occ, dim=1)
            rep_output_lengths = torch.repeat_interleave(output_lengths, occ, dim=0)

            loss = self.loss(log_probs=rep_log_probs, targets=labels, input_lengths=rep_output_lengths, target_lengths=labels_lengths, weights=weights)
            return torch.repeat_interleave(out, occ, dim=0), loss

        elif self.loss_type == 'alignment':
            labels_orig = torch.from_numpy(labels_orig).to(self.device).float()
            logits = out.permute(0, 2, 1)

            #crop to output size
            logit_output_shape = output_lengths[0]
            labels_orig = labels_orig[:,:logit_output_shape,:]

            #extended to output size
            labels = torch.zeros(logits.shape).to(self.device).float()
            labels[:, :, -1] = 1
            labels[:, :labels_orig.shape[1], :] = labels_orig

            labels_orig = torch.flatten(labels, start_dim=0, end_dim=1)
            logits = torch.flatten(logits, start_dim=0, end_dim=1)

            loss = self.loss(logits=logits, labels=labels_orig)

            return out, loss

    def compute_mask(self, inputs):
        mask, _ = torch.max(inputs, dim=1, keepdim=True)
        mask, _ = torch.max(mask, dim=2, keepdim=True)
        mask = torch.min(mask, torch.full(mask.size(), 1).to(self.device).float())
        return mask

    def save_weights(self, path):
        torch.save(self.net.state_dict(), path)

    def load_weights(self, path):
        self.net.load_state_dict(torch.load(path, map_location=self.device))
