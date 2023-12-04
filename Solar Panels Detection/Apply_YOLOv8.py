import pandas as pd
from ultralytics import YOLO

model = YOLO("best_MySolar.pt")

results = model( source="/Users/mashaelalmus/Desktop/Screenshot 2023-11-26 at 8.35.44 AM Large.jpeg" , show =True, conf=0.4, save=True)