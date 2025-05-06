import pygame
import random
import math

pygame.init()

class drawInformation:
    BLACK = 0,0,0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BLUE = 187, 241, 241
    BACKGROUND_COLOR = 254, 132, 132

    GRADIENTS = [
        (83, 0, 0),
        (107, 0, 0),
        (186, 0, 0)
    ]
    FONT = pygame.font.SysFont('comicsans', 18)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150


    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD // 2

def generateStartingList(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | Space - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | H - Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    sorting2 = draw_info.FONT.render(
        "S - Shell Sort | X - Radix Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting2, (draw_info.width / 2 - sorting2.get_width() / 2, 105))

    drawList(draw_info)
    pygame.display.update()

def drawList(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        # Clear the entire sorting area
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                     draw_info.width - draw_info.SIDE_PAD,
                     draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Draw all bars
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height - y))

    if clear_bg:
        pygame.display.update()

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]

                drawList(draw_info, {j: draw_info.BLUE, j + 1: draw_info.GREY}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			drawList(draw_info, {i - 1: draw_info.BLUE, i: draw_info.GREY}, True)
			yield True

	return lst


def heapify(lst, n, i, draw_info, ascending):
    largest_smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        if (ascending and lst[left] > lst[largest_smallest]) or (not ascending and lst[left] < lst[largest_smallest]):
            largest_smallest = left

    if right < n:
        if (ascending and lst[right] > lst[largest_smallest]) or (not ascending and lst[right] < lst[largest_smallest]):
            largest_smallest = right

    if largest_smallest != i:
        lst[i], lst[largest_smallest] = lst[largest_smallest], lst[i]
        drawList(draw_info, {i: draw_info.BLUE, largest_smallest: draw_info.RED}, True)
        yield True
        yield from heapify(lst, n, largest_smallest, draw_info, ascending)

def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    # Build heap (Max-Heap or Min-Heap based on sorting order)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(lst, n, i, draw_info, ascending)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        drawList(draw_info, {0: draw_info.BLUE, i: draw_info.RED}, True)
        yield True
        yield from heapify(lst, i, 0, draw_info, ascending)

    return lst



def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    gap = n // 2

    # Start with a big gap, then reduce the gap
    while gap > 0:
        # Do a gapped insertion sort
        for i in range(gap, n):
            # Store current value
            temp = lst[i]
            j = i

            # Shift earlier gap-sorted elements up until the correct location
            while j >= gap and ((lst[j - gap] > temp and ascending) or (lst[j - gap] < temp and not ascending)):
                lst[j] = lst[j - gap]
                drawList(draw_info, {j: draw_info.BLUE, j - gap: draw_info.RED}, True)
                yield True
                j -= gap

            # Put temp (the original lst[i]) in its correct location
            lst[j] = temp
            drawList(draw_info, {j: draw_info.BLUE}, True)
            yield True

        # Reduce the gap for the next iteration
        gap = gap // 2

    return lst


def counting_sort(draw_info, exp, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    output = [0] * n
    count = [0] * 10

    # Count occurrences of each digit
    for i in range(n):
        index = (lst[i] // exp) % 10
        count[index] += 1
        drawList(draw_info, {i: draw_info.BLUE}, True)
        yield True

    # Update count[i] to store position in output array
    if ascending:
        for i in range(1, 10):
            count[i] += count[i - 1]
    else:
        for i in range(8, -1, -1):
            count[i] += count[i + 1]

    # Build the output array
    for i in range(n - 1, -1, -1):
        index = (lst[i] // exp) % 10
        output[count[index] - 1] = lst[i]
        count[index] -= 1
        drawList(draw_info, {i: draw_info.RED}, True)
        yield True

    # Copy output back to original list
    for i in range(n):
        lst[i] = output[i]
        drawList(draw_info, {i: draw_info.BLUE}, True)
        yield True



def radix_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Find the maximum number to know number of digits
    max_val = max(lst)

    # Do counting sort for every digit
    exp = 1
    while max_val // exp > 0:
        yield from counting_sort(draw_info, exp, ascending)
        exp *= 10

    return lst


def partition(lst, low, high, draw_info, ascending):
    pivot = lst[high]
    i = low - 1

    for j in range(low, high):
        if (ascending and lst[j] <= pivot) or (not ascending and lst[j] >= pivot):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            drawList(draw_info, {i: draw_info.BLUE, j: draw_info.RED, high: draw_info.BLUE}, True)
            yield True

    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    drawList(draw_info, {i + 1: draw_info.BLUE, high: draw_info.RED}, True)
    yield True

    return i + 1


def quick_sort_helper(lst, low, high, draw_info, ascending):
    if low < high:
        # Find pivot element such that elements smaller than pivot are on the left
        # and elements greater than pivot are on the right
        pivot_idx = yield from partition(lst, low, high, draw_info, ascending)

        # Recursively sort elements before and after pivot
        yield from quick_sort_helper(lst, low, pivot_idx - 1, draw_info, ascending)
        yield from quick_sort_helper(lst, pivot_idx + 1, high, draw_info, ascending)


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    yield from quick_sort_helper(lst, 0, len(lst) - 1, draw_info, ascending)
    return lst

def main():
    run = True
    sorting = False
    ascending = True

    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generateStartingList(n, min_val, max_val)

    draw_info = drawInformation(800, 600, lst)

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generateStartingList(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = shell_sort
                sorting_algo_name = "Shell Sort"

            elif event.key == pygame.K_x and not sorting:
                sorting_algorithm = radix_sort
                sorting_algo_name = "Radix Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"

    pygame.quit()

if __name__ == "__main__":
    main()