# dash-dash-help

Let's help help help devs.

`--help` should take <1000ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | hardware | gpu time | gpu cost | measured on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| vllm | [21829ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27422517342) | [8882ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27422517342) | [0.22.1+precompiled](https://github.com/vllm-project/vllm/releases/tag/v0.22.1) | [1x RTX 3060](https://cloud.vast.ai/instances/40715981) | 303s | $0.0066 | 2026-06-12T14:42Z |
| VLMEvalKit | [15757ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [6397ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) |  |  |  | 2026-06-05T15:50Z |
| sglang | [28834ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [5252ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [v0.5.12.post1](https://github.com/sgl-project/sglang/releases/tag/v0.5.12.post1) |  |  |  | 2026-06-05T15:45Z |
| tensorrt-llm | [6722ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [2109ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) |  |  |  | 2026-06-05T15:43Z |
| datasets | [3092ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024437557) | [788ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024437557) | [5.0.0](https://github.com/huggingface/datasets/releases/tag/5.0.0) |  |  |  | 2026-06-05T15:38Z |
| llm | [1399ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024470497) | [618ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024470497) | [0.31](https://github.com/simonw/llm/releases/tag/0.31) |  |  |  | 2026-06-05T15:38Z |
| openai | [1201ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27092062663) | [525ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27092062663) | [2.34.0](https://github.com/openai/openai-python/releases/tag/v2.34.0) |  |  |  | 2026-06-07T12:06Z |
| hf | [1148ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024410507) | [392ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024410507) | [1.18.0](https://github.com/huggingface/huggingface_hub/releases/tag/v1.18.0) |  |  |  | 2026-06-05T15:37Z |
| langchain-cli | [863ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024512190) | [295ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024512190) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) |  |  |  | 2026-06-05T15:39Z |
| lm-eval | [1577ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024547386) | [246ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024547386) | [0.4.12](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.12) |  |  |  | 2026-06-05T15:40Z |
| tokenspeed | [601ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27348393122) | [207ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27348393122) | [0.1.0@4df7c87](https://github.com/lightseekorg/tokenspeed/commit/4df7c87969b744fc8af62a59cfdc49f4439c30eb) |  |  |  | 2026-06-11T12:58Z |
| ollama | [15ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024369716) | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024369716) | [0.30.5](https://github.com/ollama/ollama/releases/tag/v0.30.5) |  |  |  | 2026-06-05T15:37Z |
| llama.cpp | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [11ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [b9529](https://github.com/ggml-org/llama.cpp/releases/tag/b9529) |  |  |  | 2026-06-05T15:39Z |
| transformers | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [5.10.2](https://github.com/huggingface/transformers/releases/tag/v5.10.2) |  |  |  | 2026-06-05T15:41Z |

Last updated: 2026-06-12 14:42 UTC
