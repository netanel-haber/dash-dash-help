# dash-dash-help

Let's help help help devs.

`--help` should take <1000ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- |
| vllm | [15095ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024843369) | [7172ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024843369) | [0.22.1+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.22.1) | 2026-06-05T15:47Z |
| sglang | [28834ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [5252ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [v0.5.12.post1](https://github.com/sgl-project/sglang/releases/tag/v0.5.12.post1) | 2026-06-05T15:45Z |
| VLMEvalKit | [15757ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [6397ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-06-05T15:50Z |
| transformers | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [5.10.2](https://github.com/huggingface/transformers/releases/tag/v5.10.2) | 2026-06-05T15:41Z |
| tensorrt-llm | [6722ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [2109ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) | 2026-06-05T15:43Z |
| datasets | [3092ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024437557) | [788ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024437557) | [5.0.0](https://github.com/huggingface/datasets/releases/tag/5.0.0) | 2026-06-05T15:38Z |
| llm | [1399ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024470497) | [618ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024470497) | [0.31](https://github.com/simonw/llm/releases/tag/0.31) | 2026-06-05T15:38Z |
| openai | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024493931) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024493931) | [2.41.0](https://github.com/openai/openai-python/releases/tag/v2.41.0) | 2026-06-05T15:39Z |
| langchain-cli | [863ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024512190) | [295ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024512190) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-06-05T15:39Z |
| hf | [1148ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024410507) | [392ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024410507) | [1.18.0](https://github.com/huggingface/huggingface_hub/releases/tag/v1.18.0) | 2026-06-05T15:37Z |
| lm-eval | [1577ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024547386) | [246ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024547386) | [0.4.12](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.12) | 2026-06-05T15:40Z |
| llama.cpp | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [11ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [b9529](https://github.com/ggml-org/llama.cpp/releases/tag/b9529) | 2026-06-05T15:39Z |
| ollama | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024369716) | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024369716) | [0.30.5](https://github.com/ollama/ollama/releases/tag/v0.30.5) | 2026-06-05T15:37Z |

Last updated: 2026-06-05 15:50 UTC
