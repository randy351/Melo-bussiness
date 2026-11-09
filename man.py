
from flask import Flask, request, render_template_string
import os
from urllib.parse import quote

app = Flask(__name__)

# BUSINESS SETTINGS
BUSINESS_NAME = "MELO FASHION"
WHATSAPP_NUMBER = os.environ.get(
    "WHATSAPP_NUMBER", "254700000000"
)

# PRODUCTS: Edit these to add your own products
products = [
    {
        "name": "Classic T-Shirt",
        "price": 1200,
        "description": "Comfortable everyday fashion."
    },
    {
        "name": "Ladies Dress",
        "price": 2500,
        "description": "Elegant and stylish dress."
    },
    {
        "name": "Designer Shoes",
        "price": 3500,
        "description": "Fashionable everyday shoes."
    },
    {
        "name": "Luxury Handbag",
        "price": 2800,
        "description": "Beautiful handbag for every occasion."
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ business }}</title>
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f7f7f7;
            color: #222;
        }
        header {
            background: #171717;
            color: white;
            padding: 30px 15px;
            text-align: center;
        }
        nav {
            background: #333;
            padding: 15px;
            text-align: center;
        }
        nav a {
            color: white;
            margin: 12px;
            text-decoration: none;
        }
        .hero {
            text-align: center;
            padding: 35px 15px;
            background: #e9dfd5;
        }
        .container {
            max-width: 1000px;
            margin: auto;
            padding: 20px;
        }
        .products {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }
        .product {
            background: white;
            padding: 22px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px #ddd;
        }
        .product h3 {
            color: #8b5e3c;
        }
        .price {
            font-weight: bold;
            font-size: 20px;
        }
        button {
            background: #171717;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #8b5e3c;
        }
        footer {
            background: #171717;
            color: white;
            text-align: center;
            padding: 25px;
            margin-top: 30px;
        }
    </style>
</head>
<body>

<header>
    <h1>{{ business }}</h1>
    <p>Your Style, Your Choice</p>
</header>

<nav>
    <a href="/">Home</a>
    <a href="#products">Products</a>
    <a href="#contact">Contact</a>
</nav>

<section class="hero">
    <h2>Welcome to our online store!</h2>
    <p>Discover quality products at affordable prices.</p>
    <a href="#products">
        <button>Shop Now</button>
    </a>
</section>

<div class="container" id="products">
    <h2>Our Products</h2>

    <div class="products">
        {% for product in products %}
        <div class="product">
            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>
            <p class="price">
                KSh {{ "{:,}".format(product.price) }}
            </p>

            <a href="/order/{{ loop.index0 }}">
                <button>Order Now</button>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<section class="container" id="contact">
    <h2>Contact Us</h2>
    <p>Have a question? Contact our business.</p>
    <a href="https://wa.me/{{ whatsapp }}">
        <button>Chat on WhatsApp</button>
    </a>
</section>

<footer>
    <p>&copy; 2026 {{ business }}.</p>
    <p>Thank you for shopping with us!</p>
</footer>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        business=BUSINESS_NAME,
        products=products,
        whatsapp=WHATSAPP_NUMBER
    )


@app.route("/order/<int:product_id>")
def order(product_id):

    if product_id < 0 or product_id >= len(products):
        return "Product not found", 404

    product = products[product_id]

    message = (
        f"Hello {BUSINESS_NAME}, "
        f"I want to order {product['name']} "
        f"for KSh {product['price']:,}."
    )

    whatsapp_url = (
        f"https://wa.me/{WHATSAPP_NUMBER}"
        f"?text={quote(message)}"
    )

    from flask import redirect
    return redirect(whatsapp_url)


@app.route("/health")
def health():
    return {"status": "online"}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
