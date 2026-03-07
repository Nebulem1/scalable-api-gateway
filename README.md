# 🚀 Scalable API Gateway with Redis Caching, Rate Limiting, and Observability

A production-style backend infrastructure project demonstrating how modern backend systems handle high traffic using caching, load balancing, rate limiting, and monitoring.

This project simulates a **microservices architecture** with an API gateway, Redis caching layer, reverse proxy, and observability stack.

---

# 🧠 System Architecture

```
Client
   ↓
Nginx (Reverse Proxy + Edge Rate Limiting)
   ↓
API Gateway (FastAPI)
   ↓
Redis (Cache + Rate Limiter State)
   ↓
Microservices
   ├── Product Service
   └── User Service
   ↓
Prometheus (Metrics Collection)
```

---

# ⚙️ Key Features

### 1️⃣ API Gateway

* Centralized request routing
* Aggregates responses from microservices
* Handles caching, rate limiting, and monitoring

### 2️⃣ Redis Caching Layer

Implements advanced caching techniques:

* Cache with TTL
* Soft TTL & Hard TTL
* Background cache refresh
* Cache stampede protection using distributed locking
* Fallback to service if cache unavailable

### 3️⃣ Rate Limiting

Two layers of protection:

* **Nginx Rate Limiting** (edge level)
* **Gateway Rate Limiting** (application level)

Prevents system overload during traffic spikes.

### 4️⃣ Load Balancing

Nginx distributes requests across multiple gateway instances.

```
Client
   ↓
Nginx
   ↓
Gateway-1
Gateway-2
Gateway-3
```

Supports **horizontal scaling** of the gateway.

### 5️⃣ Microservices

Two backend services simulate independent services:

* **Product Service**
* **User Service**

Gateway communicates with them using internal Docker networking.

### 6️⃣ Observability & Metrics

Prometheus metrics are exposed from the gateway.

Metrics tracked include:

* Cache hits
* Cache rebuilds
* Backend service calls
* Requests waiting for cache rebuild

Prometheus scrapes the `/metrics` endpoint to monitor system behaviour.

---

# 📊 Example Metrics

```
cache_hits_total
service_calls_total
cache_rebuilds_total
wait_cache_total
```

These metrics help analyze:

* cache effectiveness
* backend load
* traffic patterns
* cache rebuild spikes

---

# 🐳 Dockerized Infrastructure

All services run inside Docker containers.

Services included:

```
gateway
redis
product_service
user_service
nginx
prometheus
```

This makes the entire system reproducible and portable.

---

# 📦 Tech Stack

* **FastAPI**
* **Redis**
* **Nginx**
* **Docker & Docker Compose**
* **Prometheus**
* **Python**

---

# 🚀 Running the Project

Clone the repository:

```
git clone <repo_url>
cd project
```

Start the entire stack:

```
docker compose up --build
```

---

# 🌐 Available Services

| Service         | URL                   |
| --------------- | --------------------- |
| API Gateway     | http://localhost      |
| Prometheus      | http://localhost:9090 |
| Product Service | internal              |
| User Service    | internal              |

---

# 🔬 Load Testing

Example load test:

```
ab -n 5000 -c 200 http://localhost/products
```

Used to observe:

* cache hit rate
* service calls
* rebuild spikes

---

# 🧪 Failure Testing

The system was tested under failure scenarios:

* Redis shutdown
* service delay simulation
* concurrent cache rebuild

This helped validate cache stampede protection and system resilience.

---

# 📚 Learning Outcomes

This project explores several backend engineering concepts:

* API Gateway design
* Distributed caching strategies
* Rate limiting
* Horizontal scaling
* Reverse proxies
* Observability with Prometheus
* Docker-based microservices

---

# 📌 Future Improvements

Potential upgrades:

* Circuit breaker pattern
* Distributed tracing
* Grafana dashboards
* Service mesh integration

---

# 👨‍💻 Author

Backend infrastructure experiment built to explore scalable backend system design using Python and microservices architecture.
