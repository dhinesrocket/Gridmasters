"""
Simple example demonstrating OpenAI API usage and token counting.
"""

from openai import OpenAI

# Initialize the OpenAI client
# Make sure to set your OPENAI_API_KEY environment variable
client = OpenAI()

def make_llm_call(prompt: str, model: str = "gpt-3.5-turbo"):
    """
    Make a call to OpenAI's API and return the response with token usage.
    
    Args:
        prompt: The user prompt to send
        model: The model to use (default: gpt-3.5-turbo)
    
    Returns:
        dict: Contains 'response' and 'usage' information
    """
    try:
        # Make the API call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the response text
        message = response.choices[0].message.content
        
        # Extract token usage information
        usage = response.usage
        
        return {
            "response": message,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
        }
    
    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"
    
    print("Making LLM call...")
    print(f"Prompt: {prompt}\n")
    
    result = make_llm_call(prompt)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Response: {result['response']}\n")
        print("Token Usage:")
        print(f"  - Prompt tokens: {result['usage']['prompt_tokens']}")
        print(f"  - Completion tokens: {result['usage']['completion_tokens']}")
        print(f"  - Total tokens: {result['usage']['total_tokens']}")
