class CodinCodException(Exception):
    msg: str
    status: int

    def __init__(self, msg: str, status: int = 400) -> None:
        self.msg = msg
        self.status = status
        super().__init__()

    def __str__(self) -> str:
        return f"msg: {self.msg} | status_code: {self.status}"