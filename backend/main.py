"""
PeakMapPH - FastAPI Backend
Real-time Bus Tracking System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="PeakMapPH API",
    description="Real-time bus tracking and crowd monitoring system",
    version="1.0.0"
)

# Configure CORS (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (temporary - will replace with Supabase)
buses = {}

# ==================== DATA MODELS ====================

class BusUpdate(BaseModel):
    """Model for bus data updates from driver app"""
    bus_id: str
    count: int  # passenger count
    lat: float  # latitude
    lng: float  # longitude
    route: Optional[str] = None
    destination: Optional[str] = None

class BusStatus(BaseModel):
    """Model for bus status response"""
    bus_id: str
    count: int
    lat: float
    lng: float
    crowd_level: str
    timestamp: str
    route: Optional[str] = None
    destination: Optional[str] = None


# ==================== HELPER FUNCTIONS ====================

def classify_crowd_level(passenger_count: int, max_capacity: int = 50) -> str:
    """
    Classify crowd level based on passenger count
    
    Args:
        passenger_count: Current number of passengers
        max_capacity: Maximum bus capacity (default: 50)
    
    Returns:
        str: 'LOW', 'MODERATE', or 'HIGH'
    """
    percentage = (passenger_count / max_capacity) * 100
    
    if percentage < 50:
        return "LOW"
    elif percentage < 80:
        return "MODERATE"
    else:
        return "HIGH"


# ==================== API ENDPOINTS ====================

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "PeakMapPH API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/update")
def update_bus(data: BusUpdate):
    """
    Update bus status from driver app or ESP32
    
    POST /update
    Body: {
        "bus_id": "BUS001",
        "count": 35,
        "lat": 14.6091,
        "lng": 121.0223,
        "route": "EDSA",
        "destination": "Cubao"
    }
    """
    try:
        # Classify crowd level
        crowd_level = classify_crowd_level(data.count)
        
        # Store bus data
        buses[data.bus_id] = {
            "bus_id": data.bus_id,
            "count": data.count,
            "lat": data.lat,
            "lng": data.lng,
            "crowd_level": crowd_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "route": data.route,
            "destination": data.destination
        }
        
        print(f"✓ Updated {data.bus_id}: {data.count} passengers - {crowd_level}")
        
        return {
            "status": "success",
            "message": f"Bus {data.bus_id} updated successfully",
            "data": buses[data.bus_id]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/buses")
def get_buses():
    """
    Get all bus statuses
    
    GET /buses
    Returns: List of all active buses with their current status
    """
    return list(buses.values())


@app.get("/bus/{bus_id}")
def get_bus(bus_id: str):
    """
    Get specific bus status
    
    GET /bus/BUS001
    Returns: Status of specific bus
    """
    if bus_id not in buses:
        raise HTTPException(status_code=404, detail=f"Bus {bus_id} not found")
    
    return buses[bus_id]


@app.delete("/bus/{bus_id}")
def delete_bus(bus_id: str):
    """
    Remove bus from tracking (for maintenance)
    
    DELETE /bus/BUS001
    """
    if bus_id not in buses:
        raise HTTPException(status_code=404, detail=f"Bus {bus_id} not found")
    
    deleted_bus = buses.pop(bus_id)
    return {
        "status": "success",
        "message": f"Bus {bus_id} removed from tracking",
        "data": deleted_bus
    }


@app.get("/stats")
def get_stats():
    """
    Get system statistics
    
    GET /stats
    Returns: Overall system statistics
    """
    if not buses:
        return {
            "total_buses": 0,
            "total_passengers": 0,
            "high_capacity": 0,
            "moderate_capacity": 0,
            "low_capacity": 0
        }
    
    total_passengers = sum(bus["count"] for bus in buses.values())
    high_capacity = sum(1 for bus in buses.values() if bus["crowd_level"] == "HIGH")
    moderate_capacity = sum(1 for bus in buses.values() if bus["crowd_level"] == "MODERATE")
    low_capacity = sum(1 for bus in buses.values() if bus["crowd_level"] == "LOW")
    
    return {
        "total_buses": len(buses),
        "total_passengers": total_passengers,
        "high_capacity": high_capacity,
        "moderate_capacity": moderate_capacity,
        "low_capacity": low_capacity,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ==================== RUN SERVER ====================
# Use: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
