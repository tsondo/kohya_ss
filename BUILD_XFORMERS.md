# Building xFormers for kohya_ss (CUDA 12.8 / Torch 2.8.0)

This document describes how to build and install a reproducible xFormers wheel
for use with kohya_ss training.

---

## Environment

- Python 3.10
- CUDA Toolkit 12.8
- PyTorch 2.8.0+cu128
- TorchVision 0.23.0+cu128
- NumPy 1.26.x (must be < 1.28 to avoid SciPy ABI errors)
- SciPy < 1.14

---

## Build Steps

1. Clone the xFormers source:

   git clone https://github.com/facebookresearch/xformers.git
   cd xformers

2. Create and activate a clean venv:

   python3 -m venv .venv
   source .venv/bin/activate

3. Install prerequisites (Torch must match your CUDA toolkit):

   pip install --upgrade pip
   pip install torch==2.8.0+cu128 torchvision==0.23.0+cu128 \
       --index-url https://download.pytorch.org/whl/cu128

4. Build the wheel without isolation (so it uses your Torch/CUDA):

   mkdir -p ~/xformers-build/dist
   pip wheel . --no-deps --no-build-isolation -w ~/xformers-build/dist

5. Verify the artifact:

   ls -lh ~/xformers-build/dist/
   # Example: xformers-0.0.33+5d4b92a5.d20251026-cp39-abi3-linux_x86_64.whl

---

## Installation into kohya_ss

From inside the kohya_ss virtual environment:

   pip install --force-reinstall ~/xformers-build/dist/xformers-0.0.33+*.whl

Confirm Torch and CUDA alignment:

   python -c "import torch; print(torch.__version__, torch.version.cuda)"
   # Expected: 2.8.0+cu128  12.8

---

## Notes

- Do **not** use NumPy 2.x — it will break SciPy/diffusers with ABI errors.
- If you rebuild xFormers, reinstall the new wheel into kohya_ss.
- Always commit the wheel artifact and `requirements.txt` snapshot to preserve reproducibility.
