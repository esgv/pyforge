def partial(decorator, target_arg):
    target_pos, target_name = target_arg
    
    def new_decorator(func):
        def new_func(*args, **kwargs):
            if len(args) > target_pos:
                target_arg = args[target_pos]
                preceding_args = tuple(args[:target_pos]) 
                trailing_args = tuple(args[target_pos + 1:])
            else:
                target_arg = kwargs[target_name]
                other_kwargs = kwargs
                other_kwargs.pop(target_name)
                
            @decorator
            def to_be_decorated(arg):
                if len(args) > target_pos:
                    other_args = preceding_args + (arg,) + trailing_args
                    return func(*other_args, **kwargs)
                else:
                    other_kwargs[target_name] = arg
                    return func(*args, **other_kwargs)
            
            return to_be_decorated(target_arg)
        
        return new_func
    
    return new_decorator

def vectorize(func):
    def vectorized_func(arg):
        if isinstance(arg, (list, tuple)):
            return type(arg)(map(func, arg))
        elif hasattr(arg, '__iter__') and not isinstance(arg, str):
            return map(func, arg)
        else:
            return func(arg)
        
    return vectorized_func

def cache_iterable_argument(func):
    def decorated_func(arg):
        if isinstance(arg, (list, tuple)):
            return func(arg)
        else:
            return func(list(arg))
        
    return decorated_func

def works_with_line_list(func):
    def decorated_func(lines):
        if isinstance(lines, str):
            return func(lines.splitlines())
        else:
            return func(lines)
        
    return decorated_func

def works_with_module_dict(func):
    def decorated_func(module):
        if hasattr(module, '__getitem__'):
            return func(module)
        else:
            return func(module.__dict__)
        
    return decorated_func

def cache(func):
    cache = {}

    def decorated_func(*args):
        nonlocal cache
        if not (args in cache):
            cache[args] = func(*args)
        return cache[args]

    return decorated_func

