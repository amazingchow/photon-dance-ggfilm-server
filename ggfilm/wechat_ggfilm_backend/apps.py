import threading

from django.apps import AppConfig


class WechatGgfilmBackendConfig(AppConfig):
    name = 'wechat_ggfilm_backend'
    verbose_name = 'GGFilm Backend Service'

    __restart = True
    __restart_lock = threading.Lock()

    def ready(self):
        # TODO: startup code here
        pass

    @classmethod
    def has_restarted(cls):
        if cls.__restart:
            with cls.__restart_lock:
                if cls.__restart:
                    cls.__restart = False
                    return True
                return False
        return False
