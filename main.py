# import threading
# import traceback
# import time
# from typing import Optional, List


# class ThreadMgr:
#     def __init__(self, threads: List) -> None:
#         self.stop = False
#         self.threads: List[BaseThread] = []
#         for thread in threads:
#             self.create_thread(thread)
#         # self.thread1 = Thread1(self)
#         # self.thread2 = Thread2(self)

#     def add_thread(self, thread: 'BaseThread') -> None:
#         self.threads.append(thread)

#     def del_thread(self, thread: 'BaseThread') -> None:
#         try:
#             self.threads.remove(thread)
#         except ValueError:
#             pass

#     def create_thread(self, thread: 'BaseThread') -> None:
#         thread_cls = thread.__class__
#         self.del_thread(thread)
#         t = thread_cls()
#         self.add_thread(t)
#         t.start()

#     def start(self) -> None:
#         # for t in self.threads:
#         #     if not t.is_alive():
#         #         t.start()
#         self.loop()

#     def loop(self) -> None:
#         while not self.stop:
#             for t in self.threads:
#                 print(f'checking thread {t.__class__.__name__}')
#                 try:
#                     status = t.check_status()
#                     thread_class = t.__class__.__name__
#                     label = 'Ok' if status else 'Critical'
#                     print(f'thread {t.__class__.__name__} status: {label}')
#                 except Exception as e:
#                     exc = e.__class__.__name__
#                     print(f'thread {thread_class} not running: {exc}: {e}')
#                     self.create_thread(t)
#                 else:
#                     print('foo')
#             time.sleep(3)


# class BaseThread(threading.Thread):
#     def __init__(self) -> None:
#         super().__init__()
#         self.exc: Optional[Exception] = None
#         self.stop: bool = False

#     def run(self) -> None:
#         try:
#             self.loop()
#         except Exception as e:
#             print('foo')
#             self.exc = e
#             return

#     def check_status(self) -> bool:
#         if not self.is_alive():
#             raise RuntimeError('error!.')
#         if self.exc:
#             traceback.print_tb(self.exc.__traceback__)
#             print(f'{self.exc.__class__.__name__}: {self.exc}')
#             raise self.exc
#         return True

#     def loop(self) -> None:
#         raise NotImplementedError()


# class Thread1(BaseThread):
#     def __init__(self) -> None:
#         super().__init__()

#     def loop(self) -> None:
#         while True:
#             print("Thread1 1")
#             time.sleep(1)
#             print("Thread1 2")
#             time.sleep(1)
#             raise Exception("Thread1")


# class Thread2(BaseThread):
#     def __init__(self) -> None:
#         super().__init__()

#     def loop(self) -> None:
#         while not self.stop:
#             print("Thread2")
#             time.sleep(2)


# def main() -> None:
#     t_mgr = ThreadMgr([Thread1, Thread2()])
#     t_mgr.start()


# if __name__ == '__main__':
#     main()

import threading
import traceback
import time
from typing import Optional, List


class ThreadMgr:
    def __init__(self, thread_cls: List) -> None:
        self.stop = False
        self.threads: List[BaseThread] = []
        for c in thread_cls:
            self.threads.append(c())
            # self.create_thread_from_cls(c)
        # self.thread1 = Thread1(self)
        # self.thread2 = Thread2(self)

    def add_thread(self, thread: 'BaseThread') -> None:
        self.threads.append(thread)

    def del_thread(self, thread: 'BaseThread') -> None:
        try:
            self.threads.remove(thread)
        except ValueError:
            pass

    def create_thread_from_cls(self, thread: 'BaseThread') -> None:
        thread_cls = thread.__class__
        self.del_thread(thread)
        t = thread_cls()
        self.add_thread(t)
        t.start()

    def start(self) -> None:
        # for t in self.threads:
        #     if not t.is_alive():
        #         t.start()
        self.loop()

    def loop(self) -> None:
        while not self.stop:
            for t in self.threads:
                print(f'checking thread {t.__class__.__name__}')
                try:
                    status = t.check_status()
                    label = 'Ok' if status else 'Critical'
                    print(f'thread {t.__class__.__name__} status: {label}')
                except Exception as e:
                    exc = e.__class__.__name__
                    thread_class = t.__class__.__name__
                    print(f'thread {thread_class} not running: {exc}: {e}')
                    self.create_thread_from_cls(t)
                # else:
                #     print(f'{t.__class__.__name__} is running.')
            time.sleep(3)


class BaseThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.exc: Optional[Exception] = None
        self.stop: bool = False

    def run(self) -> None:
        print(f'starting {self.__class__.__name__}')
        try:
            self.loop()
        except Exception as e:
            print(f'{e}')
            self.exc = e
            return

    def check_status(self) -> bool:
        if not self.is_alive():
            self.start()
        print(f'check status of {self.__class__.__name__}')
        if self.exc:
            traceback.print_tb(self.exc.__traceback__)
            print(f'{self.exc.__class__.__name__}: {self.exc}')
            raise self.exc
        return True

    def loop(self) -> None:
        raise NotImplementedError()


class Thread1(BaseThread):
    def __init__(self) -> None:
        super().__init__()

    def loop(self) -> None:
        while True:
            print("Thread1 1")
            time.sleep(1)
            print("Thread1 2")
            time.sleep(1)
            # raise Exception("Thread1")


class Thread2(BaseThread):
    def __init__(self) -> None:
        super().__init__()

    def loop(self) -> None:
        while not self.stop:
            print("Thread2")
            time.sleep(2)


def main() -> None:
    t_mgr = ThreadMgr([Thread1, Thread2])
    t_mgr.start()


if __name__ == '__main__':
    main()
