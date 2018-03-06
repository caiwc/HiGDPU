import datetime


def timeoutFn(func, kwargs={}, timeout_duration=1, default=None):
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        print('time out')
        raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_duration)
    try:
        result = func(**kwargs)
    except TimeoutError as exc:
        result = default
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)

    return result


def gen_filename(source_name):
    import time
    file_name = str(time.time())
    file_name = '%s-%s' % (file_name, source_name)
    extension = ''
    if len(source_name.split('.')) > 1:
        extension = '.' + source_name.split('.')[-1]
        extension = extension.replace(' ', '')
    import hashlib
    file_name = hashlib.new("md5", file_name.encode('utf-8')).hexdigest() + extension
    return file_name


def weibo_time_format(time_str):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    return datetime.datetime.strptime(time_str, GMT_FORMAT)
