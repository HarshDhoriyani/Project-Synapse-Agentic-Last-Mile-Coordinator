import random
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List


class MockLogisticsAPI:
    """
    Mock logistics API that simulates real-world responses
    for testing and development of the Synapse agent.
    """
    
    def __init__(self):
        self.base_timestamp = datetime.now()
    
    def check_traffic(self, route: str = "", area: str = "") -> Dict[str, Any]:
        """Simulate traffic checking API"""
        # Simulate different traffic conditions
        conditions = ["light", "moderate", "heavy", "severe"]
        condition = random.choice(conditions)
        
        incidents = []
        if random.random() < 0.3:  # 30% chance of incidents
            incident_types = ["accident", "road work", "flooding", "protest"]
            incidents.append({
                "type": random.choice(incident_types),
                "location": area or "Main Street",
                "severity": random.choice(["minor", "major"]),
                "estimated_delay": f"{random.randint(5, 30)} minutes"
            })
        
        delay_minutes = {
            "light": random.randint(0, 5),
            "moderate": random.randint(5, 15),
            "heavy": random.randint(15, 30),
            "severe": random.randint(30, 60)
        }.get(condition, 0)
        
        return {
            "success": True,
            "route": route,
            "area": area,
            "traffic_condition": condition,
            "estimated_delay_minutes": delay_minutes,
            "incidents": incidents,
            "alternative_routes_available": len(incidents) > 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_merchant_status(self, merchant_id: str = "", location: str = "") -> Dict[str, Any]:
        """Simulate merchant status API"""
        # Simulate merchant operational status
        statuses = ["open", "busy", "closed", "temporarily_unavailable"]
        status = random.choice(statuses)
        
        prep_time = random.randint(15, 60) if status in ["open", "busy"] else 0
        
        return {
            "success": True,
            "merchant_id": merchant_id or f"MERCH_{random.randint(1000, 9999)}",
            "location": location,
            "status": status,
            "prep_time_minutes": prep_time,
            "capacity_available": status == "open",
            "estimated_ready_time": (datetime.now() + timedelta(minutes=prep_time)).isoformat() if prep_time > 0 else None,
            "alternative_recommended": status in ["closed", "temporarily_unavailable"],
            "timestamp": datetime.now().isoformat()
        }
    
    def notify_customer(self, customer_id: str = "", message: str = "", notification_type: str = "push") -> Dict[str, Any]:
        """Simulate customer notification API"""
        # Simulate notification delivery
        success_rate = 0.95  # 95% success rate
        success = random.random() < success_rate
        
        return {
            "success": success,
            "customer_id": customer_id or f"CUST_{random.randint(10000, 99999)}",
            "message": message,
            "notification_type": notification_type,
            "delivery_status": "delivered" if success else "failed",
            "delivery_time": datetime.now().isoformat(),
            "read_receipt": random.random() < 0.7 if success else False,
            "message_id": f"MSG_{random.randint(100000, 999999)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def reroute_driver(self, driver_id: str = "", new_route: str = "", priority: str = "medium") -> Dict[str, Any]:
        """Simulate driver rerouting API"""
        # Simulate rerouting success
        success = random.random() < 0.9  # 90% success rate
        
        estimated_savings = random.randint(5, 20) if success else 0
        
        return {
            "success": success,
            "driver_id": driver_id or f"DRV_{random.randint(1000, 9999)}",
            "new_route": new_route,
            "priority": priority,
            "route_optimized": success,
            "estimated_time_savings_minutes": estimated_savings,
            "driver_notified": success,
            "eta_updated": success,
            "route_id": f"ROUTE_{random.randint(100000, 999999)}" if success else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def find_nearby_alternatives(self, location: str = "", service_type: str = "food", radius: int = 5) -> Dict[str, Any]:
        """Simulate finding alternative merchants/services"""
        # Generate mock alternatives
        num_alternatives = random.randint(2, 8)
        alternatives = []
        
        for i in range(num_alternatives):
            alternatives.append({
                "id": f"ALT_{random.randint(1000, 9999)}",
                "name": f"Alternative {service_type.title()} Service {i+1}",
                "location": f"{random.randint(1, 999)} Main Street",
                "distance_km": round(random.uniform(0.5, radius), 1),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "estimated_prep_time": random.randint(10, 45),
                "available": random.random() < 0.8,
                "price_range": random.choice(["$", "$$", "$$$"])
            })
        
        return {
            "success": True,
            "location": location,
            "service_type": service_type,
            "search_radius_km": radius,
            "alternatives_found": len(alternatives),
            "alternatives": alternatives,
            "best_match": alternatives[0] if alternatives else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def initiate_refund(self, order_id: str = "", amount: float = 0, reason: str = "") -> Dict[str, Any]:
        """Simulate refund processing API"""
        # Simulate refund processing
        success = random.random() < 0.95  # 95% success rate
        
        processing_time = random.randint(1, 5) if success else 0
        
        return {
            "success": success,
            "order_id": order_id or f"ORD_{random.randint(100000, 999999)}",
            "refund_amount": amount,
            "reason": reason,
            "refund_id": f"REF_{random.randint(100000, 999999)}" if success else None,
            "processing_time_business_days": processing_time,
            "refund_method": "original_payment_method",
            "customer_notified": success,
            "status": "processing" if success else "failed",
            "timestamp": datetime.now().isoformat()
        }
    
    def contact_recipient(self, recipient_id: str = "", message: str = "", method: str = "call") -> Dict[str, Any]:
        """Simulate contacting delivery recipient"""
        # Simulate contact attempt
        success_rates = {"call": 0.7, "sms": 0.9, "chat": 0.8}
        success = random.random() < success_rates.get(method, 0.7)
        
        return {
            "success": success,
            "recipient_id": recipient_id or f"RCPT_{random.randint(10000, 99999)}",
            "contact_method": method,
            "message": message,
            "contact_status": "connected" if success else "no_answer",
            "response_received": random.random() < 0.8 if success else False,
            "callback_requested": random.random() < 0.3 if not success else False,
            "contact_id": f"CONT_{random.randint(100000, 999999)}",
            "timestamp": datetime.now().isoformat()
        }
    
    def find_secure_location(self, area: str = "", location_type: str = "dropoff", requirements: str = "") -> Dict[str, Any]:
        """Simulate finding secure locations"""
        # Generate mock secure locations
        num_locations = random.randint(3, 8)
        locations = []
        
        location_types = {
            "dropoff": ["Concierge Desk", "Security Gate", "Parcel Locker", "Reception"],
            "pickup": ["Pickup Point", "Service Center", "Hub Location", "Collection Point"]
        }
        
        for i in range(num_locations):
            locations.append({
                "id": f"LOC_{random.randint(1000, 9999)}",
                "name": f"{random.choice(location_types[location_type])} {i+1}",
                "address": f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'First', 'Second'])} Street",
                "distance_km": round(random.uniform(0.1, 2.0), 1),
                "security_rating": random.choice(["high", "medium", "standard"]),
                "operating_hours": "24/7" if random.random() < 0.3 else "9 AM - 9 PM",
                "accessibility": random.choice(["wheelchair_accessible", "ground_floor", "elevator_access"]),
                "available": random.random() < 0.9
            })
        
        return {
            "success": True,
            "area": area,
            "location_type": location_type,
            "requirements": requirements,
            "locations_found": len(locations),
            "locations": locations,
            "recommended": locations[0] if locations else None,
            "timestamp": datetime.now().isoformat()
        }
    
    def update_order_status(self, order_id: str = "", status: str = "", notes: str = "") -> Dict[str, Any]:
        """Simulate order status update"""
        # Simulate status update
        success = random.random() < 0.98  # 98% success rate
        
        valid_statuses = [
            "confirmed", "preparing", "ready_for_pickup", "picked_up",
            "in_transit", "delivered", "cancelled", "delayed"
        ]
        
        return {
            "success": success,
            "order_id": order_id or f"ORD_{random.randint(100000, 999999)}",
            "previous_status": random.choice(valid_statuses),
            "new_status": status if status in valid_statuses else "updated",
            "notes": notes,
            "customer_notified": success,
            "estimated_delivery_time": (datetime.now() + timedelta(minutes=random.randint(15, 60))).isoformat() if status in ["preparing", "picked_up"] else None,
            "tracking_updated": success,
            "timestamp": datetime.now().isoformat()
        }
    
    def coordinate_with_support(self, issue_type: str = "", priority: str = "medium", details: str = "") -> Dict[str, Any]:
        """Simulate support coordination"""
        # Simulate support ticket creation
        success = random.random() < 0.99  # 99% success rate
        
        response_times = {
            "low": random.randint(60, 240),
            "medium": random.randint(30, 120),
            "high": random.randint(5, 60),
            "urgent": random.randint(1, 15)
        }
        
        return {
            "success": success,
            "ticket_id": f"SUPP_{random.randint(100000, 999999)}" if success else None,
            "issue_type": issue_type,
            "priority": priority,
            "details": details,
            "assigned_agent": f"Agent_{random.randint(1, 50)}" if success else None,
            "estimated_response_time_minutes": response_times.get(priority, 60),
            "escalation_level": 1 if priority in ["low", "medium"] else 2,
            "status": "open" if success else "failed",
            "timestamp": datetime.now().isoformat()
        }
