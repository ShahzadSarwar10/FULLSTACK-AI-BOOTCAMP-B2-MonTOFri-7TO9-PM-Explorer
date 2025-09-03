import torch
import torch.nn

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Step 1: Load the pre-trained model and tokenizer
from transformers import BertTokenizer, BertForMaskedLM, QLORAdapter

model_name = "bert-base-uncased"
pretrained_model = BertForMaskedLM.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Step 2: Prepare the dataset
texts = ["[CLS] Hello, how are you? [SEP]", "[CLS] I am doing well. [SEP]"]
train_encodings = tokenizer(texts, truncation=True, padding="max_length", return_tensors="pt")
labels = torch.tensor([tokenizer.encode(text, add_special_tokens=True) for text in texts])

# Step 3: Define the QLORAdapter class
adapter = QLORAdapter(input_dim=768, output_dim=768, rank=64)
pretrained_model.bert.encoder.layer[0].attention.output = adapter

# Step 4: Fine-tuning the model
optimizer = torch.optim.AdamW(adapter.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss()

for epoch in range(10):
    optimizer.zero_grad()
    outputs = pretrained_model(**train_encodings.to(device))
    logits = outputs.logits
    loss = loss_fn(logits.view(-1, logits.shape[-1]), labels.view(-1))
    loss.backward()
    optimizer.step()

# Step 5: Inference with the fine-tuned model
test_text = "[CLS] How are you doing today? [SEP]"
test_input = tokenizer(test_text, return_tensors="pt")
output = pretrained_model(**test_input)
predicted_ids = torch.argmax(output.logits, dim=-1)
predicted_text = tokenizer.decode(predicted_ids[0])
print("Predicted text:", predicted_text)    