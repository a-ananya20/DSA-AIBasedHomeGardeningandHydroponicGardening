# chatbot_engine.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.response = None

class ChatbotTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, keyword, response):
        node = self.root
        for char in keyword.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.response = response

    def search(self, query):
        query = query.lower()
        for i in range(len(query)):
            node = self.root
            j = i
            while j < len(query) and query[j] in node.children:
                node = node.children[query[j]]
                if node.response:
                    return node.response
                j += 1
        return None


# 🧪 Insert hydroponic-specific responses
chatbot_trie = ChatbotTrie()
chatbot_trie.insert("nutrient", "Maintain pH between 5.5-6.5. Essential nutrients include NPK and micronutrients.")
chatbot_trie.insert("ph", "Ideal pH is 5.5 to 6.5. Adjust with pH up/down solutions.")
chatbot_trie.insert("light", "Use LED grow lights for 14-16 hours daily.")
chatbot_trie.insert("temperature", "Keep water temperature between 18-24°C (65-75°F).")
chatbot_trie.insert("system", "DWC, NFT, and Ebb & Flow are common hydroponic systems.")
chatbot_trie.insert("plant", "Great starter plants include lettuce, basil, and spinach.")
chatbot_trie.insert("water", "Change nutrient solution every 1-2 weeks and monitor daily.")
chatbot_trie.insert("problem", "Watch out for root rot, algae, and nutrient imbalance.")

# 📊 Graph-based (tree) conversation flow
conversation_graph = {
    "start": {
        "question": "What do you want help with in hydroponic gardening?",
        "options": {
            "Nutrient Solution": "nutrient_help",
            "Lighting": "lighting_help",
            "System Types": "system_help",
            "Common Problems": "problem_help"
        }
    },
    "nutrient_help": {
        "response": "Maintain pH 5.5-6.5. Use NPK and micronutrients like iron, calcium."
    },
    "lighting_help": {
        "response": "LED grow lights are ideal. Use 14-16 hours/day for most plants."
    },
    "system_help": {
        "response": "Explore DWC for simplicity, NFT for flow, and Ebb & Flow for control."
    },
    "problem_help": {
        "response": "Common issues: root rot, pH imbalance, and clogged pumps. Keep checking water and roots regularly."
    }
}


# chatbot_engine.py (continued)

def get_bot_responses(user_input, current_node=None):
    user_input = user_input.strip()

    if user_input.lower() in ["reset", "start over"]:
        start_node = conversation_graph["start"]
        return "Conversation restarted. " + start_node["question"], "start", start_node["options"]

    # Tree logic
    if current_node in conversation_graph:
        node_data = conversation_graph[current_node]
        options = node_data.get("options", {})

        for key in options:
            if user_input.lower() == key.lower():
                next_node_key = options[key]
                next_node = conversation_graph[next_node_key]

                if "response" in next_node:
                    return next_node["response"], "start", conversation_graph["start"]["options"]
                elif "question" in next_node:
                    return next_node["question"], next_node_key, next_node.get("options", {})

    # Try Trie
    trie_response = chatbot_trie.search(user_input)
    if trie_response:
        return trie_response, current_node, {}

    # Fallback: Return current question and options anyway
    if current_node in conversation_graph:
        question = conversation_graph[current_node].get("question", "What would you like to know?")
        options = conversation_graph[current_node].get("options", {})
        fallback_options = options if options else conversation_graph["start"].get("options", {})
        return f"Here's what I can help with: {question}", current_node, fallback_options

    return "Sorry, I couldn't understand that. Try asking about nutrients, pH, or lighting.", "start", conversation_graph["start"]["options"]
