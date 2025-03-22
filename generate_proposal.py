import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_proposal(job_description, client_name, my_name, my_expertise=None, portfolio_links=None):
    """
    Generate an Upwork job proposal using the Groq API with Llama 3.2
    
    Args:
        job_description: The job posting description
        client_name: The name of the potential client
        my_name: Your name
        my_expertise: Your expertise (optional)
        portfolio_links: List of your portfolio links (optional)
    
    Returns:
        Generated proposal text
    """
    # Default values if not provided
    my_expertise = my_expertise or "WordPress Development, SEO, and Website Optimization"
    portfolio_links = portfolio_links or [
        "https://example.com/portfolio1",
        "https://example.com/portfolio2",
        "https://example.com/portfolio3"
    ]
    
    # Format portfolio links as a string
    portfolio_str = "\n".join(portfolio_links)
    
    # Create prompt for the model
    prompt = f"""
    Write a personalized Upwork proposal for the following job description:
    
    "{job_description}"
    
    The client's name is {client_name}.
    My name is {my_name}.
    My expertise includes {my_expertise}.
    
    My portfolio includes:
    {portfolio_str}
    
    Follow these IMPORTANT guidelines for the proposal:
    1. Start with a greeting using the client's name (if no name is provided, use a generic greeting)
    2. The second line should be a compelling hook that directly addresses the client's problem with a solution
    3. Keep the language simple, straightforward and easy to understand
    4. Include ONE small paragraph about a recent relevant experience or case study
    5. Include specific figures and statistics that demonstrate your success (e.g., "increased conversions by 45%")
    6. End with a soft call-to-action (not pushy but encouraging next steps)
    7. Keep the entire proposal under 250 words and make it conversational but professional
    8. Highlight your expertise relevant to the job without using overly enthusiastic phrases like "I'm excited"
    9. Keep paragraphs short and scannable
    10. Include the portfolio links naturally in the text
    11. Maintain a professional tone throughout - no exclamation marks or overly casual language
    12. Focus on the value you can provide rather than emotions or excitement
    
    The proposal should be easy to read, impactful, professional, and focus on solving the client's problem.
    """
    
    # Initialize Groq client
    api_key = "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"
    client = Groq(api_key=api_key)
    
    # Generate completion
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "system", "content": "You are an expert at writing compelling job proposals for freelancers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_completion_tokens=1000,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    # Return the generated proposal
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("Upwork Proposal Generator using Llama 3.2")
    print("------------------------------------------")
    
    # Get user inputs
    job_description = input("Enter the job description: ")
    client_name = input("Enter the client's name: ")
    my_name = input("Enter your name: ")
    
    # Optional inputs
    expertise_input = input("Enter your expertise (press Enter to use default): ")
    my_expertise = expertise_input if expertise_input else None
    
    # Portfolio links
    portfolio_links = []
    print("Enter your portfolio links (one per line, press Enter on an empty line to finish):")
    while True:
        link = input()
        if not link:
            break
        portfolio_links.append(link)
    
    # Generate the proposal
    proposal = generate_proposal(
        job_description=job_description,
        client_name=client_name,
        my_name=my_name,
        my_expertise=my_expertise if expertise_input else None,
        portfolio_links=portfolio_links if portfolio_links else None
    )
    
    # Print the generated proposal
    print("\n--- Generated Proposal ---\n")
    print(proposal)
    print("\n-------------------------") 