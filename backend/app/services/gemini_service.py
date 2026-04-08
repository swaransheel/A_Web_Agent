"""
Gemini service - integrates with Google Generative AI API for text generation.
"""

import re
import google.generativeai as genai
from typing import Optional
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiService:
    """Service for AI text generation via Google Gemini."""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        self.temperature = Config.GEMINI_TEMPERATURE
        self.max_tokens = Config.GEMINI_MAX_TOKENS
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Try to load the model, fall back to text-bison-001 if not available
        try:
            self.model = genai.GenerativeModel(self.model_name)
        except Exception as e:
            logger.warning(f"Could not load model {self.model_name}, trying fallback: {e}")
            self.model_name = "models/text-bison-001"
            self.model = genai.GenerativeModel(self.model_name)
    
    def generate_answer(self, query: str, context: str) -> str:
        """
        Generate answer using Gemini based on query and context.
        
        Args:
            query: User's search query
            context: Context from web search results
        
        Returns:
            Generated answer string
        
        Raises:
            Exception: If generation fails
        """
        logger.info("Generating answer with Gemini")
        
        # Build prompt with security considerations
        prompt = self._build_prompt(query, context)
        
        try:
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            # Check for safety filters
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                logger.warning(f"Response blocked: {response.prompt_feedback.block_reason}")
                raise Exception("Could not generate response due to content policy")
            
            # Extract text
            if not response.text:
                logger.warning("Empty response from Gemini")
                raise Exception("No response generated")
            
            answer = response.text.strip()
            logger.info(f"Answer generated: {len(answer)} characters")
            return answer
        
        except Exception as e:
            logger.error(f"Gemini generation error: {str(e)}")
            # Fallback: synthesize answer from context
            logger.info("Falling back to context-based answer synthesis")
            return self._synthesize_answer_from_context(context)
    
    def _synthesize_answer_from_context(self, context: str) -> str:
        """
        Fallback method: synthesize an answer directly from the context
        when LLM API is unavailable.
        
        Args:
            context: The context from search results
        
        Returns:
            Synthesized answer
        """
        if not context or not context.strip():
            return "Unable to generate answer. Please try again."
        
        # Parse context into source sections
        # Format: [Source X]\nTitle: ...\nContent: ...\nURL: ...
        sources = []
        current_source = {"title": "", "content": ""}
        
        for line in context.split('\n'):
            line_stripped = line.strip()
            
            # Check for source marker
            if line_stripped.startswith('[Source'):
                if current_source["content"]:
                    sources.append(current_source)
                current_source = {"title": "", "content": ""}
            elif line_stripped.startswith('Title:'):
                current_source["title"] = line_stripped.replace('Title:', '', 1).strip()
            elif line_stripped.startswith('Content:'):
                current_source["content"] = line_stripped.replace('Content:', '', 1).strip()
        
        # Add last source if it has content
        if current_source["content"]:
            sources.append(current_source)
        
        # Build coherent answer from sources
        if not sources:
            return "No relevant information found in search results."
        
        # Extract and combine key sentences from multiple sources
        answer_parts = []
        for source_idx, source in enumerate(sources[:5]):  # Use up to 5 sources
            if source["content"]:
                # Clean up content first
                clean_content = self._clean_content(source["content"])
                
                # Split into sentences more carefully
                # Split on periods, question marks, exclamation marks
                raw_sentences = re.split(r'[.!?]+', clean_content)
                
                # Filter for quality sentences
                sentences = []
                for sentence in raw_sentences:
                    s = sentence.strip()
                    
                    # Skip if too short
                    if len(s) < 25:
                        continue
                    
                    # Skip if has table dividers or too many dashes
                    if '---' in s or s.count('-') > 3:
                        continue
                    
                    # Skip if has too many special characters (likely garbage)
                    special_chars = '*|,;:()[]{}@#$%^&'
                    special_count = sum(1 for c in s if c in special_chars)
                    if special_count > 3:
                        continue
                    
                    # Skip if mostly numbers/entities (like table data)
                    digit_ratio = sum(1 for c in s if c.isdigit()) / max(1, len(s))
                    if digit_ratio > 0.25:
                        continue
                    
                    # Skip if has too many commas (likely a list/table)
                    if s.count(',') > 4:
                        continue
                    
                    # Skip common navigation/header patterns
                    skip_patterns = [
                        'toggle', 'subsection', 'click', 'read', 'visit',
                        'about', 'contact', 'privacy', 'terms', 'back', 'next',
                        'home', 'search', 'login', 'sign up', 'menu', 'standings',
                        'schedule', 'birthdate', 'born', 'age', 'height', 'weight'
                    ]
                    if any(pattern in s.lower()[:50] for pattern in skip_patterns):
                        continue
                    
                    # Skip if starts with special character or non-word character
                    if s and (s[0] in "'\"*|[({-— " or s[0].isdigit()):
                        continue
                    
                    # Must start with capital letter, common starting words, or article
                    valid_start = (s[0].isupper() or 
                                 s.lower().startswith(('the ', 'this ', 'that ', 'these ', 'those ', 'a ', 'an ')))
                    if not valid_start:
                        continue
                    
                    # Skip if contains weird encoding patterns
                    if any(pattern in s for pattern in ['â€', 'Â', '€20', 'Â«', 'Â»']):
                        continue
                    
                    sentences.append(s)
                
                # Add first good sentence from this source
                if sentences:
                    best_sentence = sentences[0] + '.'
                    
                    # Skip if result would be just name/title data
                    if len(best_sentence.split()) < 5:
                        continue
                    
                    # Avoid duplicates
                    if best_sentence not in answer_parts:
                        answer_parts.append(best_sentence)
        
        if answer_parts and len(answer_parts) > 0:
            # Join parts with proper spacing
            answer = ' '.join(answer_parts)
            
            # Final validation - make sure we have a reasonable answer
            if len(answer) > 40 and len(answer.split()) >= 8:
                return answer
        
        return "Unable to generate answer. Please try again."
    
    def _clean_content(self, text: str) -> str:
        """
        Clean up HTML/markdown artifacts and formatting issues from text.
        
        Args:
            text: Text to clean
        
        Returns:
            Cleaned text
        """
        # Remove table formatting (lines with pipes)
        text = re.sub(r'\|.*?\|', '', text)
        
        # Remove markdown image syntax
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Remove HTML tags and entities
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'&[a-z]+;', ' ', text)
        
        # Remove markdown link syntax, keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # Remove markdown formatting markers
        text = text.replace('**', '').replace('__', '').replace('`', '')
        text = text.replace('~~', '')  # Strikethrough
        
        # Remove markdown headers
        text = re.sub(r'#+\s+', '', text)
        
        # Remove markdown dividers (---, ***, etc)
        text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
        
        # Remove toggle/subsection text (like "Toggle History subsection")
        text = re.sub(r'Toggle\s+\w+\s+subsection', '', text, flags=re.IGNORECASE)
        
        # Remove navigation patterns with asterisks or numbers
        text = re.sub(r'\*\s*\d+\s+\w+', '', text)  # * 1 History, * 2 Career
        text = re.sub(r'^\*\s+.*?(?=\n|$)', '', text, flags=re.MULTILINE)
        
        # Remove currency symbols and encoding artifacts
        text = text.replace('Â', '').replace('·', ':')
        text = re.sub(r'â.*?20', '', text)  # Remove encoding like â¬20
        text = re.sub(r'Â«|Â»', '"', text)  # Replace smart quotes
        text = re.sub(r'€|¥|£|¢', '$', text)  # Normalize currency to $
        
        # Remove lines that look like incomplete data or fragments
        text = re.sub(r"^'.{1,20}$", '', text, flags=re.MULTILINE)
        text = re.sub(r'^\d+.*\d+-\d+.*\d+', '', text, flags=re.MULTILINE)  # Date ranges
        
        # Remove birthdates and age patterns
        text = re.sub(r'(born|age|birthdate)\s+\d+', '', text, flags=re.IGNORECASE)
        
        # Clean up whitespace
        text = text.replace('\n', ' ')
        text = text.replace('  ', ' ')
        
        # Remove malformed patterns
        text = re.sub(r'\s*\(\s*\)', '', text)
        text = re.sub(r'\[\s*\]\([^\)]*\)', '', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _build_prompt(self, query: str, context: str) -> str:
        """
        Build the prompt for Gemini with security constraints.
        
        Args:
            query: User query
            context: Search context
        
        Returns:
            Formatted prompt
        """
        prompt = f"""You are a factual AI assistant. Your task is to answer the user's question based ONLY on the provided context.

IMPORTANT RULES:
1. Use ONLY the information from the provided context
2. Do NOT add information not in the context
3. Do NOT hallucinate or invent facts
4. If the context doesn't contain enough information to answer, say "I don't have enough information in the provided sources to answer this question."
5. Always be accurate and truthful
6. Provide a clear, concise answer

Context from web search:
{context}

Question: {query}

Instructions:
- Give a clear, concise answer (2-3 sentences max)
- List the relevant sources at the end if applicable
- If multiple sources are used, list them as: Sources: [Source 1], [Source 2], etc.
- Maintain factual accuracy

Answer:"""
        
        return prompt
    
    def validate_response(self, response_text: str) -> bool:
        """
        Validate response quality.
        
        Args:
            response_text: Generated response
        
        Returns:
            True if response is valid
        """
        # Check minimum length
        if len(response_text.strip()) < 10:
            logger.warning("Response too short")
            return False
        
        # Check for common failure indicators
        fail_indicators = [
            "I cannot",
            "I'm not able",
            "I don't have enough",
            "Insufficient data"
        ]
        
        if any(indicator.lower() in response_text.lower() for indicator in fail_indicators):
            logger.info("Response indicates insufficient context")
            return True  # Still valid, just indicates lack of context
        
        return True
