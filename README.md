# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | command | cold | warm (10 runs) | version |
| ------- | ------- | ---- | -------------- | ------- |
| VLLM | `.venv/bin/vllm --help` | [16110ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680594972) | [7436ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680594972) | [0.13.0+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) |
| VLMEvalKit | `./VLMEvalKit/.venv/bin/python ./VLMEvalKit/run.py --help` | [13885ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680640100) | [5140ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680640100) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) |
| SGLang | `.venv/bin/python -m sglang.launch_server --help` | [11901ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680578863) | [4692ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680578863) | [v0.5.7](https://github.com/sgl-project/sglang/releases/tag/v0.5.7) |
| Transformers | `.venv/bin/transformers-cli --help` | [8164ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680541349) | [3429ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680541349) | [4.57.3](https://github.com/huggingface/transformers/releases/tag/v4.57.3) |
| TensorRT-LLM | `.venv/bin/trtllm-serve --help` | [7228ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680552998) | [2128ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680552998) | [1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) |
| Datasets | `.venv/bin/datasets-cli --help` | [2869ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680510713) | [837ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680510713) | [4.4.2](https://github.com/huggingface/datasets/releases/tag/4.4.2) |
| LLM | `.venv/bin/llm --help` | [1253ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680516866) | [563ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680516866) | [0.28](https://github.com/simonw/llm/releases/tag/0.28) |
| OpenAI | `.venv/bin/openai --help` | [996ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680521314) | [507ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680521314) | [2.14.0](https://github.com/openai/openai-python/releases/tag/v2.14.0) |
| LangChain CLI | `.venv/bin/langchain --help` | [804ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680526223) | [256ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680526223) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) |
| Hugging Face Hub | `.venv/bin/hf --help` | [747ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680506972) | [232ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680506972) | [1.2.3](https://github.com/huggingface/huggingface_hub/releases/tag/v1.2.3) |
| lm-eval | `.venv/bin/lm-eval --help` | [49ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680532423) | [43ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680532423) | [0.4.9.2](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.9.2) |
| llama.cpp | `./llama-bin/llama-cli --help` | [27ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680529801) | [19ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680529801) | [b7621](https://github.com/ggml-org/llama.cpp/releases/tag/b7621) |
| Ollama | `ollama --help` | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680481150) | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20680481150) | [0.13.5](https://github.com/ollama/ollama/releases/tag/v0.13.5) |

Last updated: 2026-01-03 20:48 UTC
