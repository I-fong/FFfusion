from sentence_transformers import SentenceTransformer, util
import numpy as np
import requests
import json


class EmbeddingModel:
    def __init__(self):
        self.embedder = SentenceTransformer("jhgan/ko-sbert-nli")
        self.corpus = load_text_data()  # captioning data
        self.corpus_embeddings = [self.embedder.encode(self.corpus[idx], convert_to_tensor=True) for idx in self.corpus]
        self.corpus_index = [idx for idx in self.corpus]
        self.top_k = 4

    def inference(self, query) -> list:
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        cos_scores = [util.pytorch_cos_sim(query_embedding, emb)[0].cpu().item() for emb in self.corpus_embeddings]
        top_results = np.argpartition(-np.array(cos_scores), range(self.top_k))[:self.top_k]
        labels = [self.corpus_index[idx] for idx in top_results]

        return labels


def load_text_data() -> dict:
    s3_json_url = "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com/corpus_data.json"

    try:
        response = requests.get(s3_json_url)
        corpus_data = response.json()

    except Exception as e:
        print(f"파일을 읽는 동안 오류가 발생했습니다: {e}")

    return corpus_data


def add_img_path(labels: list) -> dict:
    s3_bucket_url = "https://ifong-image-data.s3.ap-northeast-2.amazonaws.com"
    image_paths = []

    for label in labels:
        image_paths.append(f"{s3_bucket_url}/{label}.png")

    context = {
        'image_paths': image_paths,
    }

    return context
