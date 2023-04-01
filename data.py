from abc import ABC, abstractmethod


class Data(ABC):
    required = True

    @abstractmethod
    def check_type(self):
        pass

    @abstractmethod
    def check_required(self):
        pass

    def check_format(self):
        return True

    def problem(self):
        tests = [self.check_type(), self.check_format(), self.check_required()]
        return int(not all(tests))
