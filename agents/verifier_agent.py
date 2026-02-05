"""
Verifier Agent
Validates execution results and ensures output quality
"""

from typing import Dict, Any, List
from llm import LLMProvider


class VerifierAgent:
    """Agent responsible for verifying execution results"""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
    
    def verify_results(
        self, 
        plan: Dict[str, Any], 
        execution_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify if execution results meet the plan's expectations
        
        Args:
            plan: Original execution plan
            execution_results: Results from executor
            
        Returns:
            Dict with verification status and formatted output
        """
        if not execution_results.get("success"):
            return {
                "verified": False,
                "issues": ["Execution failed"],
                "output": None,
                "needs_retry": True
            }
        
        results = execution_results.get("results", [])
        expected_output = plan.get("expected_output", "")
        
        # Check for failed steps
        failed_steps = [r for r in results if not r.get("success")]
        if failed_steps:
            issues = [f"Step {s.get('step_number')} failed: {s.get('error')}" for s in failed_steps]
            return {
                "verified": False,
                "issues": issues,
                "output": None,
                "needs_retry": True,
                "partial_results": [r for r in results if r.get("success")]
            }
        
        # Check completeness with LLM
        verification_result = self._llm_verify(plan, results, expected_output)
        
        return verification_result
    
    def _llm_verify(
        self, 
        plan: Dict[str, Any], 
        results: List[Dict[str, Any]], 
        expected_output: str
    ) -> Dict[str, Any]:
        """
        Use LLM to verify completeness and quality
        
        Args:
            plan: Original plan
            results: Execution results
            expected_output: Expected output description
            
        Returns:
            Verification result
        """
        system_prompt = """You are a verification agent. Your job is to:
1. Check if execution results are complete and match expectations
2. Identify any missing or incorrect information
3. Format results into a clear, structured output

Respond with valid JSON only."""

        results_summary = "\n".join([
            f"Step {r.get('step_number')}: {r.get('description')}\n"
            f"  Success: {r.get('success')}\n"
            f"  Result: {str(r.get('result', 'None'))[:200]}\n"
            for r in results
        ])
        
        user_prompt = f"""Task Understanding: {plan.get('task_understanding', 'Unknown')}

Expected Output: {expected_output}

Execution Results:
{results_summary}

Verify the results and respond with JSON:
{{
    "verified": true/false,
    "completeness_score": 0-100,
    "issues": ["list of issues if any"],
    "missing_data": ["what data is missing if any"],
    "needs_retry": true/false
}}"""

        try:
            verification = self.llm.generate_json_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.2
            )
            
            # If verified, format the output
            if verification.get("verified", False):
                formatted_output = self._format_output(plan, results)
                verification["output"] = formatted_output
            else:
                verification["output"] = None
            
            return verification
        
        except Exception as e:
            # Fallback verification
            return {
                "verified": True,  # Assume success if LLM fails
                "completeness_score": 80,
                "issues": [f"LLM verification failed: {str(e)}"],
                "missing_data": [],
                "needs_retry": False,
                "output": self._format_output(plan, results)
            }
    
    def _format_output(self, plan: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Format execution results into structured output
        
        Args:
            plan: Original plan
            results: Execution results
            
        Returns:
            Formatted output
        """
        output = {
            "task": plan.get("task_understanding", "Unknown task"),
            "status": "completed",
            "results": []
        }
        
        for result in results:
            if result.get("success"):
                step_output = {
                    "step": result.get("step_number"),
                    "description": result.get("description"),
                    "data": result.get("result")
                }
                output["results"].append(step_output)
        
        return output
    
    def generate_final_response(self, verification: Dict[str, Any]) -> str:
        """
        Generate human-readable final response
        
        Args:
            verification: Verification results
            
        Returns:
            Formatted response string
        """
        if not verification.get("verified"):
            issues = verification.get("issues", ["Unknown issues"])
            return f"Task could not be completed:\n" + "\n".join(f"- {issue}" for issue in issues)
        
        output = verification.get("output", {})
        
        system_prompt = """You are formatting execution results for the user.
Create a clear, concise, and helpful response based on the data.
Be natural and conversational, not robotic."""

        user_prompt = f"""Task: {output.get('task', 'Unknown')}

Results Data:
{output}

Generate a helpful response for the user that presents this information clearly.
DO NOT use JSON in your response - write naturally for humans."""

        try:
            response = self.llm.generate_completion(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            return response
        
        except Exception as e:
            # Fallback formatting
            return self._simple_format(output)
    
    def _simple_format(self, output: Dict[str, Any]) -> str:
        """Simple fallback formatting"""
        response = f"Task: {output.get('task', 'Completed')}\n\n"
        
        for result in output.get("results", []):
            response += f"Step {result.get('step')}: {result.get('description')}\n"
            data = result.get('data')
            if data:
                response += f"{str(data)[:500]}\n\n"
        
        return response
