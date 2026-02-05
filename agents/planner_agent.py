"""
Planner Agent
Converts user input into structured execution plan with steps and tools
"""

from typing import Dict, Any, List
from llm import LLMProvider


class PlannerAgent:
    """Agent responsible for planning task execution"""
    
    def __init__(self, llm_provider: LLMProvider, available_tools: List[Dict[str, str]]):
        self.llm = llm_provider
        self.available_tools = available_tools
    
    def create_plan(self, user_task: str) -> Dict[str, Any]:
        """
        Create execution plan from user task
        
        Args:
            user_task: Natural language task description
            
        Returns:
            Dict with plan containing steps and required tools
        """
        
        tools_description = "\n".join([
            f"- {tool['name']}: {tool['description']}" 
            for tool in self.available_tools
        ])
        
        system_prompt = """You are a planning agent in an AI Operations Assistant system.
Your job is to break down user tasks into clear, executable steps.

For each step, you must:
1. Describe what needs to be done
2. Identify which tool (if any) is needed
3. Specify the tool parameters

Respond ONLY with a valid JSON object following this exact schema:
{
    "task_understanding": "Brief summary of what the user wants",
    "steps": [
        {
            "step_number": 1,
            "description": "What this step does",
            "tool": "tool_name or null",
            "parameters": {}
        }
    ],
    "expected_output": "What the final result should contain"
}"""

        user_prompt = f"""User Task: {user_task}

Available Tools:
{tools_description}

Create a detailed execution plan with numbered steps. Each step should either:
- Call a specific tool with proper parameters
- Process or combine results from previous steps
- Format the final output

Remember to respond with ONLY valid JSON."""

        try:
            plan = self.llm.generate_json_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3
            )
            
            # Validate plan structure
            if not isinstance(plan, dict) or "steps" not in plan:
                raise ValueError("Invalid plan structure")
            
            if not isinstance(plan["steps"], list) or len(plan["steps"]) == 0:
                raise ValueError("Plan must contain at least one step")
            
            return {
                "success": True,
                "plan": plan
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Planning failed: {str(e)}",
                "plan": None
            }
    
    def refine_plan(self, original_plan: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """
        Refine plan based on execution feedback
        
        Args:
            original_plan: Original execution plan
            feedback: Feedback from verifier or executor
            
        Returns:
            Refined plan
        """
        system_prompt = """You are refining an execution plan based on feedback.
Adjust the plan to address any issues while maintaining the original intent.
Respond with valid JSON only."""

        user_prompt = f"""Original Plan:
{original_plan}

Feedback:
{feedback}

Create an improved plan that addresses the feedback."""

        try:
            refined_plan = self.llm.generate_json_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3
            )
            
            return {
                "success": True,
                "plan": refined_plan
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Plan refinement failed: {str(e)}",
                "plan": original_plan
            }
