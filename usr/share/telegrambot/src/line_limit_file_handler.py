import logging

class LineLimitFileHandler(logging.Handler):
    def __init__(self, filename, max_lines=1000, mode='a', encoding=None, delay=False):
        super().__init__()
        self.filename = filename
        self.max_lines = max_lines
        self.mode = mode
        self.encoding = encoding
        self.delay = delay
        self._open()

    def _open(self):
        self.stream = open(self.filename, self.mode, encoding=self.encoding)

    def emit(self, record):
        if self.stream.tell() > self.max_lines:
            self.stream.seek(0)
            self.stream.truncate()
        self.stream.write(self.format(record) + '\n')
        self.stream.flush()

    def close(self):
        self.stream.close()
        super().close()