# -*- coding: utf-8 -*-
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity


Builder.load_string('''
<RootWidget>:
    Button:
        text: wv.url
        on_release: wv.create_webview()
    Wv:
        id: wv

<Wv>:
''')


class RootWidget(BoxLayout):
    pass


class Wv(Widget):

    url = StringProperty('url')

    def __init__(self, **kwargs):
        super(Wv, self).__init__(**kwargs)
        #Clock.schedule_once(self.create_webview, 5)

    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        wvc = WebViewClient();
        webview.setWebViewClient(wvc);
        activity.setContentView(webview)
        webview.loadUrl(
            'https://www.facebook.com/v2.8/dialog/oauth?'
            'client_id=303848833322071&'
            'redirect_uri=https://mytestapp-1146e.firebaseapp.com/__/auth/handler'
        )
        self.url = webview.getOriginalUrl()


class ServiceApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    ServiceApp().run()
