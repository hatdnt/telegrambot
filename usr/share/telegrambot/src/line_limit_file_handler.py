import logging

class LineLimitFileHandler(logging.FileHandler):
    def __init__(self, filename, max_lines=1000, mode='a', encoding=None, delay=False):
        self.max_lines = max_lines
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        try:
            if self.stream is None:
                self.stream = self._open()
            if self.stream.tell() > self.max_lines:
                self.stream.close()
                self.stream = self._open()
            super().emit(record)
        except Exception:
            self.handleError(record)