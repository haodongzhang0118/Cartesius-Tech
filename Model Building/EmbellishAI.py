"""
This code is for training a T5 model to embellish text by processing the input in smaller chunks and combining the
results. The script imports necessary libraries, loads the T5 model and tokenizer, prepares the dataset, sets up
training arguments, trains the model using the Trainer class, and defines a function to use the model for embellishing
sentences.
"""

import torch
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, get_scheduler, TrainerCallback

# Check if GPU is available and set the device accordingly
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the T5 model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("t5_based")
model.to(device)
tokenizer = T5Tokenizer.from_pretrained("t5_based")

# Prepare the dataset and split it into train and validation sets
datasets = [{"input": "", "target": ""}]  # the dataset should be in this format
train, val = train_test_split(datasets, test_size=0.2)


def tokenize_data(data, tokenizer, max_length=512, max_target_length=512):
    """
    Tokenize the input and target data using the given tokenizer.
    """
    return tokenizer.prepare_seq2seq_batch(
        ["embellish: " + item["input"] for item in data],
        tgt_texts=[item["target"] for item in data],
        max_length=max_length,
        max_target_length=max_target_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )


class PrintLossCallback(TrainerCallback):
    def on_epoch_end(self, args, state, control, logs=None, **kwargs):
        current_epoch = (state.global_step / state.max_steps) * args.num_train_epochs
        print(f"Epoch {current_epoch:.0f} - Loss: {logs['loss']:.4f}")


train_tokenize = tokenize_data(train, tokenizer)
val_tokenize = tokenize_data(val, tokenizer)

# Set up training arguments
args = TrainingArguments(
    output_dir="./EmbellishAI_model",
    num_train_epochs=20,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    logging_dir="./EmbellishAI_logs",
    logging_steps=500,
    eval_steps=500,
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    learning_rate=5e-5,
    warmup_ratio=0.15,
    lr_scheduler_type=get_scheduler("linear")
)

# Initialize the Trainer with the model and training arguments
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_tokenize,
    eval_dataset=val_tokenize,
    callbacks=[PrintLossCallback()]
)

# Train the model
trainer.train()


def embellish_sentence(sentence, model, tokenizer, chunk_size=200, overlap=50):
    """
    Embellish a given sentence by processing it in smaller chunks and
    combining the embellished chunks.
    """
    tokens = tokenizer.tokenize(sentence)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(tokenizer.convert_tokens_to_string(chunk))

    embellished_chunks = []
    for chunk in chunks:
        input_text = f"embellish: {chunk}"
        input_tokenized = tokenizer.encode(input_text, return_tensors="pt")
        output_tokens = model.generate(input_tokenized, max_length=chunk_size + overlap, num_return_sequences=1)
        embellished_chunk = tokenizer.decode(output_tokens[0], skip_special_tokens=True)
        embellished_chunks.append(embellished_chunk)

    embellished_sentence = " ".join(embellished_chunks)
    return embellished_sentence

