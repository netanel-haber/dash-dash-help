# dash-dash-help

Let's help help help devs.

`--help` should take <1000ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | hardware | measured |
| --- | --- | --- | --- | --- | --- |
| tensorrt-llm | [27677ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [12076ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| vllm | [16793ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [7011ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.23.0+precompiled](https://github.com/vllm-project/vllm/releases/tag/v0.23.0) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| sglang | [13377ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [4985ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.5.9](https://github.com/sgl-project/sglang/releases/tag/v0.5.9) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| VLMEvalKit | [13124ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [4500ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| transformers | [7027ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [2756ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [5.12.0](https://github.com/huggingface/transformers/releases/tag/v5.12.0) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| datasets | [2750ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [818ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [5.0.0](https://github.com/huggingface/datasets/releases/tag/5.0.0) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| llm | [1106ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [462ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.31](https://github.com/simonw/llm/releases/tag/0.31) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| openai | [986ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27474901977) | [415ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27474901977) | [2.34.0](https://github.com/openai/openai-python/releases/tag/v2.34.0) | CPU: AMD Ryzen 7 3700X 8-Core Processor<br>GPU: 1x RTX 3060 | Jun 13, 2026 18:13 UTC |
| hf | [829ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [326ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [1.19.0](https://github.com/huggingface/huggingface_hub/releases/tag/v1.19.0) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| lm-eval | [1616ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [294ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.4.12](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.12) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| langchain-cli | [691ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [229ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| tokenspeed | [467ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [180ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [0.1.0@2aea1aa](https://github.com/lightseekorg/tokenspeed/commit/2aea1aafb9c1c45bccf9f30d471a6320306f676d) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| llama.cpp | [41ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [30ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27472047825) | [b9624](https://github.com/ggml-org/llama.cpp/releases/tag/b9624) | GPU: 1x RTX 3060 | Jun 13, 2026 16:52 UTC |
| ollama | [25ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27474901977) | [20ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27474901977) | [0.30.8](https://github.com/ollama/ollama/releases/tag/v0.30.8) | CPU: AMD Ryzen 7 3700X 8-Core Processor<br>GPU: 1x RTX 3060 | Jun 13, 2026 18:13 UTC |
