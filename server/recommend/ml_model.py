from sentence_transformers import SentenceTransformer, util
import numpy as np


corpus_data = {
    0: "밤길을 조심하라고 하고 있다.",
    1: "상당히 신나하고 있다.",
    2: "흐하하하 하며 웃고 있다.",
    3: '상황판단을 못한다고 나무라고 있다.',
    4: '일요일은 일하는 날이라고 생각한다.',
    5: '찡긋 하고 있다.',
    6: '오싹하고 무서운 표정을 짓고 있다.',
    7: '상대방이 문제라고 화내고 있다.',
    8: '음식의 맛을 감탄하고 있다.',
    9: '무언가를 똑똑히 보여주려 하고 있다.',
    10: '아부하는 모습을 못마땅해 하고 있다.',
    11: '잠을 잘 못자고 있다.',
    12: '불투명한 미래를 걱정하고 있다.',
    13: '멍한 표정을 하고 있다.',
    14: '주접떠는 모습을 못마땅해 하고 있다.',
    15: '사람들이 반응을 해주지 않아 화를 내고 있다.',
}


class EmbeddingModel:
    def __init__(self):
        self.embedder = SentenceTransformer("jhgan/ko-sbert-sts")

        self.corpus = corpus_data  # captioning data
        self.corpus_embeddings = [self.embedder.encode(self.corpus[idx], convert_to_tensor=True) for idx in self.corpus]

        self.top_k = 5

    def inference(self, query) -> list:
        query_embedding = self.embedder.encode(query, convert_to_tensor=True)
        cos_scores = [util.pytorch_cos_sim(query_embedding, emb)[0].cpu().item() for emb in self.corpus_embeddings]
        top_results = np.argpartition(-np.array(cos_scores), range(self.top_k))[:self.top_k]

        return top_results
