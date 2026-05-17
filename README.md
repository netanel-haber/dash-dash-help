# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- |
| vllm | [14015ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725344911) | [6269ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725344911) | [0.20.2+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.20.2) | 2026-05-12T09:22Z |
| sglang | [13656ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725257467) | [5536ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725257467) | [v0.5.11](https://github.com/sgl-project/sglang/releases/tag/v0.5.11) | 2026-05-12T09:19Z |
| VLMEvalKit | [13984ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725488101) | [5484ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725488101) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-05-12T09:24Z |
| transformers | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725022472) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725022472) | [5.8.0](https://github.com/huggingface/transformers/releases/tag/v5.8.0) | 2026-05-12T09:13Z |
| tensorrt-llm | [5743ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725042703) | [2190ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25725042703) | [1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) | 2026-05-12T09:17Z |
| datasets | [3424ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724870060) | [973ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724870060) | [4.8.5](https://github.com/huggingface/datasets/releases/tag/4.8.5) | 2026-05-12T09:10Z |
| llm | [1412ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724907639) | [644ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724907639) | [0.31](https://github.com/simonw/llm/releases/tag/0.31) | 2026-05-12T09:11Z |
| openai | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724938109) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724938109) | [2.36.0](https://github.com/openai/openai-python/releases/tag/v2.36.0) | 2026-05-12T09:11Z |
| langchain-cli | [819ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724956511) | [262ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724956511) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-05-12T09:12Z |
| hf | [1038ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724843951) | [380ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724843951) | [1.14.0](https://github.com/huggingface/huggingface_hub/releases/tag/v1.14.0) | 2026-05-12T09:10Z |
| lm-eval | [1910ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724992970) | [330ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724992970) | [0.4.12](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.12) | 2026-05-12T09:13Z |
| llama.cpp | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724978142) | [12ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724978142) | [b9114](https://github.com/ggml-org/llama.cpp/releases/tag/b9114) | 2026-05-12T09:12Z |
| ollama | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724808408) | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25724808408) | [0.23.2](https://github.com/ollama/ollama/releases/tag/v0.23.2) | 2026-05-12T09:09Z |

Last updated: 2026-05-17 00:38 UTC
