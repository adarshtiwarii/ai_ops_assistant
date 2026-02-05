"""
Executor Agent
Executes steps from the plan and calls appropriate tools
"""

from typing import Dict, Any, List
from tools import BaseTool


class ExecutorAgent:
    """Agent responsible for executing plan steps"""
    
    def __init__(self, tools: Dict[str, BaseTool]):
        self.tools = tools
        self.execution_history = []
    
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute all steps in the plan
        
        Args:
            plan: Execution plan from planner
            
        Returns:
            Dict with execution results
        """
        steps = plan.get("steps", [])
        if not steps:
            return {
                "success": False,
                "error": "No steps to execute",
                "results": []
            }
        
        results = []
        context = {}  # Store results for later steps
        
        for step in steps:
            step_result = self.execute_step(step, context)
            results.append(step_result)
            
            # Store successful results in context
            if step_result["success"]:
                step_key = f"step_{step.get('step_number', len(results))}"
                context[step_key] = step_result["result"]
            
            # If critical step fails, stop execution
            if not step_result["success"] and step.get("critical", False):
                return {
                    "success": False,
                    "error": f"Critical step {step.get('step_number')} failed",
                    "results": results,
                    "partial_context": context
                }
        
        return {
            "success": True,
            "results": results,
            "context": context
        }
    
    def execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a single step
        
        Args:
            step: Step definition from plan
            context: Results from previous steps
            
        Returns:
            Dict with step execution result
        """
        step_number = step.get("step_number", "unknown")
        description = step.get("description", "No description")
        tool_name = step.get("tool")
        parameters = step.get("parameters", {})
        
        # Log step execution
        self.execution_history.append({
            "step": step_number,
            "description": description,
            "tool": tool_name
        })
        
        # If no tool needed, it's a processing step
        if not tool_name or tool_name == "null" or tool_name == "none":
            return {
                "success": True,
                "step_number": step_number,
                "description": description,
                "result": {
                    "type": "processing",
                    "message": "Processing step completed",
                    "context_available": list(context.keys())
                }
            }
        
        # Check if tool exists
        if tool_name not in self.tools:
            return {
                "success": False,
                "step_number": step_number,
                "description": description,
                "error": f"Tool '{tool_name}' not found",
                "result": None
            }
        
        # Execute tool with retry logic
        max_retries = 2
        last_error = None
        
        for attempt in range(max_retries):
            try:
                tool = self.tools[tool_name]
                tool_result = tool.execute(**parameters)
                
                if tool_result.get("success"):
                    return {
                        "success": True,
                        "step_number": step_number,
                        "description": description,
                        "tool": tool_name,
                        "result": tool_result.get("data")
                    }
                else:
                    last_error = tool_result.get("error", "Unknown error")
                    
                    # Don't retry on certain errors
                    if "not configured" in last_error.lower() or "not found" in last_error.lower():
                        break
            
            except Exception as e:
                last_error = str(e)
        
        return {
            "success": False,
            "step_number": step_number,
            "description": description,
            "tool": tool_name,
            "error": last_error,
            "result": None
        }
    
    def get_execution_summary(self) -> str:
        """Get summary of execution history"""
        if not self.execution_history:
            return "No steps executed"
        
        summary = "Execution Summary:\n"
        for entry in self.execution_history:
            summary += f"- Step {entry['step']}: {entry['description']}"
            if entry['tool']:
                summary += f" (using {entry['tool']})"
            summary += "\n"
        
        return summary
