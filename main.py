from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

# Функція для обчислення кроків гіпотези Коллатца для одного числа
def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

# Функція для обробки чисел у потоці
def process_numbers(start, end, result_queue):
    for number in range(start, end):
        steps = collatz_steps(number)
        result_queue.put(steps)

# Основна функція для паралельного обчислення
def parallel_collatz_calculation(max_number=10_000_000, num_threads=4):

    # Черга
    result_queue = Queue()
    
    # Розділяємо діапазон чисел між потоками
    chunk_size = max_number // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size + 1
            end = (i + 1) * chunk_size + 1 if i < num_threads - 1 else max_number + 1
            futures.append(executor.submit(process_numbers, start, end, result_queue))

        for future in as_completed(futures):
            future.result()

    # Підрахунок середньої кількості кроків
    total_steps = 0
    count = 0
    while not result_queue.empty():
        total_steps += result_queue.get()
        count += 1

    # Вивід результатів
    avg_steps = total_steps / count if count > 0 else 0
    print(f"Середня кількість кроків для гіпотези Коллатца: {avg_steps:.2f}")


parallel_collatz_calculation(num_threads=10)