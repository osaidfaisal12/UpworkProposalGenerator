import os
from groq import Groq
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

def clean_response(response):
    """
    Clean up the response from the model by removing <think> tags
    
    Args:
        response: The raw response from the model
    
    Returns:
        Cleaned response text
    """
    # Remove <think> tags if present
    cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    
    # If the cleaning removed everything, return the original
    if not cleaned.strip() and response.strip():
        # Extract content from within <think> tags
        think_content = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
        if think_content:
            return think_content.group(1).strip()
    
    return cleaned.strip() or response

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
    STRUCTURE:

    1. Start with a greeting using the client's name (if available) or a polite general greeting.  
    2. The second line must be a compelling hook that directly addresses the client's stated problem and presents a solution.  
    3. Keep the tone professional and conversational — no robotic or overly casual phrasing.  
    4. Use clear and simple language.  
    5. Add one short paragraph about a **recent, relevant** project or case study based on the job type.  
    6. Include specific numbers that highlight your success (e.g., "increased conversions by 45%").  
    7. End with a soft, non-pushy call-to-action (e.g., offer to discuss next steps).  
    8. Keep total length under 250 words.  
    9. Avoid phrases like "I'm excited", "passionate", or using exclamation marks.  
    10. Use short, readable paragraphs.

    ---

    DYNAMIC RULES BASED ON JOB TYPE:

    If the job involves GoHighLevel (GHL):
    - Only mention GHL-specific experience and terminology: automations, funnel, CRM, pipeline, snapshots, onboarding workflows.  
    - Mention that you're working with 4 of the fastest-growing startups using GHL as their backend.  
    - Include results like: "Generated 120+ high-converting leads in 10 days", or "Saved 10+ hours weekly by automating onboarding".  
    - Do not mention Webflow, WordPress, or other platforms.  
    - Include a GHL snapshot or relevant GHL portfolio link if applicable.

    ---

    If the job is for Webflow website or landing page:
    - Mention you're a Webflow Certified Developer and an official Webflow Partner.  
    - Focus on SEO-friendly structure, responsiveness, performance, clean CMS, scalable builds, and fast-loading pages.  
    - Highlight a stat like: “Helped a personal trainer generate 120+ leads in 10 days with a high-converting Webflow site”.  
    - Do not mention WordPress, GHL, or unrelated platforms.  
    - Embed Webflow portfolio links naturally.

    ---

    If the job is for WordPress:
    - Mention you have built 80+ WordPress websites and specialize in CMS flexibility, SEO structure, mobile responsiveness, and performance optimization.  
    - Mention examples like: “Reduced page load time by 60%” or “Increased session duration by 35%”.  
    - Do not mention Webflow or GHL unless the client mentions them.  
    - Include a relevant WordPress website portfolio link.

    ---

    If the job is CRO-focused (Conversion Rate Optimization):
    - Mention you have created 50+ high-converting websites for real estate, coaches, consultants, and online businesses.  
    - Emphasize keywords: user flow optimization, form improvement, heatmap testing, CTA redesign, mobile-first layout.  
    - Use results like:  
      - “Boosted form submissions by 40%”
      - “Increased checkout conversion rate by 48%”
      - “Reduced bounce rate by 32%”
    - Portfolio example (if available): “Heres a recent CRO-focused redesign: [insert link]”

    ---

    If the job is general web design without a specified platform:
    - Focus on strategy-driven design, UX, speed, mobile responsiveness, SEO, and results.  
    - Mention working with 50+ brands and measurable impacts like “increased form submissions by 40%”.  
    - Only include platforms if the client mentions one.

    ---

    PORTFOLIO LINK INSTRUCTIONS:
    Embed links naturally:  
    - “You can see a similar project here: [insert link]”  
    - “Heres a quick look at a related project I recently completed: [insert link]”

    ---

    EXPERIENCE TO INCLUDE (ONLY WHEN RELEVANT):
    - Webflow Certified Developer  
    - Official Webflow Partner  
    - Worked with 4 fastest-growing startups using GHL backend  
    - Working with 4x USA awarded Personal Trainers  
    - Built 80+ WordPress websites  
    - Created 50+ high-converting websites for real estate, coaches, and e-commerce businesses

    ---

    Always tailor the response based on the clients description and the platform or goal they mention.  
    Only include information, certifications, or achievements relevant to the job.  
    Keep the proposal short, value-focused, and always human in tone.

    DO NOT include any <think> tags or thinking steps in your response.

    The proposal should be easy to read, impactful, professional, and focus on solving the client's problem.
    """
    
    # Initialize Groq client
    api_key = "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"
    client = Groq(api_key=api_key)
    
    # Generate completion
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "system", "content": "You are an expert at writing compelling job proposals for freelancers. Do not use <think> tags in your responses."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_completion_tokens=1000,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    # Get the raw response
    raw_response = completion.choices[0].message.content
    
    # Clean the response to handle <think> tags
    cleaned_response = clean_response(raw_response)
    
    # Return the cleaned proposal
    return cleaned_response

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