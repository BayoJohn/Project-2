from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:securepassword123@localhost:5432/ecommerce")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class ProductDB(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    image = Column(String)
    category = Column(String, index=True)
    stock = Column(Integer)
    rating = Column(Float)

class OrderDB(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_address = Column(Text)
    customer_phone = Column(String)
    total = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship("OrderItemDB", back_populates="order")

class OrderItemDB(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    
    order = relationship("OrderDB", back_populates="items")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str
    category: str
    stock: int
    rating: float

    class Config:
        from_attributes = True

class CartItem(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float

class Order(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    customer_address: str
    customer_phone: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_address: str
    customer_phone: str
    items: List[CartItem]

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize sample data
def init_sample_data():
    db = SessionLocal()
    
    # Check if products already exist
    existing_products = db.query(ProductDB).first()
    if existing_products:
        db.close()
        return
    
    sample_products = [
        ProductDB(
            id=1,
            name="Wireless Headphones",
            description="Premium noise-canceling wireless headphones with 30-hour battery life",
            price=199.99,
            image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop",
            category="Electronics",
            stock=50,
            rating=4.5
        ),
        ProductDB(
            id=2,
            name="Smart Watch",
            description="Fitness tracking smartwatch with heart rate monitor and GPS",
            price=299.99,
            image="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop",
            category="Electronics",
            stock=30,
            rating=4.7
        ),
        ProductDB(
            id=3,
            name="Laptop Backpack",
            description="Water-resistant laptop backpack with USB charging port",
            price=49.99,
            image="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop",
            category="Accessories",
            stock=100,
            rating=4.3
        ),
        ProductDB(
            id=4,
            name="Mechanical Keyboard",
            description="RGB mechanical gaming keyboard with cherry MX switches",
            price=129.99,
            image="https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&h=500&fit=crop",
            category="Electronics",
            stock=45,
            rating=4.6
        ),
        ProductDB(
            id=5,
            name="Coffee Maker",
            description="Programmable coffee maker with thermal carafe",
            price=79.99,
            image="https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=500&h=500&fit=crop",
            category="Home",
            stock=60,
            rating=4.4
        ),
        ProductDB(
            id=6,
            name="Running Shoes",
            description="Lightweight running shoes with superior cushioning",
            price=89.99,
            image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
            category="Fashion",
            stock=75,
            rating=4.8
        ),
        ProductDB(
            id=7,
            name="Desk Lamp",
            description="LED desk lamp with adjustable brightness and color temperature",
            price=39.99,
            image="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&h=500&fit=crop",
            category="Home",
            stock=90,
            rating=4.2
        ),
        ProductDB(
            id=8,
            name="Yoga Mat",
            description="Non-slip yoga mat with carrying strap",
            price=29.99,
            image="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500&h=500&fit=crop",
            category="Fitness",
            stock=120,
            rating=4.5
        )
    ]
    
    db.add_all(sample_products)
    db.commit()
    db.close()

# Initialize data on startup
@app.on_event("startup")
def startup_event():
    init_sample_data()

# API Routes
@app.get("/api/products", response_model=List[Product])
def get_products(category: Optional[str] = None, search: Optional[str] = None):
    db = SessionLocal()
    query = db.query(ProductDB)
    
    if category:
        query = query.filter(ProductDB.category == category)
    
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            (ProductDB.name.ilike(search_term)) | 
            (ProductDB.description.ilike(search_term))
        )
    
    products = query.all()
    db.close()
    return products

@app.get("/api/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    db.close()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/api/categories")
def get_categories():
    db = SessionLocal()
    categories = db.query(ProductDB.category).distinct().all()
    db.close()
    return {"categories": [cat[0] for cat in categories]}

@app.post("/api/orders", response_model=Order)
def create_order(order: OrderCreate):
    db = SessionLocal()
    
    try:
        # Validate cart items and calculate total
        order_items = []
        total = 0.0
        
        for item in order.items:
            product = db.query(ProductDB).filter(ProductDB.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
            
            order_item_data = OrderItemDB(
                product_id=product.id,
                product_name=product.name,
                quantity=item.quantity,
                price=product.price
            )
            order_items.append(order_item_data)
            total += product.price * item.quantity
            
            # Update stock
            product.stock -= item.quantity
        
        # Create order
        new_order = OrderDB(
            customer_name=order.customer_name,
            customer_email=order.customer_email,
            customer_address=order.customer_address,
            customer_phone=order.customer_phone,
            total=round(total, 2),
            status="Processing",
            items=order_items
        )
        
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        
        # Convert to response model
        response_items = [
            OrderItem(
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price
            ) for item in new_order.items
        ]
        
        response = Order(
            id=new_order.id,
            customer_name=new_order.customer_name,
            customer_email=new_order.customer_email,
            customer_address=new_order.customer_address,
            customer_phone=new_order.customer_phone,
            items=response_items,
            total=new_order.total,
            status=new_order.status,
            created_at=new_order.created_at
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    db = SessionLocal()
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    db.close()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    response_items = [
        OrderItem(
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        ) for item in order.items
    ]
    
    return Order(
        id=order.id,
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_address=order.customer_address,
        customer_phone=order.customer_phone,
        items=response_items,
        total=order.total,
        status=order.status,
        created_at=order.created_at
    )

# Serve static files
@app.get("/style.css")
def get_css():
    return FileResponse("style.css")

@app.get("/script.js")
def get_js():
    return FileResponse("script.js")

# Serve index.html
@app.get("/")
def read_root():
    return FileResponse('index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)