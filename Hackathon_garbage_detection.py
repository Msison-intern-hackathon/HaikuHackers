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

    response = requests.get(URL)
    image = Image.open(BytesIO(response.content))
    image_name = URL.split("/")[-1]

    # Define the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define the transformations to be applied to the image
    transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    ])

    # Apply the transformations to the image
    input_tensor = transform(image).unsqueeze(0)

    # Pass the image to the model to get the predicted class
    with torch.no_grad():
        output = model(input_tensor.to(device))

    # Convert the output to a probability distribution
    probs = torch.softmax(output, dim=1)

    # Get the predicted class
    pred_class = torch.argmax(probs).item()

    # Define the class names
    class_names = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

    # Print the predicted class and image name
    return class_names[pred_class]


