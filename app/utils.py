from xlsxwriter import Workbook


class DataWriter:
    def __init__(self, columns: list[str], filename: str) -> None:
        self.book = Workbook(filename)
        self.columns = columns

    def write_columns(self):
        for i in range(len(self.columns)):
            self.sheet.write(0, i, self.columns[i])

    def write_values(self, data: dict[str, str], limit: int = 100):
        col_number = 1
        for item in data[:limit]:
            for value, index in zip(item.values(), range(len(self.columns))):
                if isinstance(value, dict):
                    for _value in value.values():
                        self.sheet.write(col_number, index, str(_value))
                        col_number += 1
                    col_number -= 1
                else:
                    self.sheet.write(col_number, index, str(value))
            col_number += 1

    def __enter__(self):
        self.sheet = self.book.add_worksheet()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.book.close()
        return False  # Выбрасываем любые ошибки что поймали
