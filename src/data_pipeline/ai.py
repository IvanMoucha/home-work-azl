from functools import cached_property

import torch
import os
from transformers import PreTrainedTokenizerFast, LlamaForCausalLM, pipeline

import src.utils.logger as logger
from src.utils import config

log = logger.get_logger(__name__)

class AI:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AI, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True

    @cached_property
    def generator(self):
        local_model_path = os.path.join(os.path.dirname(__file__), "../../llm")
        local_model_path_file = os.path.join(os.path.dirname(__file__), "../../llm/model.safetensors")

        log.debug("Torch version: %s", torch.__version__)  # Check PyTorch version
        log.debug("Apple Silicon MPS support: %s", torch.backends.mps.is_available())  # Should return True if MPS
        log.info(f"Loading model: {config.LLM_MODEL}")

        # Check if MPS is available and move the model to MPS
        device_model = "cpu"
        if torch.cuda.is_available():
            device_model = "cuda"
        # FixMe: MPS seams to be broken on Apple Silicon in this version and newer is not available
        # elif torch.backends.mps.is_available():
            # device_model = "mps"

        log.info(f"Device model: {device_model}")

        device = torch.device(device_model)

        # Check if the local model exists
        if os.path.exists(local_model_path_file):
            log.info(f"Loading local model from {local_model_path}")
            tokenizer = PreTrainedTokenizerFast.from_pretrained(local_model_path, local_files_only=True)
            model = LlamaForCausalLM.from_pretrained(local_model_path, local_files_only=True)
        else:
            log.info(f"Downloading model from Hugging Face: {config.LLM_MODEL}")
            tokenizer = PreTrainedTokenizerFast.from_pretrained(config.LLM_MODEL)
            model = LlamaForCausalLM.from_pretrained(config.LLM_MODEL)

        model.to(device)

        log.debug("Model loaded")

        return pipeline(task="text-generation", model=model, device=device, tokenizer=tokenizer, torch_dtype=torch.bfloat16)

    def generate_tldr(self, text: str) -> str:
        if text is None:
            return None

        log.debug(f"Generating TLDR")

        prompt = [
            {"role": "system", "content": "You are an expert on all subject matters. Keep responses unique and free of repetition. When reasoning, perform step-by-step thinking before you answer the question. Always focus on the key points in my questions to determine my intent. Provide short answers that are clear and concise."},
            {"role": "user", "content": text},
        ]

        generation = self.generator(
            prompt,
            do_sample=False,
            temperature=1.0,
            top_p=1,
            max_new_tokens=512
        )

        # Extract only the assistant's content
        assistant_content = next(item['content'] for item in generation[0]['generated_text'] if item['role'] == 'assistant')

        log.debug(f"TLDR length: {len(assistant_content)}")

        return assistant_content

