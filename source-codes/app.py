from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

def load_menu():
    with open('menu.json', 'r') as f:
        return json.load(f)['items']

MENU_ITEMS = load_menu()

class ChatbotEngine:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.cart = []

    def normalize_text(self, text):
        return text.lower().strip()

    def detect_intent(self, text):
        text = self.normalize_text(text)

        if any(k in text for k in ['menu', 'show menu']):
            return 'show_menu'
        if any(k in text for k in ['add', 'order']):
            return 'add_item'
        if any(k in text for k in ['cart']):
            return 'view_cart'
        if any(k in text for k in ['checkout', 'pay']):
            return 'checkout'
        return 'unknown'

    def find_item(self, text):
        text = self.normalize_text(text)
        for item in self.menu_items:
            if item['name'].lower() in text:
                return item
        return None

    def generate_response(self, user_input, cart):
        self.cart = cart
        intent = self.detect_intent(user_input)

        if intent == 'show_menu':
            menu = "\n".join(f"{i['name']} - ${i['price']}" for i in self.menu_items)
            return {'message': f"Menu:\n{menu}", 'cart': self.cart}

        if intent == 'add_item':
            item = self.find_item(user_input)
            if item:
                self.cart.append(item)
                return {'message': f"Added {item['name']}", 'cart': self.cart}

        if intent == 'view_cart':
            total = sum(i['price'] for i in self.cart)
            return {'message': f"Total: ${total}", 'cart': self.cart}

        if intent == 'checkout':
            total = sum(i['price'] for i in self.cart)
            self.cart = []
            return {'message': f"Paid ${total}", 'cart': []}

        return {'message': "Try: menu, add burger, cart, checkout", 'cart': self.cart}

chatbot = ChatbotEngine(MENU_ITEMS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    result = chatbot.generate_response(data['message'], data.get('cart', []))
    return jsonify(result)

@app.route('/menu')
def menu():
    return jsonify({'items': MENU_ITEMS})

if __name__ == '__main__':
    app.run(debug=True)
