from transformers import pipeline

class DistilBert:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            "typeform/distilbert-base-uncased-mnli"
        )

    def sentiment_analysis(self, text):
        labels = ["Sport", "Finance", "Health"]
        result = self.classifier(text, candidate_labels=labels)
        return result

def main():
    analyzer = DistilBert()
    sentiment = analyzer.sentiment_analysis(
        "Exercise keeps your body strong and your mind healthy."
    )
    print(sentiment)

if __name__ == "__main__":
    main()
