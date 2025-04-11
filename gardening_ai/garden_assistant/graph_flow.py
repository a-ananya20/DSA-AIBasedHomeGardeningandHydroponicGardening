# graph_flow.py

class GraphNode:
    def __init__(self, question, options=None):
        self.question = question
        self.options = options or {}  # key: option_text, value: next_node

class GraphFlow:
    def __init__(self):
        self.nodes = {}
        self.current_node = None
        self.build_graph()

    def build_graph(self):
        # Sample flow for gardening
        self.nodes['start'] = GraphNode("What help do you need today?", {
            "Composting": "compost",
            "Plant Care": "plant_care",
            "Pest Control": "pest_control"
        })

        self.nodes['compost'] = GraphNode("Do you want to compost kitchen or garden waste?", {
            "Kitchen Waste": "kitchen",
            "Garden Waste": "garden"
        })

        self.nodes['plant_care'] = GraphNode("Are you looking for seasonal or general plant care?", {
            "Seasonal": "seasonal_care",
            "General": "general_care"
        })

        self.nodes['pest_control'] = GraphNode("Do you need help identifying pests or using remedies?", {
            "Identifying Pests": "identify_pests",
            "Using Remedies": "use_remedies"
        })

        # Leaf responses
        self.nodes['kitchen'] = GraphNode("Use vegetable peels, coffee grounds, and eggshells.")
        self.nodes['garden'] = GraphNode("Use dry leaves, grass clippings, and small branches.")
        self.nodes['seasonal_care'] = GraphNode("Here are seasonal care tips for your region...")
        self.nodes['general_care'] = GraphNode("General care includes watering, sunlight, pruning...")
        self.nodes['identify_pests'] = GraphNode("Look for bite marks, color changes, and sticky residue.")
        self.nodes['use_remedies'] = GraphNode("Try neem oil spray or insecticidal soap.")

        # Set start node
        self.current_node = self.nodes['start']

    def get_current_question(self):
        return self.current_node.question, list(self.current_node.options.keys())

    def select_option(self, option):
        if option in self.current_node.options:
            next_node_key = self.current_node.options[option]
            self.current_node = self.nodes[next_node_key]
            return self.get_current_question()
        else:
            return "Invalid option. Please select one of the available options.", []

    def is_leaf(self):
        return len(self.current_node.options) == 0

    # ✅ Extra for integration with chatbot_engine
    def get_node(self, node_id):
        return self.nodes.get(node_id)

    def get_question(self, node_id):
        node = self.get_node(node_id)
        if not node:
            return "Sorry, I couldn’t find that topic."
        if not node.options:
            return node.question  # Leaf response
        else:
            question = node.question
            options = list(node.options.keys())
            return f"{question} Options: {', '.join(options)}"
