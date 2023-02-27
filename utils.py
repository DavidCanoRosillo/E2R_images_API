import torch
import torchvision
from googletrans import Translator

translator = Translator()
class Identity(torch.nn.Module):
    def __init__(self):
        super(Identity, self).__init__()
        
    def forward(self, x):
        return x

class Effnet_based(torch.nn.Module):
    def __init__(self, pretrained):
        super(Effnet_based, self).__init__()
        self.encode = torch.nn.Sequential(
            pretrained,
            torch.nn.Linear(512, 8),
        )

    def forward(self, x):
        y_hat = self.encode(x)
        return y_hat

def load_model(device):
    # load model architecture
    pretrained = torchvision.models.resnet18(pretrained=False)
    pretrained.fc = Identity()
    model = Effnet_based(pretrained).to(device)
    # load weights from training
    checkpoint = torch.load('eff_based', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    # image transformation
    preprocess = torchvision.transforms.Compose([
        #torchvision.transforms.ToPILImage(),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Resize((224, 224)),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    return model, preprocess

def translate(text, src, dest):
    result = translator.translate(text, src=src, dest=dest)
    return result.text.capitalize()