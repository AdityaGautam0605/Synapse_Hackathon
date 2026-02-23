import torch 

model = torch.load("app/models/lstm_model.pt")
model.eval()

def predict_temporal(sequence_tensor):
    with torch.no_grad():
        output = model(sequence_tensor)
        prob = torch.sigmoid(output).item
        
    return prob