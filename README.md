# AI Google Search Query Generator

https://github.com/user-attachments/assets/a3f73332-2d13-4614-a8ef-b048a96e358e

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt-6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-red.svg)](https://docs.pydantic.dev/)
[![PydanticAI](https://img.shields.io/badge/PydanticAI-Latest-blueviolet.svg)](https://pydantic-ai.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful desktop application that uses AI to generate optimized Google search queries from natural language inputs.

## 📋 Features

- **AI-Powered Search Query Generation**: Transforms natural language into optimized Google search queries
- **Smart Query Refinement**: Uses Google search operators to create more effective search strings
- **System Tray Integration**: Minimizes to system tray for easy access

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher
- OpenAI API key

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/pakagronglb/ai-google-search-query.git
   cd ai-google-search-query
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key
   ```
   OPENAI_API_KEY="your-api-key-here"
   ```

## 🚀 Usage

1. Run the application
   ```bash
   python app.py
   ```

2. Enter your search query in natural language
   ```
   Find verified customer reviews for the latest smartphones without fake ratings
   ```

3. Click "Search" or press Enter to generate and execute the optimized query
   ```
   ("iPhone 15 Pro review" OR "Samsung Galaxy S24 review") ("verified purchase" OR "real customer review") -"sponsored post" -"paid review" site:bestbuy.com OR site:amazon.com OR site:trustpilot.com OR site:reddit.com
   ```

4. The application will automatically open your default browser with the generated search query

## 💡 How It Works

The application uses:
- **OpenAI's GPT-4o-mini** for natural language processing
- **PydanticAI** for structured AI interactions
- **PyQt6** for the desktop interface

The AI agent is configured to:
1. Correct any typos or errors in the user input
2. Identify the main topic of the search
3. Apply Google search operators to refine the query
4. Construct and execute an optimized search query

## 🛠️ Technical Details

- **Architecture**: Standalone desktop application with AI backend
- **AI Framework**: PydanticAI with OpenAI integration
- **UI Framework**: PyQt6
- **Packaging**: Compatible with PyInstaller for distribution

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- Project based on a tutorial by [Jie Jenn](https://www.youtube.com/watch?v=x-lFluXYLNs&pp=ygUIamllIGplbm4%3D)
- Icons from [Flaticon](https://www.flaticon.com/)
- Built with [PydanticAI](https://github.com/jxnl/pydantic-ai) 
