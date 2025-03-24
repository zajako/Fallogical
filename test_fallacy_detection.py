import os
import sys
import ollama
from dotenv import load_dotenv
from fallacy_detector import FallacyDetector
from voice_interrupter import VoiceInterrupter

load_dotenv()

def main():
    # Default to llama3.2 model, but allow command-line override
    model_name = sys.argv[1] if len(sys.argv) > 1 else "llama3.2"
    
    # Initialize components
    detector = FallacyDetector(model_name=model_name)
    interrupter = VoiceInterrupter()
    
    # Test examples with common logical fallacies
    examples = [
        "Everyone is using this product, so it must be good.",
        "You can either support this policy or you hate your country.",
        "Your argument can't be valid because you're too young to understand this topic.",
        "If we allow gay marriage, next people will want to marry their pets.",
        "The CEO says this product is revolutionary, so it must be true.",
        "This medicine was used in ancient times, so it must be effective.",
        "He won the lottery after wearing his lucky socks, so the socks must have brought him luck.",
        "No one has proven that ghosts don't exist, so they must be real."
    ]
    
    print(f"Testing fallacy detection using Ollama model: {model_name}\n")
    
    # Check if Ollama is running and the model is available
    try:
        print("Checking Ollama availability...")
        models = ollama.list()
        model_names = [model['name'].split(':')[0] for model in models['models']]
        
        if model_name not in model_names:
            closest_match = next((m for m in model_names if model_name in m), None)
            if closest_match:
                print(f"Model '{model_name}' not found exactly, using '{closest_match}' instead.")
                model_name = closest_match
                detector.model_name = closest_match
            else:
                print(f"Warning: Model '{model_name}' not found. Available models:")
                for model in model_names:
                    print(f"  - {model}")
                print(f"Proceeding with '{model_name}' anyway. If it fails, try using one of the above models.")
    except Exception as e:
        print(f"Warning: Could not connect to Ollama: {e}")
        print("Make sure Ollama is running on your system.")
        return
    
    # Test each example
    for i, example in enumerate(examples):
        print(f"\nExample {i+1}: \"{example}\"")
        print("Analyzing...")
        
        result = detector.analyze_text(example)
        
        if result:
            print(f"Fallacy detected: {result['fallacy'].title()}")
            print(f"Explanation: {result['explanation']}")
            print(f"Example: {result['example']}")
            
            # Uncomment to test speech output
            # interrupter.interrupt(f"Fallacy detected: {result['fallacy'].title()}. {result['explanation']}. Example: {result['example']}")
        else:
            print("No fallacy detected.")
        
        print("-" * 50)

if __name__ == "__main__":
    main() 