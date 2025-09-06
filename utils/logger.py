import logging
import sys
from datetime import datetime
from typing import Optional

def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Setup and configure logger for the Synapse project
    
    Args:
        name: Logger name (if None, uses root logger)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logger_name = name or "synapse"
    logger = logging.getLogger(logger_name)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"synapse.{name}")

class ActionLogger:
    """
    Specialized logger for tracking agent actions and decisions
    """
    
    def __init__(self):
        self.logger = get_logger("actions")
        self.action_history = []
    
    def log_action(self, action_type: str, tool_name: str, input_data: str, 
                   output_data: str, execution_time: float, success: bool):
        """Log an agent action with detailed information"""
        
        action_record = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "tool_name": tool_name,
            "input": input_data[:200],  # Truncate long inputs
            "output": output_data[:200],  # Truncate long outputs
            "execution_time_seconds": execution_time,
            "success": success
        }
        
        self.action_history.append(action_record)
        
        # Log to console
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"ACTION {status}: {tool_name} - {execution_time:.2f}s"
        )
        
        if not success:
            self.logger.warning(f"Action failed: {tool_name} - {output_data[:100]}")
    
    def log_reasoning_step(self, step_number: int, thought: str, 
                          action: str, observation: str):
        """Log a reasoning step in the ReAct pattern"""
        
        self.logger.info(f"REASONING STEP {step_number}:")
        self.logger.info(f"  Thought: {thought[:150]}...")
        self.logger.info(f"  Action: {action}")
        self.logger.info(f"  Observation: {observation[:150]}...")
    
    def log_scenario_start(self, scenario: str):
        """Log the start of scenario resolution"""
        self.logger.info("=" * 50)
        self.logger.info(f"STARTING SCENARIO RESOLUTION")
        self.logger.info(f"Scenario: {scenario[:200]}...")
        self.logger.info("=" * 50)
    
    def log_scenario_end(self, success: bool, total_time: float, 
                        steps_taken: int):
        """Log the end of scenario resolution"""
        status = "COMPLETED SUCCESSFULLY" if success else "FAILED"
        self.logger.info("=" * 50)
        self.logger.info(f"SCENARIO RESOLUTION {status}")
        self.logger.info(f"Total time: {total_time:.2f} seconds")
        self.logger.info(f"Steps taken: {steps_taken}")
        self.logger.info("=" * 50)
    
    def get_action_history(self) -> list:
        """Get the complete action history"""
        return self.action_history.copy()
    
    def clear_history(self):
        """Clear the action history"""
        self.action_history.clear()
        self.logger.info("Action history cleared")

# Create global action logger instance
action_logger = ActionLogger()
