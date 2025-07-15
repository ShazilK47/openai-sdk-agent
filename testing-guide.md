# 🧪 **AI Agent API Testing Guide**

_Complete guide to testing your FastAPI AI Agent backend_

---

## 📋 **Table of Contents**

1. [Getting Started](#-getting-started)
2. [Basic Testing Methods](#-basic-testing-methods)
3. [Health Check Testing](#-health-check-testing)
4. [Tools Testing](#-tools-testing)
5. [Chat API Testing](#-chat-api-testing)
6. [Error Testing](#-error-testing)
7. [Performance Testing](#-performance-testing)
8. [Automated Testing](#-automated-testing)
9. [Troubleshooting](#-troubleshooting)

---

# 🚀 **Getting Started**

## **Prerequisites**

Before testing, make sure:

1. ✅ Your FastAPI server is running
2. ✅ All dependencies are installed
3. ✅ Environment variables are configured (API keys)

## **Starting the Server**

```powershell
# Navigate to your project directory
cd "c:\Users\khans\Desktop\GIAIC\Quarter-03\Agentic-Ai\openai-app"

# Start the FastAPI server
uv run uvicorn src.openai_app.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [67890]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**✅ Server Status Indicators:**

- ✅ **Running**: You see "Application startup complete"
- ❌ **Failed**: Error messages about imports or configuration
- ⚠️ **Warnings**: Deprecation warnings (these are normal)

---

# 🛠️ **Basic Testing Methods**

## **Method 1: PowerShell Commands (Recommended)**

PowerShell provides the best experience on Windows for API testing.

## **Method 2: Browser Testing**

Some endpoints can be tested directly in your browser.

## **Method 3: Python Script**

Automated testing using Python requests library.

---

# 💚 **Health Check Testing**

## **Basic Health Check**

**Purpose**: Verify the API is running and responding

### **PowerShell Command:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health"
```

### **Expected Response:**

```json
{
  "status": "healthy",
  "message": "AI Agent API is running",
  "version": "1.0.0",
  "timestamp": "2025-07-15T10:31:00.313813",
  "environment": {
    "python_version": "3.13.5",
    "log_level": "WARNING"
  }
}
```

### **Browser Test:**

Open in browser: `http://localhost:8000/api/health`

## **Detailed Health Check**

**Purpose**: Get system information and configuration status

### **PowerShell Command:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health/detailed"
```

### **Expected Response:**

```json
{
  "status": "healthy",
  "message": "AI Agent API is running",
  "version": "1.0.0",
  "timestamp": "2025-07-15T10:31:00.313813",
  "system": {
    "cpu_usage_percent": 15.2,
    "memory": {
      "total_mb": 8192.0,
      "available_mb": 4096.0,
      "used_percent": 50.0
    },
    "python_version": "3.13.5"
  },
  "configuration": {
    "log_level": "WARNING",
    "gemini_api_configured": true,
    "weather_api_configured": true,
    "tavily_api_configured": true
  }
}
```

### **✅ What to Check:**

- **status**: Should be "healthy"
- **configuration**: API keys should show `true` if configured
- **system**: CPU and memory usage should be reasonable

---

# 🔧 **Tools Testing**

## **List Available Tools**

**Purpose**: See all tools registered in your AI agent

### **PowerShell Command:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/available"
```

### **Expected Response:**

```json
{
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather information for any city",
      "parameters": {
        "type": "object",
        "properties": {
          "city": {
            "type": "string",
            "description": "City name to get weather for"
          }
        },
        "required": ["city"]
      }
    },
    {
      "name": "calculate",
      "description": "Perform mathematical calculations",
      "parameters": {
        "type": "object",
        "properties": {
          "expression": {
            "type": "string",
            "description": "Mathematical expression to evaluate"
          }
        },
        "required": ["expression"]
      }
    },
    {
      "name": "search_web",
      "description": "Search the internet for information",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Search query"
          }
        },
        "required": ["query"]
      }
    }
  ],
  "total_count": 3
}
```

### **✅ What to Check:**

- **total_count**: Should be 3
- **tools**: Should contain get_weather, calculate, search_web
- **parameters**: Each tool should have proper parameter definitions

## **Test Calculator Tool**

### **Simple Calculation:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {"expression": "2 + 2"}}'
```

**Expected Response:**

```json
{
  "tool_name": "calculate",
  "parameters": { "expression": "2 + 2" },
  "result": "2 + 2 = 4",
  "status": "success",
  "execution_time": 0.002,
  "error_message": null
}
```

### **Complex Calculation:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {"expression": "sqrt(16) + 10 * 2"}}'
```

**Expected Response:**

```json
{
  "tool_name": "calculate",
  "parameters": { "expression": "sqrt(16) + 10 * 2" },
  "result": "sqrt(16) + 10 * 2 = 24",
  "status": "success",
  "execution_time": 0.003,
  "error_message": null
}
```

### **Calculator Test Examples:**

```powershell
# Basic arithmetic
'{"tool_name": "calculate", "parameters": {"expression": "15 * 3"}}'

# With functions
'{"tool_name": "calculate", "parameters": {"expression": "sin(pi/2)"}}'

# Complex expression
'{"tool_name": "calculate", "parameters": {"expression": "(10 + 5) * 2 - 3"}}'
```

## **Test Weather Tool**

### **Get Weather for a City:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "get_weather", "parameters": {"city": "London"}}'
```

**Expected Response:**

```json
{
  "tool_name": "get_weather",
  "parameters": { "city": "London" },
  "result": "🌤️ Weather in London, GB:\nTemperature: 14°C (feels like 12°C)\nCondition: Clear Sky\nHumidity: 81%",
  "status": "success",
  "execution_time": 1.233,
  "error_message": null
}
```

### **Weather Test Examples:**

```powershell
# Different cities
'{"tool_name": "get_weather", "parameters": {"city": "New York"}}'
'{"tool_name": "get_weather", "parameters": {"city": "Tokyo"}}'
'{"tool_name": "get_weather", "parameters": {"city": "Paris"}}'
'{"tool_name": "get_weather", "parameters": {"city": "Karachi"}}'
```

### **✅ What to Check:**

- **status**: Should be "success"
- **result**: Should contain temperature, condition, humidity
- **execution_time**: Usually 1-3 seconds for API calls
- **error_message**: Should be null for valid cities

## **Test Search Tool**

### **Web Search:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "search_web", "parameters": {"query": "Python FastAPI tutorial"}}'
```

**Expected Response:**

```json
{
  "tool_name": "search_web",
  "parameters": { "query": "Python FastAPI tutorial" },
  "result": "Search results for 'Python FastAPI tutorial':\n**Quick Answer:** FastAPI is a high-performance Python web framework...\n1. **Python FastAPI Tutorial: Build a REST API**\n   URL: https://example.com/tutorial\n   Summary: Learn how to build APIs with FastAPI...",
  "status": "success",
  "execution_time": 2.401,
  "error_message": null
}
```

### **Search Test Examples:**

```powershell
# Technology searches
'{"tool_name": "search_web", "parameters": {"query": "machine learning trends 2025"}}'

# News searches
'{"tool_name": "search_web", "parameters": {"query": "latest AI developments"}}'

# How-to searches
'{"tool_name": "search_web", "parameters": {"query": "how to deploy FastAPI"}}'
```

---

# 💬 **Chat API Testing**

## **Send Message to AI Agent**

**Purpose**: Test the complete AI agent pipeline with tool usage

### **Simple Chat:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/message" -Method POST -ContentType "application/json" -Body '{"message": "What is 25 * 4?", "conversation_id": "test_001"}'
```

**Expected Response:**

```json
{
  "response": "The calculation 25 * 4 equals 100.",
  "conversation_id": "test_001",
  "tool_usage": [
    {
      "tool_name": "calculate",
      "parameters": { "expression": "25 * 4" },
      "result": "25 * 4 = 100",
      "status": "success",
      "execution_time": 0.002
    }
  ],
  "timestamp": "2025-07-15T10:31:00.313813"
}
```

### **Weather Chat:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/message" -Method POST -ContentType "application/json" -Body '{"message": "What is the weather like in Paris?", "conversation_id": "test_002"}'
```

### **Search Chat:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/message" -Method POST -ContentType "application/json" -Body '{"message": "Find information about Next.js 15 features", "conversation_id": "test_003"}'
```

### **Multi-Tool Chat:**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/message" -Method POST -ContentType "application/json" -Body '{"message": "Calculate 15 * 8 and then search for information about that number", "conversation_id": "test_004"}'
```

### **✅ What to Check:**

- **response**: Should be a natural language response
- **conversation_id**: Should match what you sent
- **tool_usage**: Should list tools that were used
- **timestamp**: Should be recent

---

# ❌ **Error Testing**

## **Test Invalid Tool Names**

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "invalid_tool", "parameters": {"test": "value"}}'
```

**Expected Response:**

```json
{
  "detail": "Tool 'invalid_tool' not found"
}
```

## **Test Invalid Parameters**

```powershell
# Missing required parameter
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {}}'

# Invalid expression
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {"expression": "2 + + 2"}}'
```

## **Test Invalid Endpoints**

```powershell
# Non-existent endpoint
Invoke-RestMethod -Uri "http://localhost:8000/api/invalid"
```

---

# ⚡ **Performance Testing**

## **Measure Response Times**

### **Create Performance Test Script:**

```powershell
# Time a health check
Measure-Command { Invoke-RestMethod -Uri "http://localhost:8000/api/health" }

# Time a calculation
Measure-Command { Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {"expression": "2 + 2"}}' }

# Time a weather request
Measure-Command { Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "get_weather", "parameters": {"city": "London"}}' }
```

### **✅ Expected Performance:**

- **Health Check**: < 50ms
- **Calculator**: < 10ms
- **Weather API**: 1-3 seconds
- **Search API**: 2-5 seconds
- **Chat API**: 2-10 seconds (depends on complexity)

---

# 🤖 **Automated Testing**

## **Using the Test Script**

We created a comprehensive test script (`test_api.py`) for automated testing:

```powershell
# Run all tests
uv run python test_api.py
```

**Expected Output:**

```
🚀 Testing FastAPI AI Agent Endpoints

🔍 Testing Health Endpoint...
Status: 200
Response: {
  "status": "healthy",
  "message": "AI Agent API is running",
  "version": "1.0.0"
}

🛠️ Testing Tools Endpoint...
Status: 200
Found 3 tools:
  - get_weather: Get current weather information for any city
  - calculate: Perform mathematical calculations
  - search_web: Search the internet for information

⚡ Testing Tool Execution...
Testing Calculator:
  Result: 10 * 5 + 2 = 52
  Time: 0.001s

💬 Testing Chat Endpoint...
Response: The answer is 45.
Tools used: 0

✅ All tests completed!
```

## **Create Custom Test Scripts**

### **Quick Calculator Test:**

```python
import requests

def test_calculator():
    expressions = ["2 + 2", "10 * 5", "sqrt(16)", "pi * 2"]

    for expr in expressions:
        response = requests.post(
            "http://localhost:8000/api/tools/execute",
            json={"tool_name": "calculate", "parameters": {"expression": expr}}
        )
        result = response.json()
        print(f"{expr} = {result['result']}")

test_calculator()
```

### **Weather Cities Test:**

```python
import requests

def test_weather_cities():
    cities = ["London", "New York", "Tokyo", "Sydney", "Karachi"]

    for city in cities:
        response = requests.post(
            "http://localhost:8000/api/tools/execute",
            json={"tool_name": "get_weather", "parameters": {"city": city}}
        )
        result = response.json()
        if result['status'] == 'success':
            print(f"✅ {city}: {result['result'][:50]}...")
        else:
            print(f"❌ {city}: {result['error_message']}")

test_weather_cities()
```

---

# 🌐 **Browser Testing**

## **Interactive API Documentation**

The best way to test APIs in browser:

1. **Open Swagger UI**: http://localhost:8000/docs
2. **Open ReDoc**: http://localhost:8000/redoc

### **Using Swagger UI:**

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out" button
4. Fill in the parameters
5. Click "Execute" to test

### **Endpoints You Can Test in Browser:**

- ✅ `GET /api/health` - Direct browser access
- ✅ `GET /api/health/detailed` - Direct browser access
- ✅ `GET /api/tools/available` - Direct browser access
- ❌ `POST` endpoints - Need Swagger UI or PowerShell

---

# 🔍 **Troubleshooting**

## **Common Issues & Solutions**

### **Issue 1: Server Not Starting**

**Symptoms:**

```
ModuleNotFoundError: No module named 'xyz'
```

**Solutions:**

```powershell
# Reinstall dependencies
uv sync

# Check if in correct directory
pwd

# Check Python path
uv run python -c "import sys; print(sys.path)"
```

### **Issue 2: API Key Errors**

**Symptoms:**

```json
{
  "detail": "API key not configured"
}
```

**Solutions:**

```powershell
# Check .env file exists
Get-Content .env

# Verify API keys are set
uv run python -c "from src.openai_app.config.settings import settings; print(f'Gemini: {bool(settings.gemini_api_key)}')"
```

### **Issue 3: Tool Execution Failures**

**Symptoms:**

```json
{
  "status": "error",
  "error_message": "Some error occurred"
}
```

**Solutions:**

```powershell
# Test individual tools
uv run python -c "
from src.openai_app.tools.registry import tool_registry
for tool in tool_registry.get_all_tools():
    print(f'Tool: {tool.name} - OK')
"

# Check tool imports
uv run python -c "from src.openai_app.tools.calculator import CalculatorTool; print('Calculator OK')"
```

### **Issue 4: CORS Errors**

**Symptoms:**

```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions:**

- This is normal if frontend isn't running yet
- CORS is already configured in the FastAPI app
- Will work when you add the frontend

### **Issue 5: Port Already in Use**

**Symptoms:**

```
Error: [Errno 48] Address already in use
```

**Solutions:**

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /F /PID 1234

# Or use a different port
uv run uvicorn src.openai_app.api.main:app --reload --port 8001
```

---

# 📊 **Testing Checklist**

## **Basic Health Check** ✅

- [ ] Server starts without errors
- [ ] Health endpoint returns 200
- [ ] Configuration shows API keys as configured
- [ ] System metrics are reasonable

## **Tools Testing** ✅

- [ ] All 3 tools listed in /api/tools/available
- [ ] Calculator tool works with simple expressions
- [ ] Calculator tool works with complex expressions
- [ ] Weather tool returns data for valid cities
- [ ] Search tool returns relevant results
- [ ] Error handling works for invalid inputs

## **Chat Integration** ✅

- [ ] Chat endpoint accepts messages
- [ ] Chat endpoint returns natural responses
- [ ] Tool usage is tracked and reported
- [ ] Conversation IDs work correctly

## **Error Handling** ✅

- [ ] Invalid tool names return 404
- [ ] Invalid parameters return appropriate errors
- [ ] Invalid endpoints return 404
- [ ] Server errors return 500 with details

## **Performance** ✅

- [ ] Health checks are fast (< 50ms)
- [ ] Calculator responses are fast (< 10ms)
- [ ] API calls complete within reasonable time
- [ ] No memory leaks during extended testing

## **Documentation** ✅

- [ ] Swagger UI loads at /docs
- [ ] ReDoc loads at /redoc
- [ ] All endpoints are documented
- [ ] Request/response schemas are clear

---

# 🎯 **Testing Best Practices**

## **Before Every Development Session:**

1. Start the server
2. Run quick health check
3. Test one tool to verify everything works

## **Before Committing Code:**

1. Run the full test script (`test_api.py`)
2. Check all endpoints manually
3. Verify error handling works

## **Performance Monitoring:**

1. Track response times
2. Monitor memory usage
3. Check for any timeout issues

## **Security Testing:**

1. Test with invalid inputs
2. Verify error messages don't leak sensitive data
3. Check that API keys aren't exposed in responses

---

# 🚀 **Next Steps**

## **Ready for Frontend Integration**

Once all tests pass, you're ready to:

1. **Week 2**: Build Next.js frontend
2. **Week 3**: Connect frontend to this API
3. **Week 4**: Add advanced features

## **Expanding the API**

To add more functionality:

1. Create new tools following the BaseTool pattern
2. Add new endpoints in the routes directory
3. Update the test script to include new features

---

# 📝 **Quick Reference Commands**

```powershell
# Start server
uv run uvicorn src.openai_app.api.main:app --reload --port 8000

# Health check
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# List tools
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/available"

# Test calculator
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "calculate", "parameters": {"expression": "2 + 2"}}'

# Test weather
Invoke-RestMethod -Uri "http://localhost:8000/api/tools/execute" -Method POST -ContentType "application/json" -Body '{"tool_name": "get_weather", "parameters": {"city": "London"}}'

# Test chat
Invoke-RestMethod -Uri "http://localhost:8000/api/chat/message" -Method POST -ContentType "application/json" -Body '{"message": "Calculate 5 * 5", "conversation_id": "test"}'

# Run all tests
uv run python test_api.py

# Open documentation
# Browser: http://localhost:8000/docs
```

---

**🎉 Happy Testing!**

Your FastAPI AI Agent backend is now fully tested and ready for production use! 🚀
