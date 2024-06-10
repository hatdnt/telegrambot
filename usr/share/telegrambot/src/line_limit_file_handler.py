import logging

class LineLimitFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=100, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)
        self.max_lines = max_lines

    def emit(self, record):
        super().emit(record)
        self._enforce_line_limit()

    def _enforce_line_limit(self):
        with open(self.baseFilename, 'r+', encoding=self.encoding) as file:
            lines = file.readlines()
            if len(lines) > self.max_lines:
                file.seek(0)
                file.writelines(lines[-self.max_lines:])
                file.truncate()