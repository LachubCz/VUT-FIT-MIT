import torch
import numpy as np
from sklearn.linear_model import LinearRegression


def build_optimizer(name, net, lr):
    if name == "Adam":
        optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    elif name == "SGD":
        optimizer = torch.optim.SGD(net.parameters(), lr=lr)
    else:
        raise Exception(f'Not implemented optimizer: "{name}"')
    return optimizer


class HonzaSchleduler:
    def __init__(self, optimizer, base_lr, warm_up_iterations, warm_up_polynomial_order):
        self.optimizer = optimizer
        self.base_lr = base_lr
        self.last_learning_rate = None

        self.warm_up_iterations = warm_up_iterations
        self.warm_up_polynomial_order = warm_up_polynomial_order

    def update_learning_rate(self, iteration_count):
        if self.warm_up_iterations is None or self.warm_up_polynomial_order is None:
            self.last_learning_rate = self.base_lr

        if iteration_count <= self.warm_up_iterations and self.warm_up_iterations > 0:
            lr = ((iteration_count / self.warm_up_iterations) ** self.warm_up_polynomial_order) * self.base_lr
        else:
            lr = self.base_lr

        set_single_lr(self.optimizer, lr)
        self.last_learning_rate = lr

    @property
    def act_lr(self):
        return self.last_learning_rate


def set_single_lr(optimizer, lr):
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class PlateauLRReducer:
    def __init__(self, patience, decay_factor, base_scheduler, cooldown=None):
        '''If no improvement for `patience` steps, multiply base_lr of `base_scheduler` by `decay_factor`'''

        if cooldown is None:
            cooldown = patience

        self.base_scheduler = base_scheduler
        self.patience = patience
        self.decay_factor = decay_factor
        self.base_cooldown = cooldown
        self.cooldown = cooldown

        self.has_reduced = False

        self.losses = [float('inf')]

    def step(self, loss):
        best_loss = min(self.losses)
        self.cooldown = max(self.cooldown-1, 0)

        if loss >= best_loss:
            no_improvement_period = len(self.losses) - self.losses.index(best_loss) - 1
            if no_improvement_period > self.patience and not self.cooldown:
                self.cooldown = self.base_cooldown
                self.base_scheduler.base_lr *= self.decay_factor
                print(f'Loss has not improved in the last {no_improvement_period} steps, reducing LR to {self.base_scheduler.base_lr}')
                self.has_reduced = True

        self.losses.append(loss)


class InterpolatingLRReducer:
    def __init__(self, threshold, cooldown, decay_factor, base_scheduler):
        '''If slope of losses after `cooldown` step rises to `threshold`,
           multiply base_lr of `base_scheduler` by `decay_factor`
        '''

        if threshold >= 0.0:
            raise ValueError(f"Threshold has to be negative, got {threshold} (loss minimization is assumed).")
        self.threshold = threshold

        self.base_scheduler = base_scheduler
        self.decay_factor = decay_factor

        if cooldown < 2:
            raise ValueError(f"Cooldown has to be at least 2, so that there are 2 points to calculate slope from, got {cooldown}")

        self.base_cooldown = cooldown
        self.cooldown = cooldown

        self.has_reduced = False

        self.losses = []
        self.regr = LinearRegression()

    def step(self, loss):
        self.losses.append(loss)

        self.cooldown = max(self.cooldown-1, 0)
        if self.cooldown > 0:
            return

        assert(len(self.losses) >= 2)

        X = np.expand_dims(np.arange(len(self.losses)), -1)
        y = np.asarray(self.losses)
        self.regr.fit(X, y)
        slope = self.regr.coef_[0]

        if slope > self.threshold:  # less is better, steep decrease
            self.cooldown = self.base_cooldown
            self.base_scheduler.base_lr *= self.decay_factor
            print(f'Loss slope has grown to {slope}, reducing LR to {self.base_scheduler.base_lr}')
            self.has_reduced = True
            self.losses = []


class NOPReducer:
    def __init__(self):
        self.has_reduced = False

    def step(self, loss):
        pass
