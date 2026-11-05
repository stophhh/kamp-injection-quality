"""실행 전 공개 파일 구문·출력·금지 파일 검사. 모델 성능 검증은 아닙니다."""
import ast
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
        continue
    if path.suffix.lower() in {".csv", ".tsv", ".xlsx", ".zip", ".pkl", ".joblib"}:
        raise ValueError(f"공개 검토가 필요한 파일: {path.relative_to(root)}")
    if path.suffix == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] == "code":
                if cell.get("outputs") or cell.get("execution_count") is not None:
                    raise ValueError(f"노트북 출력이 남았습니다: {path.name}, cell {index}")
                ast.parse("".join(cell["source"]))
print("공개 파일 구조·노트북 구문·출력 검사 통과. 실제 학습 검증은 별도입니다.")
