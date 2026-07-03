
class VectorMemory:

    def __init__(self):
        self.store = []

    def add(self, text):
        self.store.append(text)

    def search(self, query):

        results = []

        for item in self.store:

            if any(
                word.lower() in item.lower()
                for word in query.split()
            ):
                results.append(item)

        return results[:3]
