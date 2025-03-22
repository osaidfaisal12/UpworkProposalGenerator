import streamlit as st
import os
from generate_proposal import generate_proposal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Upwork Proposal Generator",
    page_icon="💼",
    layout="wide"
)

# App title and description
st.title("Upwork Proposal Generator")
st.markdown("Generate personalized Upwork proposals using Llama 3.2 via Groq API")

# Sidebar with guidelines
with st.sidebar:
    st.subheader("Proposal Guidelines")
    st.markdown("""
    Your proposal will follow these important guidelines:
    
    1. Start with client's name greeting
    2. Compelling hook addressing the problem
    3. Simple, straightforward language
    4. Include relevant experience with stats
    5. Include specific figures/percentages
    6. End with soft call-to-action
    7. Under 250 words, professional tone
    8. No "excited" or overly enthusiastic language
    9. Short, scannable paragraphs
    10. Portfolio links included naturally
    11. Value-focused, not emotion-focused
    """)

# Create a two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    # Input fields
    st.subheader("Input Parameters")
    
    # Job description input as a text area
    job_description = st.text_area(
        "Job Description", 
        placeholder="Enter the full job posting description here...",
        height=200
    )
    
    # Client and your name as text inputs
    client_name = st.text_input("Client's Name", placeholder="Enter client's name")
    my_name = st.text_input("Your Name", placeholder="Enter your name")
    
    # Expertise with default option
    default_expertise = "WordPress Development, SEO, and Website Optimization"
    my_expertise = st.text_input(
        "Your Expertise", 
        placeholder=f"Default: {default_expertise}",
        help=f"Leave blank to use default: {default_expertise}"
    )
    
    # Portfolio links as a text area
    portfolio_links_text = st.text_area(
        "Portfolio Links",
        placeholder="Enter your portfolio links, one per line",
        height=100,
        help="Leave blank to use default portfolio links"
    )
    
    # Parse portfolio links
    portfolio_links = [link.strip() for link in portfolio_links_text.split('\n') if link.strip()] if portfolio_links_text else None
    
    # Generate button
    generate_button = st.button("Generate Proposal", type="primary")

with col2:
    # Output section
    st.subheader("Generated Proposal")
    
    if generate_button:
        if not job_description or not client_name or not my_name:
            st.error("Please fill in all required fields: Job Description, Client's Name, and Your Name")
        else:
            # Show loading spinner while generating
            with st.spinner("Generating proposal..."):
                try:
                    # Generate the proposal
                    proposal = generate_proposal(
                        job_description=job_description,
                        client_name=client_name,
                        my_name=my_name,
                        my_expertise=my_expertise if my_expertise else None,
                        portfolio_links=portfolio_links
                    )
                    
                    # Display the proposal
                    st.success("Proposal generated successfully!")
                    st.text_area("Your Proposal", proposal, height=400, disabled=True)
                    
                    # Copy button
                    st.download_button(
                        label="Download Proposal as Text",
                        data=proposal,
                        file_name="upwork_proposal.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating proposal: {str(e)}")
                    if "GROQ_API_KEY" not in os.environ:
                        st.error("GROQ_API_KEY not found. Please make sure you have a .env file with your API key.")
    else:
        st.info("Fill in the fields and click 'Generate Proposal' to create your Upwork proposal.")
        
# Footer
st.markdown("---")
st.markdown("Powered by Groq API with Llama 3.2 model") 