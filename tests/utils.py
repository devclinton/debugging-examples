import os
from functools import wraps
from typing import Union, Callable
import time


def dump_output(output_directory: Union[str, Callable[[Callable], str]] = os.getcwd(),
                capture_output: bool = False):

    import pickle

    def decorate(func):
        # create directory for function output
        # if we have a function for directory naming, call it
        if callable(output_directory):
            out = output_directory(func)
        else:
            out = os.path.abspath(os.path.join(".", func.__name__))

        out_directory = os.path.join(out, 'output')
        input_directory = os.path.join(out, 'input')
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_time = int(round(time.time() * 1000))
            # if output directory is a
            for name, a in [('args', args), ('kwargs', kwargs)]:
                if len(a):
                    os.makedirs(input_directory, exist_ok=True)
                    input_file_out = os.path.join(input_directory, f'{call_time}_{name}.pkl')
                    with open(input_file_out, 'bw') as o:
                        pickle.dump(a, o)
            result = func(*args, **kwargs)
            if capture_output:
                os.makedirs(out_directory, exist_ok=True)
                output_file_out = os.path.join(out_directory, f'{call_time}.pkl')
                with open(output_file_out, 'bw') as o:
                    pickle.dump(result, o)
            return result
        return wrapper
    return decorate