import ollama
from typing import List, Dict, Any, Optional
import json
import logging
import re
import asyncio
from pathlib import Path
from functools import partial
from tools.search_web_serp import search_web_serp
from tools.get_page_content import get_page_content
from tools.extract_vocabulary import extract_vocabulary
from tools.generate_song_id import generate_song_id
from tools.save_results import save_results
import math

# Get the app's root logger
logger = logging.getLogger('song_vocab')

class ToolRegistry:
    def __init__(self, lyrics_path: Path, vocabulary_path: Path):
        self.lyrics_path = lyrics_path
        self.vocabulary_path = vocabulary_path
        self.tools = {
            'search_web_serp': search_web_serp,
            'get_page_content': get_page_content,
            'extract_vocabulary': extract_vocabulary,
            'generate_song_id': generate_song_id,
            'save_results': partial(save_results, lyrics_path=lyrics_path, vocabulary_path=vocabulary_path)
        }
    
    def get_tool(self, name: str):
        return self.tools.get(name)

def calculate_safe_context_window(available_ram_gb: float, safety_factor: float = 0.8) -> int:
    """
    Calculate a safe context window size based on available RAM.
    
    Args:
        available_ram_gb (float): Available RAM in gigabytes
        safety_factor (float): Factor to multiply by for safety margin (default 0.8)
        
    Returns:
        int: Recommended context window size in tokens
        
    Note:
        Based on observation that 128K tokens requires ~58GB RAM
        Ratio is approximately 0.45MB per token (58GB/131072 tokens)
    """
    # Known ratio from our testing
    GB_PER_128K_TOKENS = 58.0
    TOKENS_128K = 131072
    
    # Calculate tokens per GB
    tokens_per_gb = TOKENS_128K / GB_PER_128K_TOKENS
    
    # Calculate safe token count
    safe_tokens = math.floor(available_ram_gb * tokens_per_gb * safety_factor)
    
    # Round down to nearest power of 2 for good measure
    power_of_2 = 2 ** math.floor(math.log2(safe_tokens))
    
    # Cap at 128K tokens
    final_tokens = min(power_of_2, TOKENS_128K)
    
    logger.debug(f"Context window calculation:")
    logger.debug(f"  Available RAM: {available_ram_gb}GB")
    logger.debug(f"  Tokens per GB: {tokens_per_gb}")
    logger.debug(f"  Raw safe tokens: {safe_tokens}")
    logger.debug(f"  Power of 2: {power_of_2}")
    logger.debug(f"  Final tokens: {final_tokens}")
    
    return final_tokens

class SongLyricsAgent:
    def __init__(self, stream_llm=True, available_ram_gb=32):
        logger.info("Initializing SongLyricsAgent")
        self.base_path = Path(__file__).parent
        self.prompt_path = self.base_path / "prompts" / "Lyrics-Angent.md"
        self.lyrics_path = self.base_path / "outputs" / "lyrics"
        self.vocabulary_path = self.base_path / "outputs" / "vocabulary"
        self.stream_llm = stream_llm
        self.context_window = calculate_safe_context_window(available_ram_gb)
        logger.info(f"Calculated safe context window size: {self.context_window} tokens for {available_ram_gb}GB RAM")
        
        # Create output directories
        self.lyrics_path.mkdir(parents=True, exist_ok=True)
        self.vocabulary_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directories created: {self.lyrics_path}, {self.vocabulary_path}")
        
        # Initialize Ollama client and tool registry
        logger.info("Initializing Ollama client and tool registry")
        try:
            self.client = ollama.Client()
            self.tools = ToolRegistry(self.lyrics_path, self.vocabulary_path)
            logger.info("Initialization successful")
        except Exception as e:
            logger.error(f"Failed to initialize: {e}")
            raise
    
    def parse_llm_action(self, content: str) -> Optional[tuple[str, Dict[str, Any]]]:
        """Parse the LLM's response to extract tool name and arguments."""
        # Look for tool calls in the format: Tool: tool_name(arg1="value1", arg2="value2")
        match = re.search(r'Tool:\s*(\w+)\((.*?)\)', content)
        if not match:
            return None
        
        tool_name = match.group(1)
        args_str = match.group(2)
        
        # Parse arguments
        args = {}
        for arg_match in re.finditer(r'(\w+)="([^"]*?)"', args_str):
            args[arg_match.group(1)] = arg_match.group(2)
        
        return tool_name, args
    
    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Execute a tool with the given arguments."""
        tool = self.tools.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool Unknown: {tool_name}")
        
        logger.info(f"Tool Execute: {tool_name} with args: {args}")
        try:
            result = await tool(**args) if asyncio.iscoroutinefunction(tool) else tool(**args)
            logger.info(f"Tool Succeeded: {tool_name}")
            return result
        except Exception as e:
            logger.error(f"Tool Failed: {tool_name} - {e}")
            raise

    def _get_llm_response(self, conversation):
        """Get response from LLM with optional streaming.
        
        Args:
            conversation (list): List of conversation messages
            
        Returns:
            dict: Response object with 'content' key
        """
        if self.stream_llm:
            # Stream response and collect tokens
            full_response = ""
            logger.info("Streaming tokens:")
            for chunk in self.client.chat(
                model="llama3.2:3b",
                messages=conversation,
                stream=True
            ):
                content = chunk.get('message', {}).get('content', '')
                if content:
                    logger.info(f"Token: {content}")
                    full_response += content
            
            # Create response object similar to non-streaming format
            return {'content': full_response}
        else:
            # Non-streaming response
            try:
                response = self.client.chat(
                    model="llama3.2:3b",
                    messages=conversation,
                    options={
                        "num_ctx": self.context_window
                    }
                )
                # Log context window usage
                prompt_tokens = response.get('prompt_eval_count', 0)
                total_tokens = prompt_tokens + response.get('eval_count', 0)
                logger.info(f"Context window usage: {prompt_tokens}/{2048} tokens (prompt), {total_tokens} total tokens")
                
                logger.info(f"  Message ({response['message']['role']}): {response['message']['content'][:300]}...")
                return response
            except Exception as e:
                logger.error(f"LLM response error: {e}")
                # Return a minimal response to prevent crashes
                return {'message': {'role': 'assistant', 'content': 'Error: Context too large. Please try with less context.'}}
    
    async def process_request(self, message: str) -> str:
        """Process a user request using the ReAct framework."""
        logger.info("-"*20)
        
        # Initialize conversation with system prompt and user message
        conversation = [
            {"role": "system", "content": self.prompt_path.read_text()},
            {"role": "user", "content": message}
        ]
        
        max_turns = 10
        current_turn = 0
        
        while current_turn < max_turns:
            try:
                logger.info(f"[Turn {current_turn + 1}/{max_turns}]")
                try:
                    # Log the request payload
                    logger.info(f"Request:")
                    for msg in conversation[-2:]:  # Show last 2 messages for context
                        logger.info(f"  Message ({msg['role']}): {msg['content'][:300]}...")

                    response = self._get_llm_response(conversation)

                    #breakpoint()
                    
                    if not isinstance(response, dict) or 'message' not in response or 'content' not in response['message']:
                        raise ValueError(f"Unexpected response format from LLM: {response}")
                    
                    # Extract content from the message
                    content = response.get('message', {}).get('content', '')
                    if not content or not content.strip():
                        breakpoint()
                        logger.warning("Received empty response from LLM")
                        conversation.append({"role": "system", "content": "Your last response was empty. Please process the previous result and specify the next tool to use, or indicate FINISHED if done."})
                        continue

                    response = {'content': content}
                    
                    # Parse the action
                    action = self.parse_llm_action(response['content'])
                    
                    if not action:
                        if 'FINISHED' in response['content']:
                            logger.info("LLM indicated task is complete")
                            return response['content']
                        else:
                            logger.warning("No tool call found in LLM response")
                            conversation.append({"role": "system", "content": "Please specify a tool to use or indicate FINISHED if done."})
                            continue
                except Exception as e:
                    logger.error(f"Error getting LLM response: {e}")
                    logger.debug("Last conversation state:", exc_info=True)
                    for msg in conversation[-2:]:
                        logger.debug(f"Message ({msg['role']}): {msg['content']}")
                    raise
                
                # Execute the tool
                tool_name, tool_args = action
                logger.info(f"Executing tool: {tool_name}")
                logger.info(f"Arguments: {tool_args}")
                result = await self.execute_tool(tool_name, tool_args)
                logger.info(f"Tool execution complete")
                
                # Add the interaction to conversation
                conversation.extend([
                    {"role": "assistant", "content": response['content']},
                    {"role": "system", "content": f"Tool {tool_name} result: {json.dumps(result)}"}
                ])
                
                current_turn += 1
                
            except Exception as e:
                logger.error(f"❌ Error in turn {current_turn + 1}: {e}")
                logger.error(f"Stack trace:", exc_info=True)
                conversation.append({"role": "system", "content": f"Error: {str(e)}. Please try a different approach."})
        
        raise Exception("Reached maximum number of turns without completing the task")
        raise Exception("Failed to get results within maximum turns")
