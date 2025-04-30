import torch

print(f"PyTorch version: {torch.__version__}")

if torch.cuda.is_available():
    print(f"CUDA available: Yes")
    print(f"CUDA version: {torch.version.cuda}")
else:
    print("CUDA available: No")