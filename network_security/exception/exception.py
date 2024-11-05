import sys
from network_security.logging import logger


class NetworkSecurityException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message
        _, _, exc_tb = error_detail.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in script: [{self.filename}] at line number: [{self.lineno}] error message: [{self.error_message}]"


if __name__ == "__main__":
    try:
        logger.logging.info("Logging has started")
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
