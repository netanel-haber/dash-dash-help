# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | command | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- | --- |
| VLLM | `.venv/bin/vllm --help` | [16214ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683151092) | [7580ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683151092) | [0.13.0+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) | 2026-01-03T21:30Z |
| SGLang | `.venv/bin/python -m sglang.launch_server --help` | [13180ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683132853) | [5422ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683132853) | [v0.5.7](https://github.com/sgl-project/sglang/releases/tag/v0.5.7) | 2026-01-03T21:26Z |
| VLMEvalKit | `./VLMEvalKit/.venv/bin/python ./VLMEvalKit/run.py --help` | [13719ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683191064) | [4843ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683191064) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-01-03T21:34Z |
| Transformers | `.venv/bin/transformers-cli --help` | [8195ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683078788) | [3328ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683078788) | [4.57.3](https://github.com/huggingface/transformers/releases/tag/v4.57.3) | 2026-01-03T21:21Z |
| TensorRT-LLM | `.venv/bin/trtllm-serve --help` | [7481ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683090026) | [2258ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683090026) | [1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) | 2026-01-03T21:25Z |
| Datasets | `.venv/bin/datasets-cli --help` | [2635ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683049447) | [815ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683049447) | [4.4.2](https://github.com/huggingface/datasets/releases/tag/4.4.2) | 2026-01-03T21:18Z |
| LLM | `.venv/bin/llm --help` | [1133ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683055429) | [518ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683055429) | [0.28](https://github.com/simonw/llm/releases/tag/0.28) | 2026-01-03T21:18Z |
| OpenAI | `.venv/bin/openai --help` | [963ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683059081) | [502ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683059081) | [2.14.0](https://github.com/openai/openai-python/releases/tag/v2.14.0) | 2026-01-03T21:18Z |
| LangChain CLI | `.venv/bin/langchain --help` | [808ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683063035) | [280ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683063035) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-01-03T21:19Z |
| Hugging Face Hub | `.venv/bin/hf --help` | [778ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683046219) | [223ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683046219) | [1.2.3](https://github.com/huggingface/huggingface_hub/releases/tag/v1.2.3) | 2026-01-03T21:17Z |
| lm-eval | `.venv/bin/lm-eval --help` | [48ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683069788) | [42ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683069788) | [0.4.9.2](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.9.2) | 2026-01-03T21:20Z |
| llama.cpp | `./llama-bin/llama-cli --help` | [29ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683066798) | [18ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683066798) | [b7621](https://github.com/ggml-org/llama.cpp/releases/tag/b7621) | 2026-01-03T21:19Z |
| Ollama | `ollama --help` | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683033506) | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683033506) | [0.13.5](https://github.com/ollama/ollama/releases/tag/v0.13.5) | 2026-01-03T21:17Z |

Last updated: 2026-01-03 21:55 UTC
