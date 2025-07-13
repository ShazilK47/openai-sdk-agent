# OpenAI Agents Application

A professional, enterprise-grade AI agents application built with Python 3.13 and modern development practices.

## Features

### 🤖 AI Agents

- **Weather Agent**: Specialized agent for weather-related queries with real-time data
- **General Agent**: Multi-purpose agent for various tasks and conversations
- Built on OpenAI Agents framework with Gemini API integration

### 🌤️ Real Weather Data

- **Live Weather API**: Real-time weather data from OpenWeatherMap
- **Multiple Cities**: Query weather for multiple cities in a single request
- **Detailed Information**: Temperature, humidity, wind speed, weather conditions
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Temperature Units**: Celsius with "feels like" temperature

### 🛠️ Professional Architecture

- **Modular Design**: Clean separation of concerns with services, tools, and configuration
- **Environment Configuration**: Secure API key management with `.env` files
- **Structured Logging**: Configurable logging with quiet/verbose modes
- **Extensible Tools**: Plugin-based tool architecture for easy feature additions
- **Service Layer**: Business logic separated from presentation

### 🔧 Developer Features

- **CLI Interface**: Command-line interface with multiple interaction modes
- **Error Handling**: Comprehensive error handling and logging
- **Type Safety**: Full type hints and Pydantic validation
- **Testing Ready**: Modular structure supports easy unit testing
- **Modern Python**: Built with Python 3.13 and UV package manager

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- OpenWeatherMap API key (free at https://openweathermap.org/api)
- Gemini API key (free at https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd openai-app
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Configure your `.env` file**:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```

### Usage

#### Single Query Mode

```bash
# Get weather for one city
uv run openai-app "What's the weather in London?"

# Get weather for multiple cities
uv run openai-app "What's the weather like in Tokyo and New York?"

# Travel planning
uv run openai-app "I'm planning a trip. Can you tell me the weather in Paris, Rome, and Bangkok?"
```

#### Interactive Mode

```bash
# Start interactive session
uv run openai-app --interactive

# With verbose logging
uv run openai-app --interactive --verbose
```

#### Quiet Mode

```bash
# Minimal output
uv run openai-app --quiet "Weather in Sydney?"
```

## Weather API Features

### Real-Time Data

The application fetches live weather data including:

- **Current conditions**: Clear, cloudy, rainy, etc.
- **Temperature**: Actual and "feels like" temperatures in Celsius
- **Humidity**: Relative humidity percentage
- **Wind**: Wind speed in meters per second
- **Location validation**: Handles invalid city names gracefully

### Example Outputs

```
The weather in London is clear sky with a temperature of 26°C, humidity 41%, and wind speed 3.4 m/s.
```

```
The weather in Tokyo is broken clouds with a temperature of 26°C (feels like 27°C), humidity 78%, and wind speed 3.42 m/s.
The weather in New York is overcast clouds with a temperature of 28°C (feels like 31°C), humidity 74%, and wind speed 4.42 m/s.
```

### Fallback Behavior

- If weather API is unavailable, falls back to simulation
- Invalid city names return user-friendly error messages
- Network errors are handled gracefully with logging

## Configuration

### Environment Variables

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here

# Optional - API Configuration
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5

# Optional - Application Settings
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=development
TRACING_ENABLED=false
```

### Logging Levels

- `ERROR`: Only errors
- `WARNING`: Errors and warnings (default)
- `INFO`: General information
- `DEBUG`: Detailed debugging information

## Architecture

### Project Structure

```
src/openai_app/
├── config/          # Configuration and settings
├── core/            # Core business logic (agents, models)
├── services/        # Application services
├── tools/           # Agent tools (weather, calculator, etc.)
├── utils/           # Utility functions (weather API)
├── cli/             # Command-line interface
└── main.py          # Application entry point
```

### Key Components

- **Settings**: Pydantic-based configuration management
- **Logging**: Structured logging with configurable output
- **Agent Factory**: Creates specialized agents for different tasks
- **Tool Registry**: Manages available tools and capabilities
- **Weather API Service**: Handles external weather API calls

## Development

### Adding New Tools

1. Create a new tool class in `src/openai_app/tools/`
2. Inherit from `BaseTool`
3. Implement `execute()` and `get_function_tool()` methods
4. Register in `src/openai_app/tools/registry.py`

### Extending Agents

1. Add new agent factory methods in `src/openai_app/core/agents.py`
2. Configure tools and capabilities
3. Update CLI commands if needed

## Contributing

1. Follow existing code style and patterns
2. Add type hints for all functions
3. Include proper error handling and logging
4. Update documentation for new features

## License

[Add your license information here]
