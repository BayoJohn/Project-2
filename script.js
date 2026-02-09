const API_URL = '/api';
let products = [];
let cart = JSON.parse(localStorage.getItem('cart') || '[]');
let currentCategory = 'all';
let checkoutMode = false;

// Initialize on page load
window.onload = () => {
    loadProducts();
    updateCartCount();
};

// Load products from API
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/products`);
        products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Display products in grid
function displayProducts(productsToShow) {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = productsToShow.map(product => `
        <div class="product-card">
            <img src="${product.image}" alt="${product.name}" class="product-image">
            <div class="product-info">
                <div class="product-category">${product.category}</div>
                <div class="product-name">${product.name}</div>
                <div class="product-description">${product.description}</div>
                <div class="product-rating">${'⭐'.repeat(Math.floor(product.rating))} ${product.rating}</div>
                <div class="stock-info">${product.stock} in stock</div>
                <div class="product-footer">
                    <div class="product-price">$${product.price.toFixed(2)}</div>
                    <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// Filter products by category
function filterByCategory(category) {
    currentCategory = category;
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    const filtered = category === 'all' 
        ? products 
        : products.filter(p => p.category === category);
    displayProducts(filtered);
}

// Search products
function searchProducts() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = products.filter(p => 
        p.name.toLowerCase().includes(query) || 
        p.description.toLowerCase().includes(query)
    );
    displayProducts(filtered);
}

// Add product to cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const cartItem = cart.find(item => item.id === productId);

    if (cartItem) {
        if (cartItem.quantity < product.stock) {
            cartItem.quantity++;
        } else {
            alert('Sorry, not enough stock available');
            return;
        }
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            quantity: 1,
            maxStock: product.stock
        });
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    
    // Visual feedback
    event.target.textContent = 'Added! ✓';
    setTimeout(() => {
        event.target.textContent = 'Add to Cart';
    }, 1000);
}

// Update cart count badge
function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cartCount').textContent = count;
}

// Open cart modal
function openCart() {
    checkoutMode = false;
    displayCart();
    document.getElementById('cartModal').classList.add('active');
}

// Close cart modal
function closeCart() {
    document.getElementById('cartModal').classList.remove('active');
}

// Display cart contents
function displayCart() {
    const cartItemsDiv = document.getElementById('cartItems');
    const totalDiv = document.getElementById('cartTotal');
    const checkoutDiv = document.getElementById('checkoutSection');

    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<div class="empty-cart">Your cart is empty</div>';
        totalDiv.innerHTML = '';
        checkoutDiv.innerHTML = '';
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    cartItemsDiv.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                <div class="quantity-controls">
                    <button class="qty-btn" onclick="updateQuantity(${index}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQuantity(${index}, 1)">+</button>
                </div>
            </div>
            <button class="remove-btn" onclick="removeFromCart(${index})">Remove</button>
        </div>
    `).join('');

    totalDiv.innerHTML = `Total: $${total.toFixed(2)}`;

    if (checkoutMode) {
        checkoutDiv.innerHTML = `
            <div class="checkout-form">
                <input type="text" id="customerName" placeholder="Full Name" required>
                <input type="email" id="customerEmail" placeholder="Email" required>
                <input type="text" id="customerPhone" placeholder="Phone Number" required>
                <input type="text" id="customerAddress" placeholder="Shipping Address" required>
                <button class="checkout-btn" onclick="submitOrder()">Place Order - $${total.toFixed(2)}</button>
            </div>
        `;
    } else {
        checkoutDiv.innerHTML = `
            <button class="checkout-btn" onclick="startCheckout()">Proceed to Checkout</button>
        `;
    }
}

// Update item quantity in cart
function updateQuantity(index, change) {
    const item = cart[index];
    const newQuantity = item.quantity + change;

    if (newQuantity <= 0) {
        removeFromCart(index);
    } else if (newQuantity <= item.maxStock) {
        item.quantity = newQuantity;
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        displayCart();
    } else {
        alert('Sorry, not enough stock available');
    }
}

// Remove item from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    displayCart();
}

// Start checkout process
function startCheckout() {
    checkoutMode = true;
    displayCart();
}

// Submit order to backend
async function submitOrder() {
    const name = document.getElementById('customerName').value.trim();
    const email = document.getElementById('customerEmail').value.trim();
    const phone = document.getElementById('customerPhone').value.trim();
    const address = document.getElementById('customerAddress').value.trim();

    if (!name || !email || !phone || !address) {
        alert('Please fill in all fields');
        return;
    }

    const orderData = {
        customer_name: name,
        customer_email: email,
        customer_phone: phone,
        customer_address: address,
        items: cart.map(item => ({
            product_id: item.id,
            quantity: item.quantity
        }))
    };

    try {
        const response = await fetch(`${API_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });

        if (!response.ok) {
            throw new Error('Order failed');
        }

        const order = await response.json();
        
        // Clear cart
        cart = [];
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();

        // Show success message
        document.getElementById('cartItems').innerHTML = `
            <div class="success-message">
                <h2>Order Placed Successfully! 🎉</h2>
                <p>Order ID: #${order.id}</p>
                <p>Total: $${order.total.toFixed(2)}</p>
                <p>A confirmation email has been sent to ${order.customer_email}</p>
            </div>
        `;
        document.getElementById('cartTotal').innerHTML = '';
        document.getElementById('checkoutSection').innerHTML = '';

        // Reload products to update stock
        loadProducts();
    } catch (error) {
        console.error('Error placing order:', error);
        alert('Failed to place order. Please try again.');
    }
}
