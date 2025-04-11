# trie_search.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.response = None

class TrieSearch:
    def __init__(self):
        self.root = TrieNode()
        self.build_trie()

    def insert(self, keyword, response):
        node = self.root
        for char in keyword.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.response = response

    def search(self, query):
        node = self.root
        for char in query.lower():
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.response if node.is_end else None

    def build_trie(self):
        # Add sample entries
        self.insert("how to compost at home", "Use kitchen waste and dry leaves, keep moist and turn weekly.")
        self.insert("yellow leaves", "Yellow leaves can mean overwatering or nutrient deficiency.")
        self.insert("neem oil", "Neem oil helps fight pests like aphids and spider mites.")
        self.insert("sunlight needs", "Most vegetables need 6–8 hours of sunlight per day.")
        self.insert("best time to plant basil", "Plant basil in warm weather after the last frost.")
