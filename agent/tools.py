import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from langchain.tools import Tool
from langchain_core.tools import tool

from services.mock_apis import MockLogisticsAPI


class LogisticsToolkit:
    """
    Collection of logistics tools for the Synapse agent.
    Each tool simulates real-world logistics operations.
    """
    
    def __init__(self):
        self.api = MockLogisticsAPI()
    
    def get_tools(self) -> List[Tool]:
        """Return the list of available tools for the agent"""
        return [
            Tool(
                name="check_traffic",
                description="Check traffic conditions and incidents for a specific route or area. Input: {'route': 'pickup to delivery location', 'area': 'city/district name'}",
                func=self.check_traffic
            ),
            Tool(
                name="get_merchant_status",
                description="Get merchant availability, prep times, and operational status. Input: {'merchant_id': 'merchant identifier', 'location': 'merchant location'}",
                func=self.get_merchant_status
            ),
            Tool(
                name="notify_customer",
                description="Send notifications to customers about order status, delays, or updates. Input: {'customer_id': 'customer identifier', 'message': 'notification message', 'type': 'sms/email/push'}",
                func=self.notify_customer
            ),
            Tool(
                name="reroute_driver",
                description="Optimize driver routes or reassign deliveries. Input: {'driver_id': 'driver identifier', 'new_route': 'optimized route', 'priority': 'high/medium/low'}",
                func=self.reroute_driver
            ),
            Tool(
                name="find_nearby_alternatives",
                description="Find alternative merchants, pickup points, or service options. Input: {'location': 'current location', 'service_type': 'food/mart/express', 'radius': 'search radius in km'}",
                func=self.find_nearby_alternatives
            ),
            Tool(
                name="initiate_refund",
                description="Process customer refunds and compensations. Input: {'order_id': 'order identifier', 'amount': 'refund amount', 'reason': 'refund reason'}",
                func=self.initiate_refund
            ),
            Tool(
                name="contact_recipient",
                description="Contact delivery recipients for coordination or updates. Input: {'recipient_id': 'recipient identifier', 'message': 'contact message', 'method': 'call/sms/chat'}",
                func=self.contact_recipient
            ),
            Tool(
                name="find_secure_location",
                description="Find secure drop-off locations or pickup points. Input: {'area': 'target area', 'type': 'dropoff/pickup', 'requirements': 'security/accessibility needs'}",
                func=self.find_secure_location
            ),
            Tool(
                name="update_order_status",
                description="Update order status and tracking information. Input: {'order_id': 'order identifier', 'status': 'new status', 'notes': 'additional notes'}",
                func=self.update_order_status
            ),
            Tool(
                name="coordinate_with_support",
                description="Escalate to human support or coordinate with support teams. Input: {'issue_type': 'issue category', 'priority': 'urgency level', 'details': 'issue details'}",
                func=self.coordinate_with_support
            )
        ]
    
    def check_traffic(self, input_data: str) -> str:
        """Check traffic conditions and incidents"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.check_traffic(
                route=data.get('route', ''),
                area=data.get('area', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"route": "pickup to delivery location", "area": "city/district name"}'
            })
    
    def get_merchant_status(self, input_data: str) -> str:
        """Get merchant availability and status"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.get_merchant_status(
                merchant_id=data.get('merchant_id', ''),
                location=data.get('location', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"merchant_id": "merchant identifier", "location": "merchant location"}'
            })
    
    def notify_customer(self, input_data: str) -> str:
        """Send customer notifications"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.notify_customer(
                customer_id=data.get('customer_id', ''),
                message=data.get('message', ''),
                notification_type=data.get('type', 'push')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"customer_id": "customer identifier", "message": "notification message", "type": "sms/email/push"}'
            })
    
    def reroute_driver(self, input_data: str) -> str:
        """Reroute or reassign driver"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.reroute_driver(
                driver_id=data.get('driver_id', ''),
                new_route=data.get('new_route', ''),
                priority=data.get('priority', 'medium')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"driver_id": "driver identifier", "new_route": "optimized route", "priority": "high/medium/low"}'
            })
    
    def find_nearby_alternatives(self, input_data: str) -> str:
        """Find alternative service options"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.find_nearby_alternatives(
                location=data.get('location', ''),
                service_type=data.get('service_type', 'food'),
                radius=data.get('radius', 5)
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"location": "current location", "service_type": "food/mart/express", "radius": "search radius in km"}'
            })
    
    def initiate_refund(self, input_data: str) -> str:
        """Process customer refund"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.initiate_refund(
                order_id=data.get('order_id', ''),
                amount=data.get('amount', 0),
                reason=data.get('reason', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"order_id": "order identifier", "amount": "refund amount", "reason": "refund reason"}'
            })
    
    def contact_recipient(self, input_data: str) -> str:
        """Contact delivery recipient"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.contact_recipient(
                recipient_id=data.get('recipient_id', ''),
                message=data.get('message', ''),
                method=data.get('method', 'call')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"recipient_id": "recipient identifier", "message": "contact message", "method": "call/sms/chat"}'
            })
    
    def find_secure_location(self, input_data: str) -> str:
        """Find secure drop-off/pickup locations"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.find_secure_location(
                area=data.get('area', ''),
                location_type=data.get('type', 'dropoff'),
                requirements=data.get('requirements', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"area": "target area", "type": "dropoff/pickup", "requirements": "security/accessibility needs"}'
            })
    
    def update_order_status(self, input_data: str) -> str:
        """Update order status and tracking"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.update_order_status(
                order_id=data.get('order_id', ''),
                status=data.get('status', ''),
                notes=data.get('notes', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"order_id": "order identifier", "status": "new status", "notes": "additional notes"}'
            })
    
    def coordinate_with_support(self, input_data: str) -> str:
        """Coordinate with human support teams"""
        try:
            # Try to parse as JSON first, then as Python dict format
            try:
                data = json.loads(input_data)
            except json.JSONDecodeError:
                # Convert single quotes to double quotes and try again
                fixed_input = input_data.replace("'", '"')
                data = json.loads(fixed_input)
            
            result = self.api.coordinate_with_support(
                issue_type=data.get('issue_type', ''),
                priority=data.get('priority', 'medium'),
                details=data.get('details', '')
            )
            return json.dumps(result)
        except (json.JSONDecodeError, Exception) as e:
            return json.dumps({
                'success': False,
                'error': f'Invalid input format: {str(e)}',
                'expected_format': '{"issue_type": "issue category", "priority": "urgency level", "details": "issue details"}'
            })
