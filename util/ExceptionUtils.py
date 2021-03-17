import traceback

def exception_process_display(error_details):
    
    print(traceback.print_tb(error_details[2]))
    
    err_message = f'From "{error_details[1].__class__.__name__}" \
            class ({error_details[1].__doc__[:-1]}) : {error_details[1]}'

    return f"An unexpected error occured, please check Streamlit's logs\
            for more details!  \n\n{err_message}"
