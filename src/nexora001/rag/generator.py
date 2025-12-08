"""
Answer generation using Google Gemini AI.
"""

import os
from typing import Optional, Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AnswerGenerator:
    """
    Generates answers using Google Gemini AI.
    """
    
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_tokens: int = 1000
    ):
        """
        Initialize the answer generator.
        
        Args:
            model_name: Gemini model to use
            temperature: Creativity (0.0-1.0)
            max_tokens: Maximum response length
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set")
        
        genai.configure(api_key=api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
        )
        
        self.system_prompt = """You are Nexora001, an intelligent AI assistant that answers questions based on provided documentation. 

Your responsibilities:
1. Answer questions using ONLY the information from the provided context documents
2. If the answer is not in the context, say "I don't have enough information to answer that"
3. Cite sources by referencing document numbers like [Document 1]
4. Be concise but comprehensive
5. Use a friendly, professional tone

Remember: Only use information from the provided documents. Do not make up information."""
    
    def generate_answer(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate an answer based on query and context.
        
        Args:
            query: User's question
            context: Retrieved document context
            conversation_history: Previous conversation (optional)
            
        Returns:
            Generated answer
        """
        # Build prompt
        prompt = self._build_prompt(query, context, conversation_history)
        
        try:
            # Generate response
            response = self. model.generate_content(prompt)
            
            # Handle both simple and complex responses
            answer = ""
            try:
                # Try simple text access first
                answer = response.text. strip()
            except (ValueError, AttributeError):
                # Response is not simple text, extract from parts
                if hasattr(response, 'parts'):
                    for part in response.parts:
                        if hasattr(part, 'text'):
                            answer += part.text
                elif hasattr(response, 'candidates') and response.candidates:
                    # Fallback: extract from candidates
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            answer += part.text
                
                answer = answer.strip()
            
            return answer if answer else "I don't have enough information to answer that."
            
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def _build_prompt(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Build the complete prompt for the LLM.
        
        Args:
            query: User's question
            context: Retrieved documents
            conversation_history: Previous messages
            
        Returns:
            Complete prompt string
        """
        prompt_parts = [self.system_prompt, ""]
        
        # Add conversation history if available
        if conversation_history:
            prompt_parts.append("Previous conversation:")
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = msg. get('role', 'user')
                content = msg.get('content', '')
                prompt_parts.append(f"{role. title()}: {content}")
            prompt_parts.append("")
        
        # Add context documents
        if context:
            prompt_parts. append("Context Documents:")
            prompt_parts.append(context)
            prompt_parts.append("")
        
        # Add current query
        prompt_parts.append(f"User Question: {query}")
        prompt_parts.append("")
        prompt_parts.append("Your Answer:")
        
        return "\n".join(prompt_parts)
    
    def generate_streaming_answer(
        self,
        query: str,
        context: str,
        conversation_history: Optional[List[Dict]] = None
    ):
        """
        Generate answer with streaming (for real-time display).
        
        Args:
            query: User's question
            context: Retrieved documents
            conversation_history: Previous conversation
            
        Yields:
            Chunks of generated text
        """
        prompt = self._build_prompt(query, context, conversation_history)
        
        try:
            response = self.model.generate_content(prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            yield f"Error: {e}"