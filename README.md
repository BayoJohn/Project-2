# 🛍️ E-commerce Platform with Load Balancing

A production-ready e-commerce application featuring containerized microservices, PostgreSQL database, and automated load balancing with Caddy reverse proxy.

## 🚀 Features

- **Full-Stack Application**: FastAPI backend with responsive frontend
- **PostgreSQL Database**: Production-grade data persistence
- **Docker Containerization**: Consistent deployments across environments
- **Load Balancing**: Caddy reverse proxy with round-robin distribution
- **Horizontal Scaling**: Auto-scaling with 3 replicas
- **Health Monitoring**: Automated health checks and failover
- **CI/CD Pipeline**: GitHub Actions for automated deployment

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Pydantic**: Data validation

### Frontend
- **HTML5/CSS3**: Responsive design
- **JavaScript**: Dynamic functionality
- **Fetch API**: RESTful communication

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Caddy**: Reverse proxy & load balancer
- **GitHub Actions**: CI/CD automation

## 📋 Prerequisites

- Docker & Docker Compose
- Git
- Python 3.11+ (for local development)

## 🏃 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ecommerce-platform.git
cd ecommerce-platform

# Start all services with 3 replicas
docker-compose up -d --scale web=3

# Access the application
open http://localhost
```

### Check Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Check health
docker-compose ps
```

## 🏗️ Architecture

```
User Request (Port 80/443)
        ↓
    Caddy Load Balancer
        ↓
   Round-Robin Distribution
    ↓      ↓      ↓
  web_1  web_2  web_3
    ↓      ↓      ↓
   PostgreSQL Database
        ↓
  Persistent Volume
```

## 📊 API Endpoints

- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `GET /api/categories` - List categories
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details

## 🗄️ Database

Access PostgreSQL:

```bash
docker exec -it ecommerce-db psql -U admin -d ecommerce
```

Connection details:
- **Host**: localhost
- **Port**: 5432
- **Database**: ecommerce
- **User**: admin
- **Password**: securepassword123

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
POSTGRES_DB=ecommerce
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://admin:password@postgres:5432/ecommerce
```

### Scaling

```bash
# Scale to 5 replicas
docker-compose up -d --scale web=5

# Scale down to 2 replicas
docker-compose up -d --scale web=2
```

## 🚀 Deployment

This project uses GitHub Actions for automated deployment to AWS EC2.

### Prerequisites
1. AWS EC2 instance with Docker installed
2. GitHub repository secrets configured
3. SSH key pair for EC2 access

See `.github/workflows/deploy.yml` for CI/CD configuration.

## 📈 Monitoring

```bash
# Monitor resource usage
docker stats

# View Caddy logs
docker logs caddy-lb -f

# View application logs
docker logs ecommerce_web_1 -f
```

## 🧪 Testing

```bash
# Test API endpoints
curl http://localhost/api/products

# Test load balancing
for i in {1..10}; do curl http://localhost/api/products; done
```

## 🛡️ Security Features

- CORS configuration
- SQL injection protection (SQLAlchemy ORM)
- Environment-based secrets
- Health check endpoints
- Automatic failover

## 📝 Project Structure

```
ecommerce-platform/
├── main.py                 # FastAPI backend
├── index.html             # Frontend HTML
├── style.css              # Styling
├── script.js              # Frontend JavaScript
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Multi-container orchestration
├── Caddyfile             # Load balancer configuration
├── requirements.txt       # Python dependencies
└── .github/
    └── workflows/
        └── deploy.yml     # CI/CD pipeline
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Caddy for simple yet powerful reverse proxy
- Docker for containerization technology