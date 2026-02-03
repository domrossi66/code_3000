import subprocess
import sys
import venv
from pathlib import Path

ENV_DIR = Path("3000-env")

# Create venv
venv.create(ENV_DIR, with_pip=True)

pip = ENV_DIR / "bin" / "pip"
python = ENV_DIR / "bin" / "python"

packages = [
    "numpy==1.26.4",
    "pandas==2.1.4",
    "scikit-learn==1.3.2",
    "matplotlib==3.8.2",
    "seaborn==0.13.0",
    "shap==0.44.1"
]

subprocess.check_call([pip, "install", "--upgrade", "pip"])
subprocess.check_call([pip, "install", *packages])

subprocess.check_call([
    python, "-c",
    "import numpy, sklearn, shap; print('Setup complete')"
])
