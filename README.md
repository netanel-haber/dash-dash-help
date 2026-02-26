# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- |
| vllm | [15610ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/21456701512) | [7473ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/21456701512) | [0.14.1+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.14.1) | 2026-01-28T21:50Z |
| sglang | [15662ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394388327) | [6825ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394388327) | [v0.5.9](https://github.com/sgl-project/sglang/releases/tag/v0.5.9) | 2026-02-25T11:16Z |
| VLMEvalKit | [13936ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394562217) | [5076ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394562217) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-02-25T11:21Z |
| transformers | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394050081) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394050081) | [5.2.0](https://github.com/huggingface/transformers/releases/tag/v5.2.0) | 2026-02-25T11:04Z |
| tensorrt-llm | [7467ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394060364) | [2600ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394060364) | [1.0.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.0.0) | 2026-02-25T11:14Z |
| datasets | [3074ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393976449) | [907ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393976449) | [4.5.0](https://github.com/huggingface/datasets/releases/tag/4.5.0) | 2026-02-25T11:02Z |
| llm | [1205ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393990717) | [569ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393990717) | [0.28](https://github.com/simonw/llm/releases/tag/0.28) | 2026-02-25T11:03Z |
| openai | [1053ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394005087) | [504ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394005087) | [2.24.0](https://github.com/openai/openai-python/releases/tag/v2.24.0) | 2026-02-25T11:03Z |
| langchain-cli | [845ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394017290) | [259ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394017290) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-02-25T11:03Z |
| hf | [990ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393965273) | [331ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393965273) | [1.4.1](https://github.com/huggingface/huggingface_hub/releases/tag/v1.4.1) | 2026-02-25T11:02Z |
| lm-eval | [800ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394037930) | [228ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394037930) | [0.4.11](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.11) | 2026-02-25T11:04Z |
| llama.cpp | [19ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394029264) | [13ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22394029264) | [b8149](https://github.com/ggml-org/llama.cpp/releases/tag/b8149) | 2026-02-25T11:04Z |
| ollama | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393921697) | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/22393921697) | [0.17.0](https://github.com/ollama/ollama/releases/tag/v0.17.0) | 2026-02-25T11:02Z |

Last updated: 2026-02-26 00:20 UTC
