# The machine

One workstation, used for local LLM agents research. All results in this repo were measured on it.

| | |
|---|---|
| GPUs | **4× AMD Radeon AI PRO R9700** (RDNA4, gfx1201, 32 GB GDDR6 each, 128 GB total) |
| GPU links | PCIe Gen5 x8 / x4 / x8 / x4 (the cards' on-board switch reports x16 at the endpoint; the slot link is the real one) |
| GPU power / cooling | 250 W cap per card (range 210–330 W), custom fan curve; ≤ 83 °C junction under full 4-card load |
| Motherboard | Gigabyte B850 AI TOP |
| CPU / RAM | AMD Ryzen 7 9700X / 64 GB DDR5 |
| PSU | be quiet! Dark Power Pro 13, 1600 W |
| OS | Ubuntu 24.04.5, kernel 7.0 |
| GPU stack | ROCm 7.2.4 (`amdgpu-install --usecase=rocm --no-dkms`), in-tree amdgpu, `amdgpu.ppfeaturemask=0xfff7ffff` (overdrive, for the fan curve) |
| Inference | llama.cpp (HIP build, `GGML_HIP=ON`, `GPU_TARGETS=gfx1201`), commit recorded in every run |
| Serving | [llama-swap](https://github.com/mostlygeek/llama-swap) v255 in front of `llama-server`; one model in VRAM at a time; config in [serving/llama-swap.yaml](serving/llama-swap.yaml) |

Multi-GPU inference uses `--split-mode layer` with tuned tensor splits (see `perf/configs/`). How it was built and tuned (lane plan, BIOS, risers, fan curve, monitoring) and the traps on the way:
[radeon-r9700-rocm-notes](https://github.com/michal-konik-human/radeon-r9700-rocm-notes).
