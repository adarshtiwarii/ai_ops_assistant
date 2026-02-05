"""
Demo Script
Shows example tasks and expected outputs (simulated)
"""

def print_demo():
    """Print demo scenarios"""
    
    print("\n" + "="*70)
    print("AI OPERATIONS ASSISTANT - DEMO SCENARIOS")
    print("="*70)
    
    scenarios = [
        {
            "task": "Find top 3 Python projects on GitHub",
            "plan_steps": [
                "Search GitHub API for Python repositories",
                "Sort by stars in descending order",
                "Extract top 3 results with names and descriptions"
            ],
            "tools_used": ["github_search"],
            "sample_output": """
Top 3 Python Projects on GitHub:

1. **Python** (Python/cpython) - 195K+ stars
   - The Python programming language
   - Official Python repository

2. **System Design Primer** (donnemartin/system-design-primer) - 180K+ stars
   - Learn how to design large-scale systems
   - Preparation resources for system design interviews

3. **Python Algorithms** (TheAlgorithms/Python) - 160K+ stars
   - All algorithms implemented in Python
   - For education and learning
"""
        },
        {
            "task": "What's the weather in Mumbai and latest tech news?",
            "plan_steps": [
                "Fetch current weather for Mumbai using weather API",
                "Fetch latest tech news headlines",
                "Combine and format results"
            ],
            "tools_used": ["weather_fetch", "news_fetch"],
            "sample_output": """
**Weather in Mumbai:**
- Temperature: 28°C (feels like 31°C)
- Conditions: Partly cloudy
- Humidity: 75%
- Wind Speed: 12 km/h

**Latest Tech News:**
1. "AI Breakthrough: New Model Surpasses GPT-4" - TechCrunch
2. "Apple Announces Vision Pro 2" - The Verge
3. "Quantum Computing Milestone Achieved" - MIT Technology Review
"""
        },
        {
            "task": "Search for machine learning repositories and weather in London",
            "plan_steps": [
                "Search GitHub for machine learning repos",
                "Get current weather in London",
                "Format combined results"
            ],
            "tools_used": ["github_search", "weather_fetch"],
            "sample_output": """
**Machine Learning Repositories:**

1. TensorFlow (175K stars) - ML framework by Google
2. scikit-learn (52K stars) - ML library for Python
3. PyTorch (65K stars) - Deep learning framework

**Current Weather in London:**
- Temperature: 12°C
- Conditions: Light rain
- Humidity: 88%
"""
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'─'*70}")
        print(f"SCENARIO {i}")
        print(f"{'─'*70}")
        print(f"\n📝 User Task:")
        print(f"   {scenario['task']}")
        print(f"\n🧠 Planner Agent Output:")
        print(f"   Steps to execute:")
        for j, step in enumerate(scenario['plan_steps'], 1):
            print(f"     {j}. {step}")
        print(f"\n⚙️  Executor Agent:")
        print(f"   Tools used: {', '.join(scenario['tools_used'])}")
        print(f"\n🔍 Verifier Agent:")
        print(f"   ✓ All steps completed successfully")
        print(f"   ✓ Results verified and formatted")
        print(f"\n📋 Final Output:")
        print(scenario['sample_output'])
    
    print("\n" + "="*70)
    print("ARCHITECTURE HIGHLIGHTS")
    print("="*70)
    print("""
1. **Separation of Concerns**
   - Planner: Converts natural language to structured plan
   - Executor: Runs steps and calls APIs
   - Verifier: Validates completeness and formats output

2. **LLM Integration**
   - JSON-constrained outputs for reliability
   - Temperature tuning per agent role
   - Fallback mechanisms for LLM failures

3. **Error Handling**
   - Automatic retries on API failures
   - Graceful degradation with partial results
   - Clear error messages for users

4. **API Integrations**
   - GitHub API: Repository search and metadata
   - Weather API: Real-time weather data
   - News API: Latest headlines and articles

5. **Extensibility**
   - Easy to add new tools (inherit BaseTool)
   - Plugin architecture for agents
   - Configuration via environment variables
""")
    
    print("\n" + "="*70)
    print("GETTING STARTED")
    print("="*70)
    print("""
1. Install dependencies:
   pip install -r requirements.txt

2. Configure API keys in .env:
   cp env.example .env
   # Edit .env and add your OPENAI_API_KEY

3. Run the assistant:
   python main.py

4. Try these example commands:
   - "Find top Python projects on GitHub"
   - "What's the weather in Mumbai?"
   - "Latest tech news"
   - "Search for AI repositories and weather in Tokyo"
""")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_demo()
