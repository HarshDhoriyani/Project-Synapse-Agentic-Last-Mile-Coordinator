import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class MockLogisticsAPI:
    """
    Mock logistics API service that simulates real-world logistics operations.
    Provides realistic responses for traffic, merchant status, communications, etc.
    """
    
    def __init__(self):
        self.merchant_data = self._initialize_merchant_data()
        self.traffic_incidents = self._initialize_traffic_data()
        self.driver_pool = self._initialize_driver_data()
        logger.info("Mock Logistics API initialized")
    
    def get_traffic_conditions(self, origin: str, destination: str, route_name: str) -> Dict[str, Any]:
        """Get current traffic conditions for a route"""
        logger.info(f"Getting traffic conditions for route: {route_name}")
        
        # Simulate different traffic scenarios
        scenarios = [
            {
                "status": "clear",
                "delay_minutes": random.randint(0, 5),
                "incidents": [],
                "congestion_level": "low"
            },
            {
                "status": "moderate_traffic",
                "delay_minutes": random.randint(10, 20),
                "incidents": ["Heavy traffic on main road"],
                "congestion_level": "medium"
            },
            {
                "status": "heavy_traffic", 
                "delay_minutes": random.randint(25, 45),
                "incidents": ["Major accident blocking 2 lanes", "Road construction"],
                "congestion_level": "high"
            },
            {
                "status": "blocked",
                "delay_minutes": random.randint(60, 120),
                "incidents": ["Complete road closure due to accident", "Emergency services on scene"],
                "congestion_level": "severe"
            }
        ]
        
        selected_scenario = random.choice(scenarios)
        
        return {
            "route_name": route_name,
            "origin": origin,
            "destination": destination,
            "status": selected_scenario["status"],
            "estimated_delay_minutes": selected_scenario["delay_minutes"],
            "current_incidents": selected_scenario["incidents"],
            "congestion_level": selected_scenario["congestion_level"],
            "alternative_route_suggested": selected_scenario["delay_minutes"] > 30,
            "timestamp": datetime.now().isoformat(),
            "data_source": "mock_traffic_api"
        }
    
    def calculate_alternative_routes(self, origin: str, destination: str, avoid_areas: List[str]) -> Dict[str, Any]:
        """Calculate alternative routes avoiding specified areas"""
        logger.info(f"Calculating alternative routes from {origin} to {destination}")
        
        # Generate multiple alternative routes
        routes = []
        route_names = ["Highway Route", "City Center Route", "Scenic Route", "Express Lane Route"]
        
        for i, route_name in enumerate(route_names[:3]):  # Return top 3 alternatives
            base_time = random.randint(20, 40)
            delay_factor = random.uniform(1.0, 1.5)
            
            routes.append({
                "route_id": f"alt_route_{i+1}",
                "route_name": route_name,
                "estimated_time_minutes": int(base_time * delay_factor),
                "distance_km": random.uniform(8.0, 25.0),
                "traffic_level": random.choice(["low", "medium", "high"]),
                "toll_cost": random.uniform(0, 8.5) if "Highway" in route_name else 0,
                "recommended": i == 0  # First route is recommended
            })
        
        return {
            "origin": origin,
            "destination": destination,
            "avoided_areas": avoid_areas,
            "alternative_routes": routes,
            "calculation_time": datetime.now().isoformat(),
            "total_routes_found": len(routes)
        }
    
    def get_merchant_info(self, merchant_identifier: str) -> Dict[str, Any]:
        """Get merchant status and information"""
        logger.info(f"Getting merchant info for: {merchant_identifier}")
        
        # Simulate various merchant scenarios
        merchant_scenarios = [
            {
                "status": "operational",
                "prep_time_minutes": random.randint(15, 25),
                "queue_length": random.randint(0, 3),
                "availability": "high"
            },
            {
                "status": "busy",
                "prep_time_minutes": random.randint(30, 50),
                "queue_length": random.randint(8, 15),
                "availability": "limited"
            },
            {
                "status": "overloaded",
                "prep_time_minutes": random.randint(60, 90),
                "queue_length": random.randint(20, 35),
                "availability": "very_low"
            },
            {
                "status": "temporarily_closed",
                "prep_time_minutes": 0,
                "queue_length": 0,
                "availability": "none",
                "closure_reason": random.choice(["staff_shortage", "technical_issue", "supply_shortage"])
            }
        ]
        
        selected_scenario = random.choice(merchant_scenarios)
        
        # Generate merchant details
        merchant_types = ["restaurant", "grocery", "pharmacy", "convenience_store"]
        cuisines = ["Asian", "Western", "Local", "Fast Food", "Healthy"]
        
        return {
            "merchant_id": f"merchant_{hash(merchant_identifier) % 10000}",
            "merchant_name": merchant_identifier,
            "merchant_type": random.choice(merchant_types),
            "cuisine_type": random.choice(cuisines) if selected_scenario["status"] != "temporarily_closed" else None,
            "status": selected_scenario["status"],
            "current_prep_time_minutes": selected_scenario["prep_time_minutes"],
            "order_queue_length": selected_scenario["queue_length"],
            "availability_level": selected_scenario["availability"],
            "closure_reason": selected_scenario.get("closure_reason"),
            "operating_hours": "06:00-23:00",
            "accepts_new_orders": selected_scenario["status"] in ["operational", "busy"],
            "estimated_ready_time": (datetime.now() + timedelta(minutes=selected_scenario["prep_time_minutes"])).isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def find_nearby_merchants(self, location: str, service_type: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Find nearby alternative merchants"""
        logger.info(f"Finding nearby {service_type} merchants near {location}")
        
        # Generate nearby alternatives
        alternatives = []
        merchant_names = [
            "Golden Dragon Restaurant", "Fresh Market Grocery", "Quick Bite Cafe",
            "Healthy Bowl", "Pizza Palace", "Local Favorites", "Express Mart",
            "Gourmet Kitchen", "Street Food Corner", "Family Restaurant"
        ]
        
        for i in range(random.randint(3, 7)):
            distance = random.uniform(0.5, 3.0)
            prep_time = random.randint(10, 35)
            
            alternatives.append({
                "merchant_id": f"nearby_{i+1}",
                "merchant_name": random.choice(merchant_names),
                "distance_km": round(distance, 1),
                "estimated_prep_time_minutes": prep_time,
                "rating": round(random.uniform(3.5, 4.8), 1),
                "cuisine_type": random.choice(["Asian", "Western", "Local", "Fast Food"]),
                "status": "operational",
                "accepts_orders": True,
                "estimated_delivery_time": prep_time + int(distance * 3),  # 3 min per km
                "price_range": random.choice(["$", "$$", "$$$"]),
                "similarity_score": random.uniform(0.6, 0.95)  # How similar to original merchant
            })
        
        # Sort by combination of distance and prep time
        alternatives.sort(key=lambda x: x["distance_km"] + (x["estimated_prep_time_minutes"] / 10))
        
        return {
            "search_location": location,
            "service_type": service_type,
            "requirements": requirements,
            "alternatives_found": alternatives,
            "total_count": len(alternatives),
            "search_radius_km": 3.0,
            "timestamp": datetime.now().isoformat()
        }
    
    def send_customer_notification(self, customer_id: str, message_type: str, message: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification to customer"""
        logger.info(f"Sending {message_type} notification to customer {customer_id}")
        
        # Simulate notification delivery
        delivery_methods = ["push_notification", "sms", "email", "in_app"]
        selected_method = random.choice(delivery_methods)
        
        # Simulate delivery success/failure
        delivery_success = random.random() > 0.05  # 95% success rate
        
        notification_content = {
            "delay": f"Your order is delayed by {details.get('delay_minutes', 15)} minutes due to high demand.",
            "route_change": f"Your driver is taking an alternative route due to traffic. New ETA: {details.get('new_eta', 'updating...')}",
            "merchant_issue": f"The restaurant is experiencing delays. We're finding you alternatives.",
            "compensation": f"We've issued a ${details.get('voucher_amount', 5)} voucher for the inconvenience.",
            "update": message if message else "We're working to resolve your order issue."
        }
        
        return {
            "customer_id": customer_id,
            "notification_id": f"notif_{random.randint(100000, 999999)}",
            "message_type": message_type,
            "content": notification_content.get(message_type, notification_content["update"]),
            "delivery_method": selected_method,
            "delivery_status": "delivered" if delivery_success else "failed",
            "delivery_time": datetime.now().isoformat(),
            "read_status": "unread",
            "compensation_offered": details.get('voucher_amount', 0) > 0
        }
    
    def contact_recipient(self, recipient_contact: str, message_type: str, urgency: str) -> Dict[str, Any]:
        """Contact delivery recipient"""
        logger.info(f"Contacting recipient {recipient_contact} with {urgency} urgency")
        
        # Simulate different contact outcomes
        contact_outcomes = [
            {"status": "answered", "response": "Available now, please deliver"},
            {"status": "answered", "response": "Not home, please leave with concierge"},
            {"status": "answered", "response": "Can you come back in 30 minutes?"},
            {"status": "no_answer", "response": None},
            {"status": "busy", "response": "Will call back shortly"}
        ]
        
        outcome = random.choice(contact_outcomes)
        
        return {
            "recipient_contact": recipient_contact,
            "message_type": message_type,
            "urgency_level": urgency,
            "contact_method": random.choice(["call", "sms", "chat"]),
            "contact_status": outcome["status"],
            "recipient_response": outcome["response"],
            "contact_time": datetime.now().isoformat(),
            "follow_up_required": outcome["status"] == "no_answer",
            "alternative_instructions": outcome["response"] if outcome["status"] == "answered" else None
        }
    
    def reroute_driver(self, driver_id: str, new_assignment: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Reroute driver to new assignment"""
        logger.info(f"Rerouting driver {driver_id} with {priority} priority")
        
        # Simulate driver status and rerouting
        driver_statuses = ["available", "on_delivery", "between_orders", "offline"]
        current_status = random.choice(driver_statuses)
        
        reroute_success = current_status in ["available", "between_orders"]
        
        return {
            "driver_id": driver_id,
            "previous_status": current_status,
            "new_assignment": new_assignment,
            "priority_level": priority,
            "reroute_status": "successful" if reroute_success else "pending",
            "estimated_arrival_time": (datetime.now() + timedelta(minutes=random.randint(5, 20))).isoformat(),
            "driver_location": f"Lat: {random.uniform(1.2, 1.5)}, Lng: {random.uniform(103.6, 104.0)}",
            "acceptance_status": "accepted" if reroute_success else "pending_response",
            "reroute_time": datetime.now().isoformat()
        }
    
    def find_secure_dropoff_locations(self, address: str, package_type: str, security_level: str) -> Dict[str, Any]:
        """Find secure drop-off locations"""
        logger.info(f"Finding secure drop-off locations near {address}")
        
        # Generate secure location options
        location_types = ["parcel_locker", "concierge", "security_desk", "neighbor", "pickup_point"]
        locations = []
        
        for i in range(random.randint(2, 5)):
            location_type = random.choice(location_types)
            distance = random.uniform(0.1, 1.0)
            
            locations.append({
                "location_id": f"secure_{i+1}",
                "location_type": location_type,
                "name": self._generate_location_name(location_type),
                "address": f"{address} vicinity",
                "distance_km": round(distance, 2),
                "security_rating": random.randint(7, 10),
                "operating_hours": "24/7" if location_type == "parcel_locker" else "08:00-20:00",
                "access_requirements": self._get_access_requirements(location_type),
                "cost": random.uniform(0, 3.0) if location_type == "parcel_locker" else 0,
                "availability": "available"
            })
        
        # Sort by security rating and distance
        locations.sort(key=lambda x: (-x["security_rating"], x["distance_km"]))
        
        return {
            "search_address": address,
            "package_type": package_type,
            "required_security_level": security_level,
            "secure_locations": locations,
            "total_options": len(locations),
            "recommended_location": locations[0] if locations else None,
            "search_time": datetime.now().isoformat()
        }
    
    def process_refund(self, order_id: str, refund_type: str, amount: float, reason: str) -> Dict[str, Any]:
        """Process customer refund"""
        logger.info(f"Processing {refund_type} refund for order {order_id}")
        
        # Simulate refund processing
        processing_success = random.random() > 0.02  # 98% success rate
        
        refund_methods = ["original_payment", "grab_credits", "voucher"]
        selected_method = random.choice(refund_methods)
        
        # Calculate processing time based on method
        processing_times = {
            "original_payment": "3-5 business days",
            "grab_credits": "immediate",
            "voucher": "immediate"
        }
        
        return {
            "order_id": order_id,
            "refund_id": f"refund_{random.randint(100000, 999999)}",
            "refund_type": refund_type,
            "amount": amount,
            "reason": reason,
            "processing_status": "approved" if processing_success else "pending_review",
            "refund_method": selected_method,
            "processing_time": processing_times[selected_method],
            "approval_time": datetime.now().isoformat(),
            "customer_notification_sent": True,
            "additional_compensation": {
                "voucher_amount": random.randint(3, 10),
                "loyalty_points": random.randint(50, 200)
            } if processing_success else None
        }
    
    def escalate_to_human_support(self, issue_details: str, priority_level: str, customer_info: Dict[str, Any]) -> Dict[str, Any]:
        """Escalate issue to human support"""
        logger.info(f"Escalating {priority_level} priority issue to human support")
        
        # Simulate support queue and assignment
        support_agents = ["Agent_Sarah", "Agent_Mike", "Agent_Lisa", "Agent_David"]
        
        queue_sizes = {
            "low": random.randint(10, 30),
            "medium": random.randint(5, 15),
            "high": random.randint(1, 5),
            "critical": 0
        }
        
        eta_minutes = {
            "low": random.randint(30, 120),
            "medium": random.randint(10, 30),
            "high": random.randint(2, 10),
            "critical": random.randint(0, 2)
        }
        
        return {
            "escalation_id": f"esc_{random.randint(100000, 999999)}",
            "issue_details": issue_details,
            "priority_level": priority_level,
            "customer_info": customer_info,
            "assigned_agent": random.choice(support_agents),
            "queue_position": queue_sizes.get(priority_level, 10),
            "estimated_response_time_minutes": eta_minutes.get(priority_level, 30),
            "escalation_time": datetime.now().isoformat(),
            "case_status": "assigned",
            "internal_notes": "Auto-escalated by Synapse AI coordinator",
            "customer_notified": True,
            "follow_up_scheduled": True
        }
    
    # Helper methods
    def _initialize_merchant_data(self) -> Dict[str, Any]:
        """Initialize mock merchant database"""
        return {
            "total_merchants": 1500,
            "active_merchants": 1200,
            "avg_prep_time": 25
        }
    
    def _initialize_traffic_data(self) -> List[Dict[str, Any]]:
        """Initialize mock traffic incident data"""
        return [
            {"type": "accident", "severity": "major", "location": "Highway 1"},
            {"type": "construction", "severity": "minor", "location": "City Center"},
            {"type": "weather", "severity": "moderate", "location": "East Side"}
        ]
    
    def _initialize_driver_data(self) -> Dict[str, Any]:
        """Initialize mock driver pool data"""
        return {
            "total_drivers": 800,
            "active_drivers": 600,
            "available_drivers": 150
        }
    
    def _generate_location_name(self, location_type: str) -> str:
        """Generate name for secure location"""
        names = {
            "parcel_locker": "SmartLocker Station",
            "concierge": "Building Concierge",
            "security_desk": "Security Reception",
            "neighbor": "Trusted Neighbor",
            "pickup_point": "Collection Point"
        }
        return names.get(location_type, "Secure Location")
    
    def _get_access_requirements(self, location_type: str) -> List[str]:
        """Get access requirements for location type"""
        requirements = {
            "parcel_locker": ["PIN code", "Mobile verification"],
            "concierge": ["ID verification", "Recipient contact"],
            "security_desk": ["ID verification", "Building access"],
            "neighbor": ["Recipient approval", "Photo verification"],
            "pickup_point": ["QR code", "ID verification"]
        }
        return requirements.get(location_type, ["Standard verification"])
