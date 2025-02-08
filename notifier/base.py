import schedule
import time
from abc import abstractmethod, ABC


class Notifier(ABC):
    is_active: bool = False

    def start_scheduler(self):
        self.is_active = True

        schedule.every(1).week.do(self._execute()) # будет ли нормально работать несколько шедулеров, каждый со своим классом?

        while self.is_active:
            schedule.run_pending()
            time.sleep(1)
        pass

    def stop_scheduler(self):
        self.is_active = False


    def _execute(self):
        self.__get_data()
        self.__write_message()
        self.__send_message()

    @abstractmethod
    def __get_data(self):
        data = ""
        #Тут работа с data_manager. Он предоставляет данные. Data manager скрывает за собой источники.
        return data

    @abstractmethod
    def __send_message(self):
        pass

    @abstractmethod
    def __write_message(self):
        pass

