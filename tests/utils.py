import os
from functools import wraps
from typing import Union, Callable, Any, Optional
import time


TEST_FIXTURE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')


def dump_output(output_directory: Union[str, Callable[[str, Callable], str]] = None,
                capture_output: bool = False,
                custom_save_output_func: Optional[Callable[[str, Any], Any]] = None,
                exclude_kw: dict = None):
    """
    Dumps output to pickle

    :param output_directory: Base directory to save. Defaults to fixture path
    :param capture_output: Whether result of function should be captured
    :param custom_save_output_func: Optional function to process output for saving. Should take a filename and value to save
    :return:
    """
    # if no output directory, set to fixture path
    if output_directory is None:
        output_directory = TEST_FIXTURE_PATH
    import pickle


    def decorate(func):
        # create directory for function output
        # if we have a function for directory naming, call it
        if callable(output_directory):
            out = output_directory(TEST_FIXTURE_PATH, func)
        else:
            out = os.path.abspath(os.path.join(output_directory, func.__name__))

        # create our paths to input/output files
        out_directory = os.path.join(out, 'output')
        input_directory = os.path.join(out, 'input')
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_time = int(round(time.time() * 1000))
            # if output directory is a
            # save keywords and args to files
            for name, a in [('args', args), ('kwargs', kwargs)]:
                if len(a):
                    os.makedirs(input_directory, exist_ok=True)
                    input_file_out = os.path.join(input_directory, f'{call_time}_{name}.pkl')
                    if custom_save_output_func:
                        custom_save_output_func(input_file_out, args)
                    else:
                        default_fixture_pickle_save(input_file_out, args)
            result = func(*args, **kwargs)
            if capture_output:
                os.makedirs(out_directory, exist_ok=True)
                output_file_out = os.path.join(out_directory, f'{call_time}.pkl')
                if custom_save_output_func:
                    custom_save_output_func(output_file_out, result)
                else:
                    default_fixture_pickle_save(output_file_out, result)
            return result

        def default_fixture_pickle_save(filename, args):
            with open(filename, 'bw') as o:
                pickle.dump(args, o)

        return wrapper
    return decorate