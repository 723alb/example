import numpy as np
from django.core.files.uploadedfile import InMemoryUploadedFile
from map_parser.parsers.abstract_parser import Parser


class ImapParser(Parser):
    empty_value = 9999900

    @classmethod
    def parse(cls, file: InMemoryUploadedFile, additional_data: InMemoryUploadedFile) -> dict:
        """
        Парсинг карт в формате Irap Classic Grid
        :param file - загруженный файл
        :param additional_data - содержимое сопроводительного файла
        """
        # Читаем размер сетки
        lines = file.readlines()
        num_x = int(lines[0].split()[1])  # Количество строк
        num_y = int(lines[2].split()[0])  # Количество столбцов
        header = lines[:4]  # Читаем шапку файла
        data_lines = lines[4:]  # Данные сетки

        # Создаем массив для данных
        grid_values = np.zeros((num_x, num_y))

        x_i, y_i = 0, 0
        for line in data_lines:
            values = line.split()
            for val in values:
                if float(val) != cls.empty_value:  # Пропускаем отсутствующие значения
                    grid_values[x_i][y_i] = float(val)
                y_i += 1
                if y_i == num_y:  # Переход на следующую строку
                    y_i = 0
                    x_i += 1

        return {'data': grid_values.tolist(),
                'description': {'data': str(additional_data.read()), **cls._get_metadata(header)}}

    @staticmethod
    def _get_metadata(header: list[bytes]) -> dict:
        """Чтение метаданных"""
        line0 = header[0].split()
        line1 = header[1].split()
        return {
            'dx': float(line0[2]),
            'dy': float(line0[3]),
            'xmin': float(line1[0]),
            'xmax': float(line1[1]),
            'ymin': float(line1[2]),
            'ymax': float(line1[3]),
        }
