from blinker import Namespace

my_signals = Namespace()

get_message = my_signals.signal('get_message')
