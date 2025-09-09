def get_sample_scenarios():
    """
    Return a collection of realistic delivery disruption scenarios
    for testing the Synapse agent.
    """
    return {
        "Restaurant Overload - GrabFood": """
A GrabFood order for lunch delivery to an office building is experiencing delays. The restaurant (Nasi Lemak Express) is overcrowded with a current prep time of 40 minutes due to a lunch rush. The customer has a meeting at 1:30 PM and needs the food delivered by 1:15 PM. The order was placed at 12:20 PM with an original ETA of 1:00 PM. Customer has already paid including delivery fees.
        """.strip(),
        
        "Traffic Jam - GrabCar": """
A GrabCar ride to Changi Airport is stuck in unexpected traffic due to a multi-vehicle accident on the PIE expressway. The passenger has a flight departing at 6:30 PM and needs to reach the airport by 5:00 PM for international check-in. Current location is Jurong East and the usual 45-minute journey is now estimated at 90 minutes due to the accident. The driver is experienced but needs guidance on alternative routes.
        """.strip(),
        
        "Recipient Unavailable - GrabExpress": """
A GrabExpress document delivery to a law firm is experiencing issues because the recipient is in court and unavailable. The package contains time-sensitive legal documents that need to be delivered today before 5 PM for a court filing tomorrow. The building security cannot accept packages, and the recipient's assistant is also unavailable. The package has been at the building for 20 minutes with the driver waiting.
        """.strip(),
        
        "Merchant Dispute - GrabMart": """
A GrabMart grocery order for a family dinner is being rejected by the merchant (NTUC FairPrice) due to several out-of-stock items including the main protein and vegetables. The customer has already paid $85 for the order and needs ingredients for cooking tonight. The merchant suggests waiting 2 hours for restocking, but the customer needs the groceries by 6 PM. Alternative items or merchants need to be found quickly.
        """.strip(),
        
        "Delivery Address Issues": """
A GrabFood order is ready for delivery, but the customer provided an incomplete address missing the unit number in a large condominium complex (The Pinnacle@Duxton with 50 floors and 1,848 units). The driver has been searching for 15 minutes and cannot reach the customer by phone. The food is getting cold, and the driver has other orders waiting. The customer's phone appears to be switched off.
        """.strip(),
        
        "Weather Disruption": """
Heavy rain and flooding in the Orchard Road area has made several roads impassable for GrabCar services. Multiple customers are stranded and requesting rides, but drivers are avoiding the area due to safety concerns. A customer needs urgent transport from Orchard MRT to Singapore General Hospital for a medical appointment. Alternative transportation methods and routes need to be arranged quickly.
        """.strip(),
        
        "Payment Issues": """
A GrabFood order worth $45 has been delivered successfully, but the customer's payment method (credit card) was declined after delivery. The customer claims they have sufficient funds and suspects a technical issue. The merchant has already prepared and provided the food, and the driver has completed the delivery. The customer is requesting to use an alternative payment method but the order is already marked as unpaid in the system.
        """.strip(),
        
        "Driver Emergency": """
A GrabCar driver en route to pick up a passenger for a ride to the airport suddenly experiences a medical emergency and needs immediate assistance. The passenger is waiting at Raffles Place with a flight departure in 3 hours. The original driver is unable to continue driving and requires medical attention. A replacement driver needs to be arranged immediately while ensuring the original driver receives proper care.
        """.strip(),
        
        "Multiple Order Conflict": """
A GrabFood driver has two orders from the same restaurant with pickup time conflicts. Order A is for a premium customer with GrabFood Pro subscription going to CBD area, while Order B is for a regular customer going to HDB estate. The restaurant can only prepare one order at a time due to kitchen capacity, and both customers are expecting delivery within their promised time windows. The driver needs to optimize the delivery sequence while maintaining customer satisfaction.
        """.strip(),
        
        "Technical System Failure": """
The GrabMart ordering system has experienced a technical glitch that double-charged a customer for their grocery order. The customer was charged twice ($120 instead of $60) but only received one order. The customer is requesting immediate refund for the duplicate charge and threatening to file a complaint with their bank. The merchant confirms only one order was processed and delivered. The issue needs to be resolved quickly to maintain customer trust.
        """.strip()
    }
