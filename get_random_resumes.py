import random
from pathlib import Path

def get_random_resumes(folder: str, n: int = 5) -> list[Path]:
    pdf_files = list(Path(folder).rglob("*.pdf"))
    random.seed(10)
    selected_pdfs = random.sample(pdf_files, n)
    return selected_pdfs
    