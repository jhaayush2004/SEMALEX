from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import GPT2Tokenizer

class EnhancedEvaluator:
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2', top_n_keywords=50):
        self.model = SentenceTransformer(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.top_n_keywords = top_n_keywords
        
    '''Defining evaluate_semantic_similarity'''
    def evaluate_semantic_similarity(self, reference_text, generated_text):
        reference_embedding = self.model.encode(reference_text).reshape(1, -1)
        generated_embedding = self.model.encode(generated_text).reshape(1, -1)
        similarity_score = cosine_similarity(reference_embedding, generated_embedding)[0][0]
        return similarity_score
    
    def tokenize_text(self, text):
        tokens = self.tokenizer.tokenize(text)
        return list(tokens)
    
    #def topn_keyword(self, reference_token, generated_token):
        top_n_keyword = min(self.top_n_keywords, len(reference_token) // 2, len(generated_token) // 2)
        return top_n_keyword
    
    def compute_tfidf(self, reference_tokens, generated_tokens):
        reference_str = ' '.join(reference_tokens)
        generated_str = ' '.join(generated_tokens)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([reference_str, generated_str])
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = tfidf_matrix.toarray()
        return feature_names, tfidf_scores
    
    def compare_keywords(self, tfidf_scores, feature_names):
        reference_scores = tfidf_scores[0]
        generated_scores = tfidf_scores[1]
        reference_top_indices = reference_scores.argsort()[-self.top_n_keywords:][::-1]
        generated_top_indices = generated_scores.argsort()[-self.top_n_keywords:][::-1]
        reference_top_tokens = [feature_names[i] for i in reference_top_indices]
        generated_top_tokens = [feature_names[i] for i in generated_top_indices]
        #print("Reference top tokens:", reference_top_tokens)
        #print("Generated top tokens:", generated_top_tokens)
        overlap = set(reference_top_tokens) & set(generated_top_tokens)
        overlap_score = len(overlap) / self.top_n_keywords
        #print("Overlap tokens:", overlap)
        #print("Overlap score:", overlap_score)

        return overlap_score
    
    def evaluate_all(self, reference_text, generated_text):
        # Semantic similarity score
        semantic_similarity = self.evaluate_semantic_similarity(reference_text, generated_text)
        
        # TF-IDF keyword matching
        reference_tokens = self.tokenize_text(reference_text)
        generated_tokens = self.tokenize_text(generated_text)
        #n_keyword = int(self.topn_keyword(reference_tokens, generated_tokens))
        feature_names, tfidf_scores = self.compute_tfidf(reference_tokens, generated_tokens)
        keyword_overlap_score = self.compare_keywords(tfidf_scores, feature_names)
        # Introducing weighted_score to give semantic capturing more importance than lexical matching.
        weighted_score = (0.3*keyword_overlap_score + 0.7*semantic_similarity)
        return {
            "SemaLex": weighted_score
            #"keyword_overlap_score": keyword_overlap_score,
            #"semantic_similarity": semantic_similarity
        }

if __name__ == "__main__":
    evaluator = EnhancedEvaluator()
    reference_text = "Human activities such as burning fossil fuels cause climate change."
    generated_text = "There is a huge impact of human activities on climate. Some of these activities are burning fossil fuels, mining and so on."
    metrics = evaluator.evaluate_all(reference_text, generated_text)
    #print(f"Semantic Similarity Score: {metrics['semantic_similarity']}")
    #print(f"Keyword Overlap Score: {metrics['keyword_overlap_score']}")
    print(f"Final Score (SemaLex): {metrics['SemaLex']}")
