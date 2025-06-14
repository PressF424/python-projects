def heapify(arr, n, i):
    """
    Heapify - функция для восстановления свойств max-heap.
    
    Параметры:
    arr — массив, представляющий кучу
    n — размер кучи
    i — индекс текущего узла, для которого нужно проверить/восстановить свойства кучи
    """
    largest = i           # Считаем текущий узел наибольшим
    left = 2 * i + 1       # Индекс левого потомка
    right = 2 * i + 2      # Индекс правого потомка

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    # Если наибольший элемент не текущий узел, то
    if largest != i:
        # Меняем местами
        arr[i], arr[largest] = arr[largest], arr[i]

        # И реккурсивно восстанавливаем свойства кучи для поддерева
        heapify(arr, n, largest)

def heap_sort(arr):
    """
    Основная функция сортировки массива с использованием алгоритма Heap Sort.
    
    Входные параметры:
    arr — массив, который нужно отсортировать
    """
    n = len(arr)

    # Первый шаг - построение max-heap
    # Начинаем с последнего НЕ листового узла и вызываем heapify для каждого элемента
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Второй шаг - извлечение элементов из кучи по одному
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]

        heapify(arr, i, 0)

# Вызов для проверки
if __name__ == "__main__":
    array = [4, 10, 3, 5, 1]
    print("Исходный массив:", array)
    heap_sort(array)
    print("Отсортированный массив:", array)
