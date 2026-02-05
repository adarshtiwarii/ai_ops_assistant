# 🚀 Quick Start Guide - AI Operations Assistant

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd ai_ops_assistant
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy example file
cp env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

Your `.env` should look like:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Optional (for enhanced functionality)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxx
NEWS_API_KEY=xxxxxxxxxxxxx
```

### Step 3: Run the Assistant
```bash
python main.py
```

## Getting API Keys

### 1. OpenAI (REQUIRED) ⚡
- Go to: https://platform.openai.com/api-keys
- Sign up / Login
- Click "Create new secret key"
- Copy and paste into `.env`
- **Cost**: ~$0.002 per request (very cheap!)

### 2. GitHub (Optional but Recommended) 🐙
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- No scopes needed for public repos
- Copy token to `.env`
- **Benefit**: Higher rate limits (5000/hour vs 60/hour)

### 3. OpenWeatherMap (Optional) 🌤️
- Go to: https://openweathermap.org/api
- Sign up for free
- Get API key from dashboard
- **Free Tier**: 1000 calls/day

### 4. NewsAPI (Optional) 📰
- Go to: https://newsapi.org/register
- Instant API key after registration
- **Free Tier**: 100 requests/day

## Example Commands to Try

```
You: Find top 5 Python projects on GitHub

You: What's the weather in London?

You: Latest tech news

You: Search for machine learning repos and weather in Tokyo

You: Find trending JavaScript frameworks

You: Get news about artificial intelligence
```

## Validation

Before running, validate your setup:
```bash
python validate.py
```

This checks:
- ✓ All files present
- ✓ Dependencies installed
- ✓ Modules importable
- ✓ Environment configured

## Demo Mode

See example outputs without API keys:
```bash
python demo.py
```

## Project Structure (Simple View)

```
ai_ops_assistant/
├── main.py              ← Start here
├── agents/              ← Planner, Executor, Verifier
├── tools/               ← GitHub, Weather, News APIs
├── llm/                 ← OpenAI integration
├── requirements.txt     ← Dependencies
├── .env                 ← Your API keys (create this!)
└── README.md           ← Full documentation
```

## Troubleshooting

### "OPENAI_API_KEY not found"
→ Create `.env` file and add your key

### "Module not found"
→ Run: `pip install -r requirements.txt`

### "Rate limit exceeded" (GitHub)
→ Add GITHUB_TOKEN to `.env`

### "Invalid API key"
→ Check your key has no extra spaces/quotes

## Architecture Summary

```
User Input → Planner Agent → Executor Agent → Verifier Agent → Response
             (Plans steps)   (Calls APIs)     (Validates)
```

**Planner** 🧠: Breaks down task into steps
**Executor** ⚙️: Runs steps and calls APIs  
**Verifier** 🔍: Checks results and formats output

## What Makes This Special?

✅ **Multi-Agent**: Not just one LLM call - proper pipeline
✅ **Real APIs**: Actually calls GitHub, Weather, News
✅ **Error Handling**: Retries, fallbacks, graceful failures
✅ **Structured**: JSON planning, typed Python code
✅ **Extensible**: Easy to add new tools/agents
✅ **Production-Ready**: Proper logging, validation, docs

## Next Steps

1. **Run basic examples** to understand the flow
2. **Add optional API keys** for full functionality
3. **Try complex queries** using multiple tools
4. **Check main README.md** for detailed docs

## Support

For issues or questions:
1. Check README.md (comprehensive guide)
2. Run `python validate.py` for diagnostics
3. Review error messages (they're descriptive!)

---

**Total Setup Time**: ~5 minutes
**Lines of Code**: ~1500+
**Test Coverage**: All core components
**Documentation**: Complete

Ready to go! 🚀
