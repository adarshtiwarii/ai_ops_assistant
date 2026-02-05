"""
AI Operations Assistant
Main orchestrator that coordinates all agents
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from llm import LLMProvider
from tools import GitHubTool, WeatherTool, NewsTool
from agents import PlannerAgent, ExecutorAgent, VerifierAgent


class AIOperationsAssistant:
    """Main AI Operations Assistant orchestrator"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize LLM provider
        self.llm = LLMProvider()
        
        # Initialize tools
        self.tools = {
            "github_search": GitHubTool(),
            "weather_fetch": WeatherTool(),
            "news_fetch": NewsTool()
        }
        
        # Get tool information for planner
        available_tools = [tool.get_tool_info() for tool in self.tools.values()]
        
        # Initialize agents
        self.planner = PlannerAgent(self.llm, available_tools)
        self.executor = ExecutorAgent(self.tools)
        self.verifier = VerifierAgent(self.llm)
        
        print("✓ AI Operations Assistant initialized")
        print(f"✓ {len(self.tools)} tools available: {', '.join(self.tools.keys())}")
    
    def process_task(self, user_task: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Process a user task through the complete pipeline
        
        Args:
            user_task: Natural language task from user
            verbose: Print detailed execution logs
            
        Returns:
            Dict with final results and metadata
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"USER TASK: {user_task}")
            print(f"{'='*60}\n")
        
        # Step 1: Planning
        if verbose:
            print("🧠 PLANNER AGENT: Creating execution plan...")
        
        plan_result = self.planner.create_plan(user_task)
        
        if not plan_result["success"]:
            return {
                "success": False,
                "error": plan_result["error"],
                "stage": "planning"
            }
        
        plan = plan_result["plan"]
        
        if verbose:
            print(f"   Task Understanding: {plan.get('task_understanding', 'N/A')}")
            print(f"   Steps: {len(plan.get('steps', []))}")
            for step in plan.get('steps', []):
                print(f"     {step.get('step_number')}. {step.get('description')}")
                if step.get('tool'):
                    print(f"        Tool: {step.get('tool')}")
            print()
        
        # Step 2: Execution
        if verbose:
            print("⚙️  EXECUTOR AGENT: Executing plan...")
        
        execution_result = self.executor.execute_plan(plan)
        
        if verbose:
            for result in execution_result.get("results", []):
                status = "✓" if result.get("success") else "✗"
                print(f"   {status} Step {result.get('step_number')}: {result.get('description')}")
                if not result.get("success"):
                    print(f"      Error: {result.get('error')}")
            print()
        
        # Step 3: Verification
        if verbose:
            print("🔍 VERIFIER AGENT: Validating results...")
        
        verification = self.verifier.verify_results(plan, execution_result)
        
        if verbose:
            print(f"   Verified: {verification.get('verified', False)}")
            print(f"   Completeness: {verification.get('completeness_score', 'N/A')}%")
            if verification.get('issues'):
                print(f"   Issues: {', '.join(verification['issues'])}")
            print()
        
        # Step 4: Generate final response
        if verification.get("verified"):
            if verbose:
                print("📝 Generating final response...\n")
            
            final_response = self.verifier.generate_final_response(verification)
            
            return {
                "success": True,
                "response": final_response,
                "metadata": {
                    "plan": plan,
                    "verification": verification,
                    "execution_summary": self.executor.get_execution_summary()
                }
            }
        else:
            # Handle failures gracefully
            return {
                "success": False,
                "error": "Task verification failed",
                "issues": verification.get("issues", []),
                "partial_results": verification.get("output"),
                "needs_retry": verification.get("needs_retry", False)
            }
    
    def interactive_mode(self):
        """Run assistant in interactive CLI mode"""
        print("\n" + "="*60)
        print("AI OPERATIONS ASSISTANT - Interactive Mode")
        print("="*60)
        print("\nType 'quit' or 'exit' to stop\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\nGoodbye! 👋\n")
                    break
                
                if not user_input:
                    continue
                
                result = self.process_task(user_input, verbose=True)
                
                if result["success"]:
                    print(f"\n{'='*60}")
                    print("FINAL RESPONSE:")
                    print(f"{'='*60}")
                    print(result["response"])
                    print()
                else:
                    print(f"\n❌ Error: {result.get('error')}")
                    if result.get('issues'):
                        print("Issues:")
                        for issue in result['issues']:
                            print(f"  - {issue}")
                    print()
            
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye! 👋\n")
                break
            
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}\n")


def main():
    """Main entry point"""
    try:
        assistant = AIOperationsAssistant()
        assistant.interactive_mode()
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from env.example)")
        print("2. Added your OPENAI_API_KEY")
        print("3. (Optional) Added API keys for GitHub, Weather, and News\n")
    
    except Exception as e:
        print(f"\n❌ Startup Error: {str(e)}\n")


if __name__ == "__main__":
    main()
