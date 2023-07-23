import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.models as models
from torch.utils.data import random_split
from torchvision import transforms
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import random
import os


def classify(URL):
    # Load the model
    model = torch.load('./garbage_classification.pth')

    # Get image from server hosted by the quickcapture
    response = requests.get(URL)
    image = Image.open(BytesIO(response.content))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    ])

    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor.to(device))
    probs = torch.softmax(output, dim=1)

    pred_class = torch.argmax(probs).item()

    class_names = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

    return class_names[pred_class]


