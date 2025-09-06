"""
Test scenarios for the Synapse agent based on the project documentation.
These scenarios are derived from real-world disruptions in the Grab ecosystem.
"""

def get_sample_scenarios():
    """
    Return a dictionary of sample disruption scenarios for testing
    
    Returns:
        Dict mapping scenario names to descriptions
    """
    return {
        "Restaurant Overload - GrabFood": """
        A GrabFood order has been placed at "Golden Dragon Restaurant" but the merchant status shows a 40-minute kitchen prep time due to being overloaded with orders. The customer ordered premium dishes worth $35 and is expecting delivery within 30 minutes. The assigned driver is currently idle and waiting. The restaurant is popular and often has long wait times during peak hours. The customer has a VIP status and needs to be handled with priority.
        """,
        
        "Traffic Accident - GrabCar": """
        A GrabCar passenger is on an urgent trip to Changi Airport for an international flight departing in 90 minutes. The trip was supposed to take 35 minutes, but a major accident has just occurred on the East Coast Parkway (ECP), causing a complete blockage of 2 lanes. Traffic is backing up severely and the estimated delay is 45-60 minutes. The passenger is getting anxious and keeps asking for updates. Alternative routes need to be found immediately.
        """,
        
        "Recipient Unavailable - GrabExpress": """
        A GrabExpress driver has arrived at a high-rise condominium to deliver a valuable electronics package worth $800. The recipient is not answering calls or texts, and the security guard says the recipient left earlier and won't be back for 2 hours. The package requires signature confirmation and cannot be left unattended. The driver has other deliveries waiting and cannot stay. The building has a concierge service but they don't accept packages without explicit permission.
        """,
        
        "Damaged Package Dispute - GrabFood": """
        A GrabFood driver has arrived at the customer's doorstep with an order containing drinks and food. Upon handover, the customer notices that one of the drinks has spilled inside the bag, making the food container wet. Both the customer and driver are unsure whether this happened due to poor merchant packaging or driver mishandling during transport. The customer is demanding a full refund and the driver is worried about getting a bad rating. The situation is escalating and needs immediate resolution.
        """,
        
        "Merchant Closure - GrabMart": """
        A GrabMart order for groceries worth $65 has been placed for a customer who needs the items for a dinner party tonight. However, the merchant (FreshMart Grocery) has suddenly closed due to a technical issue with their POS system and won't reopen until tomorrow. The customer specifically needed organic vegetables and specialty items that aren't available at regular supermarkets. The order was supposed to be delivered in 45 minutes and the driver has already been assigned.
        """,
        
        "Route Deviation - GrabExpress": """
        A GrabExpress driver is delivering important legal documents that must arrive by 4 PM for a court filing. It's currently 3:15 PM and the driver has taken a wrong turn due to GPS malfunction, ending up in a traffic-heavy area that will add 25 minutes to the journey. The original route would have gotten there by 3:45 PM. The customer is calling repeatedly asking for updates and threatening to cancel if the delivery is late. The documents are time-sensitive and cannot be filed late.
        """,
        
        "Multiple Order Chaos - GrabFood": """
        A GrabFood driver has picked up orders from 3 different restaurants and is delivering to 4 different customers in sequence. However, the second restaurant gave the wrong order (meant for another driver), the third customer's address is incorrect in the system, and the fourth customer just called to cancel their order. The driver is confused about what to do with each order, customers are calling asking about delays, and food is getting cold. The driver needs clear guidance on how to resolve each situation.
        """,
        
        "Weather Emergency - GrabCar": """
        Heavy rain and flooding has started in several areas of the city during peak hour. A GrabCar driver with a passenger onboard is stuck in rising flood water on a main road. The passenger needs to get to an important medical appointment, but the current route is no longer safe to travel. Emergency services are advising people to avoid several roads due to flooding. The passenger is elderly and anxious about the situation. Alternative routes and safety measures need to be coordinated immediately.
        """,
        
        "Payment Dispute - GrabExpress": """
        A GrabExpress customer received a package but claims it was damaged during delivery. The package contained a birthday gift (a ceramic vase) that arrived with visible cracks. The customer wants a full refund, but the sender (another customer using GrabExpress) claims the item was packed properly. The driver says the package was intact when picked up and delivered. There's no clear evidence of when the damage occurred, and both parties are demanding compensation. The situation requires fair mediation.
        """,
        
        "System Glitch - Multi-Service": """
        A major system glitch has affected the assignment algorithms, causing multiple issues: 1) Three drivers have been assigned to the same GrabFood order, 2) A GrabCar passenger has been charged twice for the same trip, 3) Several GrabExpress packages are showing as delivered but weren't actually delivered, and 4) Customer service is overwhelmed with complaints. The technical team is working on fixes but customers need immediate resolution. Each affected service requires different approaches to resolve their specific issues.
        """
    }

def get_scenario_categories():
    """
    Categorize scenarios by service type and complexity
    
    Returns:
        Dict mapping categories to scenario lists
    """
    return {
        "GrabFood": [
            "Restaurant Overload - GrabFood",
            "Damaged Package Dispute - GrabFood", 
            "Multiple Order Chaos - GrabFood"
        ],
        "GrabCar": [
            "Traffic Accident - GrabCar",
            "Weather Emergency - GrabCar"
        ],
        "GrabExpress": [
            "Recipient Unavailable - GrabExpress",
            "Route Deviation - GrabExpress",
            "Payment Dispute - GrabExpress"
        ],
        "GrabMart": [
            "Merchant Closure - GrabMart"
        ],
        "Multi-Service": [
            "System Glitch - Multi-Service"
        ]
    }

def get_complexity_levels():
    """
    Categorize scenarios by complexity level
    
    Returns:
        Dict mapping complexity levels to scenario characteristics
    """
    return {
        "Simple": {
            "description": "Single issue, clear solution path, 1-2 tools needed",
            "scenarios": ["Restaurant Overload - GrabFood", "Traffic Accident - GrabCar"],
            "expected_resolution_time": "< 30 seconds",
            "tools_typically_used": 2
        },
        "Moderate": {
            "description": "Multiple stakeholders, requires coordination, 3-4 tools needed",
            "scenarios": ["Recipient Unavailable - GrabExpress", "Damaged Package Dispute - GrabFood"],
            "expected_resolution_time": "30-60 seconds",
            "tools_typically_used": 4
        },
        "Complex": {
            "description": "Multiple issues, high stakes, requires escalation, 5+ tools needed",
            "scenarios": ["Multiple Order Chaos - GrabFood", "Weather Emergency - GrabCar", "System Glitch - Multi-Service"],
            "expected_resolution_time": "60+ seconds",
            "tools_typically_used": 6
        }
    }

def get_success_criteria():
    """
    Define success criteria for each scenario type
    
    Returns:
        Dict with success metrics and criteria
    """
    return {
        "resolution_success_rate": {
            "target": 80,
            "description": "Percentage of scenarios successfully resolved"
        },
        "customer_notification_time": {
            "target": 30,
            "unit": "seconds",
            "description": "Time to notify customers about issues"
        },
        "driver_idle_time_reduction": {
            "target_min": 10,
            "target_max": 20,
            "unit": "percent",
            "description": "Reduction in driver idle time"
        },
        "eta_breach_reduction": {
            "target_min": 10,
            "target_max": 15,
            "unit": "percent",
            "description": "Reduction in ETA breaches"
        },
        "tools_usage_efficiency": {
            "description": "Using appropriate tools for each scenario",
            "metrics": [
                "Correct tool selection",
                "Minimal redundant tool calls",
                "Effective tool sequencing"
            ]
        }
    }

def get_expected_outcomes():
    """
    Define expected outcomes for each sample scenario
    
    Returns:
        Dict mapping scenario names to expected resolution approaches
    """
    return {
        "Restaurant Overload - GrabFood": {
            "expected_tools": ["get_merchant_status", "notify_customer", "find_nearby_alternatives", "reroute_driver"],
            "expected_actions": [
                "Check actual merchant prep time",
                "Notify VIP customer about delay with compensation",
                "Find alternative restaurants with shorter wait times",
                "Reassign driver to other deliveries while food is being prepared"
            ],
            "success_indicators": ["Customer notified", "Alternative suggested", "Driver optimally utilized"]
        },
        
        "Traffic Accident - GrabCar": {
            "expected_tools": ["check_traffic", "calculate_alternative_route", "notify_customer"],
            "expected_actions": [
                "Assess traffic situation and delay",
                "Calculate fastest alternative route",
                "Notify passenger with new ETA and route explanation",
                "Provide real-time updates"
            ],
            "success_indicators": ["Alternative route found", "Passenger informed", "ETA updated"]
        },
        
        "Recipient Unavailable - GrabExpress": {
            "expected_tools": ["contact_recipient", "find_secure_location", "notify_customer"],
            "expected_actions": [
                "Attempt to contact recipient through multiple channels",
                "Find secure drop-off location (concierge, locker, etc.)",
                "Get recipient permission for alternative delivery",
                "Coordinate with building management if needed"
            ],
            "success_indicators": ["Recipient contacted", "Secure location found", "Delivery completed"]
        }
    }
