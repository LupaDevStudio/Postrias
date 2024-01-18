from kivy.utils import platform


if platform == "android":
    from android import PythonJavaClass, autoclass, java_method, mActivity
    from android.runnable import run_on_ui_thread

    context = mActivity.getApplicationContext()
    GameServicesHandler = autoclass(
        'org.org.kivygameservices.GameServicesHandler')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

    def connect(*_):
        activity = PythonActivity.mActivity
        game_services_handler = GameServicesHandler(activity)
        game_services_handler.connect()
