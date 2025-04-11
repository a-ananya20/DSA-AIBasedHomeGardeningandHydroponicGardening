from django.apps import AppConfig







# Trie implementation
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        curr = self.root
        for char in word.lower():
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end = True

    def search_prefix(self, prefix):
        curr = self.root
        for char in prefix.lower():
            if char not in curr.children:
                return []
            curr = curr.children[char]

        result = []
        self._dfs(curr, prefix.lower(), result)
        return result

    def _dfs(self, node, prefix, result):
        if node.is_end:
            result.append(prefix)
        for char, child in node.children.items():
            self._dfs(child, prefix + char, result)

class GardenAssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garden_assistant'

    def ready(self):
        from .models import Plant
        self.recommend_map = {}  # key = (soil_type_name, season_name), value = list of Plant
        self.trie = Trie()

        for plant in Plant.objects.all():
            for soil in plant.soil_types.all():
                for season in plant.seasons.all():
                    key = (soil.name, season.name)
                    if key not in self.recommend_map:
                        self.recommend_map[key] = []
                    self.recommend_map[key].append(plant)
            self.trie.insert(plant.name)
