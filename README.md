# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | command | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- | --- |
| VLLM | `.venv/bin/vllm --help` | [16214ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683151092) | [7580ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683151092) | [0.13.0+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) | 2026-01-03T21:30Z |
| SGLang | `.venv/bin/python -m sglang.launch_server --help` | [13988ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684833400) | [5573ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684833400) | [v0.5.7](https://github.com/sgl-project/sglang/releases/tag/v0.5.7) | 2026-01-04T00:09Z |
| VLMEvalKit | `./VLMEvalKit/.venv/bin/python ./VLMEvalKit/run.py --help` | [13719ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683191064) | [4843ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683191064) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-01-03T21:34Z |
| Transformers | `.venv/bin/transformers-cli --help` | [8195ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683078788) | [3328ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683078788) | [4.57.3](https://github.com/huggingface/transformers/releases/tag/v4.57.3) | 2026-01-03T21:21Z |
| TensorRT-LLM | `.venv/bin/trtllm-serve --help` | [6525ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684760216) | [2277ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684760216) | [1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) | 2026-01-04T00:05Z |
| Datasets | `.venv/bin/datasets-cli --help` | [2635ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683049447) | [815ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683049447) | [4.4.2](https://github.com/huggingface/datasets/releases/tag/4.4.2) | 2026-01-03T21:18Z |
| LLM | `.venv/bin/llm --help` | [1133ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683055429) | [518ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683055429) | [0.28](https://github.com/simonw/llm/releases/tag/0.28) | 2026-01-03T21:18Z |
| OpenAI | `.venv/bin/openai --help` | [1071ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684867429) | [511ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684867429) | [2.14.0](https://github.com/openai/openai-python/releases/tag/v2.14.0) | 2026-01-04T00:11Z |
| LangChain CLI | `.venv/bin/langchain --help` | [883ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684777476) | [273ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684777476) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-01-04T00:03Z |
| Hugging Face Hub | `.venv/bin/hf --help` | [727ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684901800) | [226ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684901800) | [1.2.3](https://github.com/huggingface/huggingface_hub/releases/tag/v1.2.3) | 2026-01-04T00:14Z |
| lm-eval | `.venv/bin/lm-eval --help` | [50ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684833482) | [43ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684833482) | [0.4.9.2](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.9.2) | 2026-01-04T00:08Z |
| llama.cpp | `./llama-bin/llama-cli --help` | [24ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684881969) | [17ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684881969) | [b7622](https://github.com/ggml-org/llama.cpp/releases/tag/b7622) | 2026-01-04T00:12Z |
| Ollama | `ollama --help` | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683033506) | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20683033506) | [0.13.5](https://github.com/ollama/ollama/releases/tag/v0.13.5) | 2026-01-03T21:17Z |

Last updated: 2026-01-04 00:19 UTC
