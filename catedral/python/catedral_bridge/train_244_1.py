import torch
import torch.nn as nn

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 10)
        self.fc2 = nn.Linear(10, 2)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))

def train_and_save():
    print("Training dummy model 244.1...")
    model = DummyModel()
    # Mocking training loop...
    print("Saving checkpoint...")
    torch.save({"model": model.state_dict()}, "checkpoint.pt")
    print("Done.")

if __name__ == "__main__":
    train_and_save()