# garden_assistant/chatbot_engine.py

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


# 🌿 Graph-based flow
conversation_graph = {
    "start": {
        "question": "",
        "options": {
            "Plant Care": "plant_care",
            "Pests or Diseases": "pest_disease",
            "Soil & Fertilizers": "soil_fertilizers",
            "Watering Schedule": "watering_schedule",
            "Sunlight Requirements": "sunlight_needs",
            "Indoor vs Outdoor Plants": "indoor_outdoor",
            "Composting Tips": "composting_tips",

        }
    },
    "plant_care": {
        "question": "What plant are you growing?",
        "options": {
            "Tomato": "tomato_care",
            "Chili": "chili_care",
            "Potato": "potato_care",
        }
    },
    "tomato_care": {
        "response": "Tomatoes love sunlight! Water them consistently and use compost-rich soil."
    },
    "chili_care": {
        "response": "Chili plants need warm weather, avoid overwatering, and prune regularly."
    },
    "potato_care": {
        "response": "Plant potatoes in loose soil and mound soil around the plant as it grows."
    },
    "pest_disease": {
        "response": "Use neem oil or garlic spray to control most garden pests naturally."
    },
   
    "soil_fertilizers": {
        "response": "Use well-draining soil rich in organic matter. Add compost or natural fertilizers for better growth."
    },
    "watering_schedule": {
        "response": "Most plants prefer deep watering 2-3 times a week rather than shallow daily watering."
    },
    "sunlight_needs": {
        "response": "Ensure your plants get 4-6 hours of sunlight daily, but adjust based on plant type."
    },

    "indoor_outdoor": {
        "response": "Indoor plants thrive with indirect sunlight and regular watering. Outdoor plants need more sun and space."
    },
"composting_tips": {
    "response": "Compost kitchen scraps, dry leaves, and garden waste. Avoid dairy, meat, and oily foods."
},


}


# 🌿 Initialize Trie
chatbot_trie = ChatbotTrie()
chatbot_trie.insert("water tomato", "Water tomatoes regularly at the base, not from the top.")
chatbot_trie.insert("neem oil", "Neem oil works great against common garden pests like aphids.")
chatbot_trie.insert("yellow leaves", "Yellow leaves often mean overwatering or nutrient deficiency.")
chatbot_trie.insert("sunlight", "Most vegetables need at least 6 hours of sunlight per day.")
chatbot_trie.insert("potato leaves yellow", "Yellowing potato leaves can be due to lack of nitrogen or overwatering.")
chatbot_trie.insert("tomato plant not growing", "Tomato growth can slow due to lack of sunlight, nutrients, or poor soil drainage.")
chatbot_trie.insert("how to compost at home", "To compost at home, combine green waste like fruit scraps with brown waste like dry leaves and keep it moist and aerated.")
chatbot_trie.insert("best time to plant basil", "Basil grows best in warm weather. Plant it in spring or early summer after the last frost.")
chatbot_trie.insert("can i grow vegetables in pots", "Yes! Many vegetables like tomatoes, peppers, lettuce, and herbs grow well in pots with proper sunlight and watering.")
chatbot_trie.insert("how to save water in gardening", "Use mulch, drip irrigation, and water early in the morning to reduce water loss and promote healthy roots.")
chatbot_trie.insert("what is companion planting", "Companion planting is placing plants together that support each other's growth, like basil with tomatoes to repel pests.")
chatbot_trie.insert("how to make soil fertile", "Add organic compost, rotate crops, and avoid overusing chemical fertilizers to maintain healthy soil.")
chatbot_trie.insert("which vegetables grow fast", "Radishes, lettuce, spinach, and green onions are among the fastest-growing vegetables.")
chatbot_trie.insert("what causes root rot", "Root rot is caused by overwatering and poor drainage. Ensure your soil drains well and don't let roots sit in water.")
chatbot_trie.insert("how to prepare garden for summer", "Add mulch to conserve moisture, check irrigation, and plant heat-tolerant crops like okra and sweet potatoes.")
chatbot_trie.insert("banana peel uses in gardening", "Banana peels are rich in potassium and can be buried in the soil or blended into compost to boost plant growth.")
chatbot_trie.insert("how to start a home garden", "Start small with pots or a raised bed, choose easy-to-grow plants, and ensure they get sunlight and regular watering.")
chatbot_trie.insert("what is the best soil for vegetables", "Loamy soil enriched with compost is ideal for most vegetables. It retains moisture and drains well.")
chatbot_trie.insert("how to keep pests away organically", "Use neem oil, garlic spray, or introduce natural predators like ladybugs to control pests without chemicals.")


# 🌿 Final hybrid response engine
def get_bot_response(user_input, current_node="start"):
    user_input = user_input.strip()

    # 🔁 Reset
    if user_input.lower() in ["reset", "start over"]:
        start_node = conversation_graph["start"]
        return "Conversation restarted. " + start_node["question"], "start", start_node["options"]

    # 🧠 Step 1: Graph node logic
    if current_node in conversation_graph:
        node_data = conversation_graph[current_node]
        options = node_data.get("options", {})

        if user_input in options:
            next_node_key = options[user_input]
            next_node = conversation_graph[next_node_key]
            if "response" in next_node:
                # Show answer and return to start
                return next_node["response"], "start", conversation_graph["start"]["options"]
            elif "question" in next_node:
                return next_node["question"], next_node_key, next_node.get("options", {})

    # 🧠 Step 2: Try Trie
    trie_response = chatbot_trie.search(user_input)
    if trie_response:
        return trie_response, current_node, {}  # no buttons here

    # 🧠 Step 3: Fallback
    if current_node in conversation_graph:
        node_data = conversation_graph[current_node]
        question = node_data.get("question", "What would you like to ask?")
        options = node_data.get("options", {})
        return f" Here's what I can help with:\n{question}", current_node, options

    # 🔁 Unknown fallback
    return "Sorry, something went wrong.", "start", conversation_graph["start"]["options"]
