class Retriever:
    def search(self, query):
        return [
            {"text": f"knowledge for {query}"},
            {"text": "general context chunk"}
        ]
