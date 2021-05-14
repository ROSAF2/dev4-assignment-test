def myDecorator(fn):
    from datetime import datetime
    import functools  
    @functools.wraps(fn)
    def wrapper(*args,**kwargs):
        with open('.logfile.txt','a+') as f:
            try:
                f.write(f'Function: {fn.__name__}\n')
                f.write(f'run at: {datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}\n')
                f.write(f'arguments: {args} and {kwargs}\n')
                f.write(f'returned value: {fn(*args,**kwargs)}\n')
            # Any exceptions raised must be propagated upstream
            except Exception as e: 
                f.write(f'exception: {e}\n')
            else:
                f.write('exception: None\n')
            finally:
                f.write('-'*50 + '\n')
        return fn(*args,**kwargs)
    return wrapper

@myDecorator
def divideIntegers(numerator, denominator):
    """ This function divides two numbers and returns an integer """
    return numerator // denominator

def main():
    print(divideIntegers(306,6))
    # print(divideIntegers(100,0)) # try the exception


if __name__ == '__main__':
    main()
