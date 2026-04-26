from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret-key"

# Sample product catalog for the skincare brand
products = [
    {
        "id": "cleanser",
        "name": "Velvet Glow Cleanser",
        "price": 799,
        "short": "A gentle daily cleanser for soft, radiant skin.",
        "description": "Luxurious foam removes impurities while preserving skin moisture. Formulated with calming botanical extracts for a fresh, balanced finish.",
        "ingredients": ["Aloe vera", "Chamomile extract", "Hyaluronic acid", "Rice water"],
        "image": "cleanser.svg",
        "category": "Cleanser"
    },
    {
        "id": "serum",
        "name": "Luminous Serum",
        "price": 1499,
        "short": "A brightening serum that refines texture and glow.",
        "description": "Lightweight serum infused with niacinamide and vitamin C to illuminate and strengthen skin from the first use.",
        "ingredients": ["Niacinamide", "Vitamin C", "Peptides", "Green tea"],
        "image": "serum.svg",
        "category": "Serum"
    },
    {
        "id": "moisturizer",
        "name": "Cloud Dew Moisturizer",
        "price": 1299,
        "short": "A hydrating cream for dewy, supple skin.",
        "description": "Rich yet breathable moisturizer that softens and protects with skin-loving ceramides and nourishing oils.",
        "ingredients": ["Squalane", "Ceramides", "Jojoba oil", "Shea butter"],
        "image": "moisturizer.svg",
        "category": "Moisturizer"
    }
]

# Helper functions

def get_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)


def get_cart_items():
    cart = session.get("cart", [])
    items = []
    for item_id in cart:
        product = get_product(item_id)
        if product:
            items.append(product)
    return items


def get_cart_total(cart_items):
    return sum(item["price"] for item in cart_items)


# Routes
@app.route("/")
def home():
    featured = products
    return render_template("home.html", featured=featured)


@app.route("/shop")
def shop():
    category = request.args.get("category")
    visible_products = [p for p in products if p["category"] == category] if category else products
    categories = sorted({p["category"] for p in products})
    return render_template("shop.html", products=visible_products, categories=categories, active_category=category)


@app.route("/product/<product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("shop"))
    return render_template("product.html", product=product)


@app.route("/add-to-cart/<product_id>")
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("shop"))

    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart
    flash(f"Added {product['name']} to your cart.", "success")
    return redirect(request.referrer or url_for("shop"))


@app.route("/remove-from-cart/<product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    if product_id in cart:
        cart.remove(product_id)
        session["cart"] = cart
        product = get_product(product_id)
        if product:
            flash(f"Removed {product['name']} from the cart.", "success")
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    items = get_cart_items()
    total = get_cart_total(items)
    return render_template("cart.html", items=items, total=total)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please complete all fields before sending your message.", "error")
        else:
            flash("Thank you for reaching out! We will respond soon.", "success")
            return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
