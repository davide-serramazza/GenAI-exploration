"""
Model Wrapper.

This class encapsulates the Qwen LLM. It handles model loading,
quantization, and text generation. By wrapping it in a class, we
ensure the model is only loaded into VRAM once and can be reused
across different scripts without global variables.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

class QwenChat:

    def __init__(self, model_path: str, device: str):
        self.model_path = model_path
        self.device = device

        # 4-bit quantization config to fit the model on a small GPU (like a 4GB laptop)
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_quant_type="nf4",
        )

        print(f"Loading model from {self.model_path} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            quantization_config=self.bnb_config,
            device_map=self.device,
        )
        self.model.eval() # Set model to evaluation mode (disables dropout)
        print("Model loaded successfully.")

    def generate_response(self, messages: list, max_new_tokens: int = 512) -> str:
        """
        Takes a list of message dicts [{'role': 'user', 'content': '...'}]
        and returns the model's text response.
        """
        # Apply the specific chat template Qwen expects (e.g., <|im_start|>)
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        # torch.no_grad() saves memory and speeds up inference by not tracking gradients
        with torch.no_grad():
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens
            )

        # Slice off the input tokens to only decode the newly generated text
        generated_ids = [
            output_ids[len(input_ids):]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    def chat_loop(self):
        """For manual testing in the terminal"""
        messages = []
        print("Type 'quit' or 'exit' to stop.")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            messages.append({"role": "user", "content": user_input})
            response = self.generate_response(messages)
            messages.append({"role": "assistant", "content": response})
            print(f"\nQwen: {response}")