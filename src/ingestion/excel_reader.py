from io import BytesIO
from typing import Optional

import pandas as pd
from python_calamine import CalamineWorkbook


def read_excel_bytes(binary: bytes, sheet_name: Optional[str] = None, usecols: Optional[list[str]] = None) -> pd.DataFrame:
    workbook = CalamineWorkbook.from_filelike(BytesIO(binary))
    selected_sheet = sheet_name or workbook.sheet_names[0]
    rows = workbook.get_sheet_by_name(selected_sheet).to_python(skip_empty_area=False)

    if not rows:
        return pd.DataFrame()

    headers = [str(h).replace("\xa0", " ").strip() if h is not None else "" for h in rows[0]]
    indexes = [i for i, h in enumerate(headers) if usecols is None or h in set(usecols)]

    data = [
        [str(row[i]).strip() if i < len(row) and row[i] is not None else "" for i in indexes]
        for row in rows[1:]
    ]
    return pd.DataFrame(data, columns=[headers[i] for i in indexes])
