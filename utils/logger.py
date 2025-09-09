import logging
import sys
from datetime import datetime
from typing import Optional


def setup_logger(name: str = "synapse_agent", level: int = logging.INFO) -> logging.Logger:
    """
    Set up a comprehensive logger for the Synapse agent system.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


class AgentLogger:
    """
    Specialized logger for agent execution tracking and debugging.
    """
    
    def __init__(self, agent_name: str = "SynapseAgent"):
        self.logger = setup_logger(f"agent.{agent_name}")
        self.execution_id: Optional[str] = None
        self.step_counter = 0
    
    def start_execution(self, scenario: str) -> str:
        """Start a new execution session"""
        self.execution_id = f"exec_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.step_counter = 0
        self.logger.info(f"[{self.execution_id}] Starting execution for scenario: {scenario[:100]}...")
        return self.execution_id
    
    def log_step(self, step_type: str, details: str, success: bool = True):
        """Log an execution step"""
        self.step_counter += 1
        status = "✅" if success else "❌"
        self.logger.info(f"[{self.execution_id}] Step {self.step_counter} - {step_type} {status}: {details}")
    
    def log_tool_use(self, tool_name: str, input_data: str, output_data: str, success: bool = True):
        """Log tool usage"""
        status = "✅" if success else "❌"
        self.logger.info(f"[{self.execution_id}] Tool: {tool_name} {status}")
        self.logger.debug(f"[{self.execution_id}] Tool Input: {input_data}")
        self.logger.debug(f"[{self.execution_id}] Tool Output: {output_data}")
    
    def log_decision(self, decision: str, reasoning: str):
        """Log agent decisions and reasoning"""
        self.logger.info(f"[{self.execution_id}] Decision: {decision}")
        self.logger.info(f"[{self.execution_id}] Reasoning: {reasoning}")
    
    def log_resolution(self, success: bool, solution: str, execution_time: float):
        """Log final resolution"""
        status = "✅ SUCCESSFUL" if success else "❌ FAILED"
        self.logger.info(f"[{self.execution_id}] Resolution {status} in {execution_time:.2f}s")
        self.logger.info(f"[{self.execution_id}] Solution: {solution}")
    
    def log_error(self, error: str, context: str = ""):
        """Log errors with context"""
        self.logger.error(f"[{self.execution_id}] ERROR: {error}")
        if context:
            self.logger.error(f"[{self.execution_id}] Context: {context}")
    
    def log_debug(self, message: str):
        """Log debug information"""
        self.logger.debug(f"[{self.execution_id}] DEBUG: {message}")


# Global logger instance for general use
logger = setup_logger()
