import time 

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start

        # Converti a ore minuti e seconfi
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = elapsed % 60

        print(f'Tempo impiegato: {hours:02d}:{minutes:02d}:{seconds:.6f}')
        return result
    return wrapper