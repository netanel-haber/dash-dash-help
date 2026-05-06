# dash-dash-help

Let's help help help devs.

`--help` should take <200ms. Most LLM CLI tools take 10+ seconds because they import torch/transformers just to print usage text.

https://dashdashhelp.win

| library | cold | warm (10 runs) | version | measured on |
| --- | --- | --- | --- | --- |
| vllm | [14194ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25251918998) | [6591ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/25251918998) | [0.20.0+cpu](https://github.com/vllm-project/vllm/releases/tag/v0.20.0) | 2026-05-02T12:31Z |
| sglang | [13130ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24403106751) | [5464ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24403106751) | [v0.5.10.post1](https://github.com/sgl-project/sglang/releases/tag/v0.5.10.post1) | 2026-04-14T13:58Z |
| VLMEvalKit | [13244ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24403409806) | [5338ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24403409806) | [v0.2](https://github.com/open-compass/VLMEvalKit/releases/tag/v0.2) | 2026-04-14T14:04Z |
| transformers | [1ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402924852) | [0ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402924852) | [5.5.4](https://github.com/huggingface/transformers/releases/tag/v5.5.4) | 2026-04-14T13:53Z |
| tensorrt-llm | [6517ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402949823) | [2183ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402949823) | [1.2.0](https://github.com/NVIDIA/TensorRT-LLM/releases/tag/v1.2.0) | 2026-04-14T13:57Z |
| datasets | [3241ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402780526) | [975ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402780526) | [4.8.4](https://github.com/huggingface/datasets/releases/tag/4.8.4) | 2026-04-14T13:51Z |
| llm | [1174ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402810655) | [539ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402810655) | [0.30](https://github.com/simonw/llm/releases/tag/0.30) | 2026-04-14T13:51Z |
| openai | [1069ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402841277) | [535ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402841277) | [2.31.0](https://github.com/openai/openai-python/releases/tag/v2.31.0) | 2026-04-14T13:52Z |
| langchain-cli | [844ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402866274) | [257ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402866274) | [0.0.37](https://github.com/langchain-ai/langchain/releases/tag/langchain-cli==0.0.37) | 2026-04-14T13:52Z |
| hf | [1351ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402759822) | [389ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402759822) | [1.10.2](https://github.com/huggingface/huggingface_hub/releases/tag/v1.10.2) | 2026-04-14T13:50Z |
| lm-eval | [751ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402898149) | [251ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402898149) | [0.4.11](https://github.com/EleutherAI/lm-evaluation-harness/releases/tag/v0.4.11) | 2026-04-14T13:53Z |
| llama.cpp | [16ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402884321) | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402884321) | [b8784](https://github.com/ggml-org/llama.cpp/releases/tag/b8784) | 2026-04-14T13:53Z |
| ollama | [14ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402724003) | [12ms](https://github.com/netanel-haber/dash-dash-help/actions/runs/24402724003) | [0.20.7](https://github.com/ollama/ollama/releases/tag/v0.20.7) | 2026-04-14T13:50Z |

Last updated: 2026-05-06 00:33 UTC
