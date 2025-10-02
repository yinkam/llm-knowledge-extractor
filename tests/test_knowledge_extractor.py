from src.app.domain.keyword_extractor import KeywordExtractor

def test_keyword_extractor():
    extractor = KeywordExtractor()
    text = "The quick brown fox jumps over the lazy dog. The dog is very lazy."
    keywords = extractor.extract(text)
    assert keywords == ['lazy', 'dog', 'quick']

def test_keyword_extractor_empty_text():
    extractor = KeywordExtractor()
    text = ""
    keywords = extractor.extract(text)
    assert keywords == []
