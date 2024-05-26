import torch
from transformers import BertModel, BertTokenizer


class BertModelWrapper:
    def __init__(self, model_name: str = "dccuchile/bert-base-spanish-wwm-cased"):
        self.tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=False)
        self.model = BertModel.from_pretrained(model_name)

    def get_embedding(self, text: str):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the mean pooled embedding
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings[0].numpy()

    def get_word_tags(self, text: str):
        """
        Get the word tags from the BERT model.
        Args:
            text: Text to analyze
        Returns: List of tuples with the word and its tag
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Get the mean pooled embedding
        embeddings = outputs.last_hidden_state.mean(dim=1)

        return embeddings[0].numpy()
