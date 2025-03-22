# Upwork Proposal Generator

This application uses the Groq API with Llama 3.2 model to generate personalized job proposals for Upwork based on input parameters like job description, client name, and your details.

## Setup

1. Make sure you have Python 3.8+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Groq API key:
   ```
   GROQ_API_KEY="your_groq_api_key_here"
   ```

## Usage

You can use this application in two ways:

### Command Line Interface

Run the script using:

```
python generate_proposal.py
```

You'll be prompted to enter:
- The job description
- Client's name
- Your name
- Your expertise (optional, will use default if left empty)
- Your portfolio links (optional, will use default if none provided)

### Streamlit Web Interface

Run the Streamlit app for a user-friendly interface:

```
streamlit run app.py
```

The web interface provides:
- Input fields for all parameters
- Real-time proposal generation
- Option to download the generated proposal as a text file

## Example

Input:
- Job description: "I need help fixing my WordPress website. The menu is broken and some images aren't loading correctly."
- Client name: "John"
- Your name: "Sarah"

Output: A personalized proposal addressing the client's specific needs in a conversational tone with your details and portfolio links.

## Customization

You can modify the prompt template in the `generate_proposal` function to change how the AI generates proposals. 