import csv
import io
from typing import List, Dict


def export_to_csv(cards: List[Dict[str, str]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["#", "Question", "Answer"])
    for i, card in enumerate(cards, 1):
        writer.writerow([i, card["question"], card["answer"]])
    return output.getvalue()
