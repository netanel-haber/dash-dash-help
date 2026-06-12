# dash-dash-help

Let's help help help devs.

`--help` should take <1000ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | hardware | measured on |
| --- | --- | --- | --- | --- | --- |
| VLMEvalKit | [15757ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [6397ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024947957) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) |  | 2026-06-05T15:50Z |
| vllm | [13383ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [5607ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [0.22.1+precompiled](https://github.com/vllm-project/vllm/releases/tag/v0.22.1) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| sglang | [28834ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [5252ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024732605) | [v0.5.12.post1](https://github.com/sgl-project/sglang/releases/tag/v0.5.12.post1) |  | 2026-06-05T15:45Z |
| tensorrt-llm | [6722ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [2109ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024612193) | [1.2.1](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.1) |  | 2026-06-05T15:43Z |
| datasets | [2593ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [787ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [5.0.0](https://github.com/huggingface/datasets/releases/tag/5.0.0) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| llm | [1015ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [452ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [0.31](https://github.com/simonw/llm/releases/tag/0.31) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| openai | [822ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [397ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [2.34.0](https://github.com/openai/openai-python/releases/tag/v2.34.0) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| hf | [1083ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [294ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [1.19.0](https://github.com/huggingface/huggingface_hub/releases/tag/v1.19.0) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| lm-eval | [1346ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [254ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [0.4.12](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.12) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| tokenspeed | [601ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27348393122) | [207ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27348393122) | [0.1.0@4df7c87](https://github.com/lightseekorg/tokenspeed/commit/4df7c87969b744fc8af62a59cfdc49f4439c30eb) |  | 2026-06-11T12:58Z |
| langchain-cli | [615ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [199ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| llama.cpp | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [11ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024535316) | [b9529](https://github.com/ggml-org/llama.cpp/releases/tag/b9529) |  | 2026-06-05T15:39Z |
| ollama | [58ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [8ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27425885794) | [0.30.7](https://github.com/ollama/ollama/releases/tag/v0.30.7) | [1x RTX 3060](https://cloud.vast.ai/create/?q=gpu_name%3DRTX%203060) | 2026-06-12T15:46Z |
| transformers | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/27024583058) | [5.10.2](https://github.com/huggingface/transformers/releases/tag/v5.10.2) |  | 2026-06-05T15:41Z |
