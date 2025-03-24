import os
import ollama
from dotenv import load_dotenv

load_dotenv()

class FallacyDetector:
    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name
        
        # Define common logical fallacies and their descriptions
        self.fallacies = {
            "ad hominem": "Attacking the person instead of addressing their argument",
            "straw man": "Misrepresenting someone's argument to make it easier to attack",
            "appeal to authority": "Using an authority figure's opinion as evidence in an argument",
            "appeal to emotion": "Manipulating emotions instead of using valid reasoning",
            "false dilemma": "Presenting only two options when others exist",
            "slippery slope": "Arguing that a small step will inevitably lead to extreme consequences",
            "circular reasoning": "Making an argument where the conclusion is included in the premise",
            "hasty generalization": "Drawing a conclusion based on insufficient or unrepresentative evidence",
            "red herring": "Introducing an irrelevant topic to divert attention from the original issue",
            "appeal to ignorance": "Claiming something is true because it hasn't been proven false (or vice versa)",
            "bandwagon fallacy": "Appealing to popularity or the fact that many people do something as validation",
            "tu quoque": "Avoiding criticism by turning it back on the accuser",
            "post hoc fallacy": "Assuming that because B followed A, A must have caused B",
            "genetic fallacy": "Judging something based on its origin rather than its current meaning or context",
            "no true scotsman": "Making an appeal to purity as a way to dismiss relevant criticisms",
        }
        
    def analyze_text(self, text):
        """
        Analyze text for logical fallacies
        
        Args:
            text: Text to analyze
            
        Returns:
            A dictionary containing fallacy information if found, None otherwise
            Format: {'fallacy': fallacy_name, 'explanation': explanation, 'example': example_from_text}
        """
        if not text or not text.strip():
            return None
            
        # Create system prompt for the detection
        system_prompt = """You are an expert in identifying logical fallacies in conversations. 
Analyze the provided text and identify if it contains any logical fallacies.
If a fallacy is detected, identify its type, explain why it's a fallacy, and quote the exact text that contains the fallacy.
If multiple fallacies are present, identify the most prominent one.
If no fallacy is detected, respond with "No fallacy detected."
Be very strict and precise - only report actual fallacies with high confidence."""

        # Define user prompt
        user_prompt = f"Analyze this text for logical fallacies: '{text}'"
        
        try:
            # Using Ollama for the analysis
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            analysis = response['message']['content']
            
            # Check if a fallacy was detected
            if "No fallacy detected" in analysis:
                return None
                
            # Parse the response to extract fallacy details
            for fallacy_name in self.fallacies.keys():
                if fallacy_name.lower() in analysis.lower():
                    # Extract the example from the analysis
                    # Assuming the example is quoted in the analysis
                    example = ""
                    lines = analysis.split("\n")
                    for line in lines:
                        if '"' in line or "'" in line:
                            # Extract text between quotes
                            start = line.find('"') if '"' in line else line.find("'")
                            end = line.rfind('"') if '"' in line else line.rfind("'")
                            if start != -1 and end != -1 and end > start:
                                example = line[start+1:end]
                                break
                    
                    return {
                        'fallacy': fallacy_name,
                        'explanation': self.fallacies[fallacy_name],
                        'example': example or "Not specified",
                        'full_analysis': analysis
                    }
            
            # If we couldn't match a specific fallacy but the analysis says there is one
            return {
                'fallacy': "Unknown fallacy",
                'explanation': "A logical fallacy was detected but could not be classified.",
                'example': text,
                'full_analysis': analysis
            }
            
        except Exception as e:
            print(f"Error analyzing text for fallacies: {e}")
            return None 