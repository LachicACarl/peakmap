# PeakMapPH Backend

FastAPI backend for real-time bus tracking and crowd monitoring system.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to backend folder
cd backend

# Install Python packages
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# Start with auto-reload
python main.py

# OR using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Endpoints

### Health Check
```http
GET /
```
Returns server status and version.

### Update Bus Status
```http
POST /update
Content-Type: application/json

{
  "bus_id": "BUS001",
  "count": 35,
  "lat": 14.6091,
  "lng": 121.0223,
  "route": "EDSA",
  "destination": "Cubao"
}
```

### Get All Buses
```http
GET /buses
```
Returns array of all active buses.

### Get Specific Bus
```http
GET /bus/BUS001
```
Returns status of specific bus.

### Get Statistics
```http
GET /stats
```
Returns system-wide statistics.

### Delete Bus
```http
DELETE /bus/BUS001
```
Removes bus from tracking.

## 🧪 Testing with cURL

```bash
# Update bus
curl -X POST http://localhost:8000/update \
  -H "Content-Type: application/json" \
  -d '{"bus_id":"BUS001","count":35,"lat":14.6091,"lng":121.0223}'

# Get all buses
curl http://localhost:8000/buses

# Get stats
curl http://localhost:8000/stats
```

## 📊 Crowd Level Classification

- **LOW**: < 50% capacity (under 25 passengers)
- **MODERATE**: 50-79% capacity (25-39 passengers)
- **HIGH**: ≥ 80% capacity (40+ passengers)

Default capacity: 50 passengers per bus

## 🔧 Configuration

Environment variables can be set in `.env` file (copy from `.env.example`).

## 📝 Next Steps

1. ✅ **Backend Complete** - Current implementation
2. ⏳ **Supabase Integration** - Replace in-memory storage
3. ⏳ **ESP32 Integration** - Hardware sensor data
4. ⏳ **Production Deployment** - Deploy to cloud

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn with auto-reload
- **Validation**: Pydantic v2
- **Storage**: In-memory (temporary)
- **Future DB**: Supabase PostgreSQL

## 📦 Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── README.md           # This file
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

**CORS errors:**
- Check `allow_origins` in main.py
- Update with your frontend URL

**Module not found:**
```bash
pip install -r requirements.txt
```
