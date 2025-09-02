from tqdm import tqdm
from torchvision import transforms
import torch.nn as nn
import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import seaborn as sns

from loadDataset import CarDataset
from model import CarPartsCNN
from sklearn.metrics import classification_report, multilabel_confusion_matrix

# Training Function
def train_model(model, train_loader, val_loader, epochs=10, device="cpu", save_path="carparts_best.pth"):
    model.to(device)
    best_val_loss = float("inf")

    history = {"train_loss": [], "val_loss": []}

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0

        for imgs, labels in tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs}"):
            imgs, labels = imgs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(imgs)

            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        avg_train_loss = train_loss / len(train_loader)

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                outputs = model(imgs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        avg_val_loss = val_loss / len(val_loader)

        history["train_loss"].append(avg_train_loss)
        history["val_loss"].append(avg_val_loss)

        print(f"Epoch {epoch+1}: Train Loss={avg_train_loss:.4f}, Val Loss={avg_val_loss:.4f}")

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Model terbaik disimpan (Val Loss={best_val_loss:.4f}) ke {save_path}")

    return history


# Evaluation Function
def evaluate_model(model, test_loader, device="cpu", class_names=None, save_path="carparts_best.pth"):
    model.load_state_dict(torch.load(save_path))
    model.to(device)
    model.eval()

    all_labels = []
    all_preds = []

    with torch.no_grad():
        for imgs, labels in test_loader:
            imgs, labels = imgs.to(device), labels.to(device)

            outputs = model(imgs)
            probs = torch.sigmoid(outputs)
            preds = (probs > 0.5).int()

            all_labels.append(labels.cpu())
            all_preds.append(preds.cpu())

    all_labels = torch.cat(all_labels, dim=0).numpy()
    all_preds = torch.cat(all_preds, dim=0).numpy()

    # Classification report
    print("🔹 Classification Report:")
    print(classification_report(all_labels, all_preds, target_names=class_names, zero_division=0))

    # Confusion matrix per kelas
    print("\n🔹 Confusion Matrices per class:")
    conf_matrices = multilabel_confusion_matrix(all_labels, all_preds)

    for idx, cm in enumerate(conf_matrices):
        save_path = f"conf_matrix_{idx}.png"
        
        plt.figure(figsize=(4,3))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                    xticklabels=["Pred 0","Pred 1"], yticklabels=["True 0","True 1"])
        plt.title(f"Confusion Matrix - {class_names[idx]}")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot disimpan di {save_path}")
        plt.show()


# Plot Loss Function
import matplotlib.pyplot as plt

def plot_loss(history, save_path=None):
    plt.figure(figsize=(8, 6))
    plt.plot(history["train_loss"], label="Train Loss")
    plt.plot(history["val_loss"], label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot disimpan di {save_path}")

    plt.show()

# Pipeline
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5])
])

train_dataset = CarDataset("dataset_fix/train", transform=transform)
val_dataset   = CarDataset("dataset_fix/val", transform=transform)
test_dataset  = CarDataset("dataset_fix/test", transform=transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=32, shuffle=False)
test_loader  = DataLoader(test_dataset, batch_size=32, shuffle=False)

model = CarPartsCNN()
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

class_names = ["front_left_open", "front_right_open", 
               "rear_left_open", "rear_right_open", "hood_open"]

history = train_model(model, train_loader, val_loader, epochs=50, device="cuda", save_path="carparts_best.pth")

plot_loss(history, save_path="loss_plot.png")

evaluate_model(model, test_loader, device="cuda" if torch.cuda.is_available() else "cpu", 
               class_names=class_names, save_path="carparts_best.pth")
