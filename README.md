# TTGD
Turing Tumble Game Developemt

## Features

- **Interactive Frontend & Backend** – A full web implementation of Turing Tumble  
- **AI-Generated Challenges** – Dynamic puzzles tailored to your skill level  
- **Intelligent Opponent** – Play against an AI that adapts to your strategies  
- **Custom Scenario Creation** – Use AI to generate new game setups for endless possibilities

## Technologies

[![Python][Python-img]][Python-url] <br>
[![React][React-img]][React-url] <br>
[![JavaScript][JavaScript-img]][JavaScript-url] <br>
[![HTML][HTML-img]][HTML-url] <br>

## 🔧 Installation

### Prerequisites

You need to have installed:
- Node.js
- Python (preferred version 3.12 or higher)
- pip
- Rust

### Backend Setup

1. Clone the repository:
```sh
git clone https://github.com/theol-tuc/TTGD.git
```
2. Navigate to the backend folder and start the virtual environment:
```sh
.venv\Scripts\activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
4. Start the backend server:
```sh
python -m uvicorn api:app --reload
```
The backend server is now running on `http://localhost:8000`

### Frontend Setup

1. Navigate to the "TTG_Frontend/app" folder and install dependencies
```sh
npm install
```
2. In the same directory run:
```sh
npm start
```
The Frontend and backend are now running on `http://localhost:3000`

You can now play the game!

## AI Usage

If you want to use the AI features, at this moment they are in the respective branches with their name.

For the usage on LLaMa3 go to the branch [llama3](llama3). For instructions read the implentation guide [IMPLEMENTATION_GUIDE.md](TTG_Backend/IMPLEMENTATION_GUIDE.md).

For the usage on GPT-4V go to the branch [gpt4](gpt4).

For the usage of VILA go to the branch [VLM_VILA](VLM_VILA).

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


<!-- MARKDOWN LINKS & IMAGES -->
[Python-img]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[React-img]: https://shields.io/badge/react-black?logo=react&style=for-the-badge
[React-url]: https://www.react.dev/
[JavaScript-img]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[HTML-img]: https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
