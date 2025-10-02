from typing import List
from collections import Counter
from src.app.interfaces import KeywordExtractorInterface


class KeywordExtractor(KeywordExtractorInterface):

    def extract(self, text: str, num_keywords: int = 3) -> List[str]:
        """A simple, non-LLM method to extract keywords using manual heuristics."""

        # Stop Word List for articles and general prose
        stop_words = {
            'a', 'an', 'the', 'and', 'in', 'is', 'it', 'of', 'on', 'for', 'with',
            'was', 'as', 'at', 'by', 'but', 'or', 'to', 'if', 'this', 'that',

            'i', 'me', 'my', 'you', 'your', 'we', 'our', 'us', 'he', 'him',
            'she', 'her', 'they', 'them', 'their', 'be', 'been', 'have', 'has',
            'had', 'do', 'does', 'did', 'am', 'are', 'were', 'being', 'can',
            'could', 'would', 'should',

            'about', 'above', 'after', 'again', 'all', 'any', 'because', 'before',
            'both', 'down', 'each', 'few', 'from', 'into', 'just', 'more', 'most',
            'must', 'not', 'no', 'only', 'other', 'out', 'over', 'so', 'than',
            'then', 'there', 'too', 'under', 'until', 'up', 'very', 'what',
            'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will',
            'yourselves', 'itself', 'herself', 'himself', 'themselves', 'such'
        }

        words = [word.strip(".,!?'\"") for word in text.lower().split()]

        non_stop_words = [
            word for word in words
            if word not in stop_words and len(word) > 2 and word.isalpha()
        ]

        return [word for word, count in Counter(non_stop_words).most_common(num_keywords)]