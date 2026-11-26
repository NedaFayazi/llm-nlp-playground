# llm-nlp-playground

Small Python experiments with LLMs and NLP models:

- **CLI chatbot**: talks to an LLM through OpenRouter, streams responses in real time, and keeps the context small by summarizing older messages.
- **Zero-shot topic classification**: classifies text into Sport, Finance or Health with DistilBERT (Hugging Face `transformers` pipeline).
- **Few-shot sentiment analysis**: labels text as positive, negative or neutral by prompting an LLM with a few examples.