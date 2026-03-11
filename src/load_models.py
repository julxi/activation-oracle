import pathlib
import dotenv
import torch
import transformers
import peft

from typing import Callable
from jaxtyping import Float, Int


dotenv.load_dotenv(".env.local")

# === load all the shit ===
dtype = torch.bfloat16
device = torch.device(
    "mps"
    if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available() else "cpu"
)
MODEL_NAME = "Qwen/Qwen3-8B"
ORACLE_LORA_PATH = "adamkarvonen/checkpoints_latentqa_cls_past_lens_addition_Qwen3-8B"

config = transformers.AutoConfig.from_pretrained(MODEL_NAME)
tokenizer = transformers.AutoTokenizer.from_pretrained(MODEL_NAME)
model = transformers.AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    dtype=dtype,
)
model.eval()

dummy_config = peft.LoraConfig()
model.add_adapter(dummy_config, adapter_name="default")
model.load_adapter(ORACLE_LORA_PATH, adapter_name="oracle", is_trainable=False)
