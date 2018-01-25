import functools
import copy


def validate_decorator(**need_arg):
    '''
       参数验证装饰器
       :param need_arg: 需要验证的参数名称 包含参数类型,参数所需要有的属性或子参数
       :return:
    '''

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kw):
            for arg in need_arg:
                if not arg in kw:
                    raise ValueError('函数使用错误, 无参数%s' % (arg))
                func_arg = kw[arg]
                if func_arg == None:
                    continue
                arg_type = need_arg[arg]['type']
                if not isinstance(func_arg, arg_type):
                    raise ValueError('函数使用错误,参数类型错误')
                if 'must_arg' in need_arg[arg]:
                    must_arg = need_arg[arg]['must_arg']
                    if not isinstance(func_arg, (list, tuple)):
                        func_arg = [func_arg]

                    for item in func_arg:
                        must_arg_copy = copy.deepcopy(must_arg)

                        for a in item:
                            if a not in must_arg_copy:
                                raise ValueError('函数使用错误,%s 含有非法参数%s' % (arg, a))
                            else:
                                must_arg_copy.pop(a)
                        if len(must_arg_copy) > 0:
                            for i in must_arg_copy:
                                if must_arg_copy[i]:
                                    raise ValueError('函数使用错误,%s 缺少参数%s' % (arg, i))
            return func(*args, **kw)

        return wrapper

    return decorator