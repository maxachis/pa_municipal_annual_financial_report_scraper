from pathlib import Path


def get_project_root(marker_files=("requirements.txt",)) -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    raise FileNotFoundError("No project root found (missing marker files)")

def project_path(*parts: str) -> Path:
    return get_project_root().joinpath(*parts)