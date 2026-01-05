# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | command | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- | --- |
| VLLM | `.venv/bin/vllm --help` | [15013ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685115316) | [6593ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685115316) | [0.13.0+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.13.0) | 2026-01-04T00:37Z |
| SGLang | `.venv/bin/python -m sglang.launch_server --help` | [13875ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701236663) | [5490ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701236663) | [v0.5.7](https://github.com/sgl-project/sglang/releases/tag/v0.5.7) | 2026-01-05T00:09Z |
| VLMEvalKit | `./VLMEvalKit/.venv/bin/python ./VLMEvalKit/run.py --help` | [14704ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685041628) | [5061ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685041628) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-01-04T00:29Z |
| Transformers | `.venv/bin/transformers-cli --help` | [7988ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684996672) | [3147ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684996672) | [4.57.3](https://github.com/huggingface/transformers/releases/tag/v4.57.3) | 2026-01-04T00:24Z |
| TensorRT-LLM | `.venv/bin/trtllm-serve --help` | [8208ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701139723) | [2372ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701139723) | [1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) | 2026-01-05T00:04Z |
| Datasets | `.venv/bin/datasets-cli --help` | [2744ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684980345) | [832ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684980345) | [4.4.2](https://github.com/huggingface/datasets/releases/tag/4.4.2) | 2026-01-04T00:21Z |
| LLM | `.venv/bin/llm --help` | [1268ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684972418) | [544ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20684972418) | [0.28](https://github.com/simonw/llm/releases/tag/0.28) | 2026-01-04T00:21Z |
| OpenAI | `.venv/bin/openai --help` | [1591ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701282803) | [505ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701282803) | [2.14.0](https://github.com/openai/openai-python/releases/tag/v2.14.0) | 2026-01-05T00:11Z |
| LangChain CLI | `.venv/bin/langchain --help` | [749ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701163240) | [253ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701163240) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-01-05T00:03Z |
| Hugging Face Hub | `.venv/bin/hf --help` | [805ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701326540) | [218ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701326540) | [1.2.3](https://github.com/huggingface/huggingface_hub/releases/tag/v1.2.3) | 2026-01-05T00:14Z |
| lm-eval | `.venv/bin/lm-eval --help` | [49ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701238026) | [43ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701238026) | [0.4.9.2](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.9.2) | 2026-01-05T00:08Z |
| llama.cpp | `./llama-bin/llama-cli --help` | [26ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701304257) | [17ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20701304257) | [b7626](https://github.com/ggml-org/llama.cpp/releases/tag/b7626) | 2026-01-05T00:12Z |
| Ollama | `ollama --help` | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685077611) | [12ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/20685077611) | [0.13.5](https://github.com/ollama/ollama/releases/tag/v0.13.5) | 2026-01-04T00:31Z |

Last updated: 2026-01-05 00:19 UTC
