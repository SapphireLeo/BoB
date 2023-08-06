import random
import timeit
import tracemalloc


# 세 개의 파일을 새롭게 만들고, 100만개의 정수를 각각 정방향, 역방향, 무작위로 생성하는 함수입니다.
def file_creation():
    # 세 개의 파일을 엽니다.
    ascending_numbers_file = open('./ascending.txt', 'w')
    descending_numbers_file = open('./descending.txt', 'w')
    randomized_numbers_file = open('./randomized.txt', 'w')

    # 정수를 각각 정방향, 역방향, 무작위로 생성하고 저장합니다.
    for inc, dec in zip(range(0, 10 ** 6), range(10 ** 6 - 1, -1, -1)):
        ascending_numbers_file.write(str(inc) + '\n')
        descending_numbers_file.write(str(dec) + '\n')
        randomized_numbers_file.write(str(random.randrange(0, 10 ** 6)) + '\n')
        # 파일 저장의 진행 상황을 10%마다 출력합니다.
        if inc % (10 ** 5) == 0:
            print(f'writing file...({int(inc / (10 ** 5)): 3d}%)', end='\r')

    # 파일 작성이 완료되었음을 출력하고 파일을 닫습니다.
    print(f'writing file...(100%)')
    ascending_numbers_file.close()
    descending_numbers_file.close()
    randomized_numbers_file.close()


# 파일을 열고 그 파일 객체를 반환하는 함수입니다.
def file_open():
    ascending_numbers_file = open('./ascending.txt', 'r')
    descending_numbers_file = open('./descending.txt', 'r')
    randomized_numbers_file = open('./randomized.txt', 'r')
    return ascending_numbers_file, descending_numbers_file, randomized_numbers_file


# 퀵 정렬을 수행하는 함수입니다. 제자리 정렬로 구현되어 있으며, 배열을 반환하지 않고 참조해서 직접 바꿉니다.
def quick_sort(array):
    # 입력받은 객체 리스트의 형태가 아닐 경우 예외를 호출합니다.
    if not isinstance(array, list):
        raise TypeError('sorting array must be type of python list, got', type(array), array)

    # 정렬이 필요한 영역의 처음과 끝 인덱스를 저장하는 스택을 선언합니다. 이 스택의 크기가 0이 된다면 정렬이 끝난 것입니다.
    sort_stack = [(0, len(array) - 1)]

    while True:
        # 정렬 스택에 남아 있는 것이 더 없는지 검사하고, 만약 없다면 정렬을 종료합니다.
        if len(sort_stack) < 1:
            break

        # 정렬 스택이 아직 남아 있다면 현재 정렬을 수행해야 할 영역을 불러옵니다.
        beginning, end = sort_stack.pop()

        # 현재 정렬할 영역의 크기가 2보다 작다면 정렬할 필요가 없으므로 다음 정렬 영역으로 넘어갑니다.
        if beginning + 1 > end:
            pass
        # 현재 정렬할 영역의 크기가 정확히 2라면 두 원소를 비교하여 바꾸고 정렬을 종료합니다.
        elif beginning + 1 == end:
            if array[beginning] > array[end]:
                array[beginning], array[end] = array[end], array[beginning]

        # 현재 정렬할 영역의 크기가 2보다 크다면, 퀵 정렬 알고리즘을 수행합니다.
        else:
            # 기준점(pivot)을 영역의 끝으로 정합니다.
            pivot = end
            # 정렬 과정에서 기준점과의 대소를 비교할 좌측 주시점과 우측 주시점을 설정합니다.
            left, right = beginning, end - 1

            # 기준점을 기준으로 값을 양쪽으로 분류합니다.
            while True:
                # 좌측에서 기준점보다 큰 값이 발견될 때까지 좌측 주시점을 우측으로 이동합니다.
                while array[left] <= array[pivot] and left < pivot:
                    left += 1
                # 우측에서 기준점보다 작은 값이 발견될 때까지 우측 주시점을 좌측으로 이동합니다.
                while array[right] >= array[pivot] and right > beginning:
                    right -= 1

                # 만약 이동 결과 두 주시점의 위치가 겹쳤다면, 이미 기준점 양쪽 값의 분류가 끝난 것이므로 다음 단계로 진행합니다.
                if left >= right:
                    break
                # 두 주시점이 아직 만나지 않았을 경우, 배치가 끝나지 않았으므로 두 값을 바꾸고 다시 반복합니다.
                else:
                    array[left], array[right] = array[right], array[left]

            # 위의 분류 반복문에서는, 왼쪽 주시점의 이동 반복문이 오른쪽 주시점의 이동보다 항상 우선하기 때문에
            # 왼쪽 주시점이 기준점보다 큰 값에 도달한 다음 오른쪽 주시점이 그곳에 겹쳐서 분류가 끝나게 됩니다.
            # 즉, 현재 전체 배열에서 기준점은 오른쪽에 위치하고 있기 때문에, 왼쪽 주시점(기준점보다 큰 값)과 서로 교환하여야 정렬이 완료됩니다.
            array[left], array[pivot] = array[pivot], array[left]

            # 현재 기준점의 오른쪽과 왼쪽 영역을, 정렬이 필요한 영역에 차례로 추가합니다.
            sort_stack.append((left + 1, end))
            sort_stack.append((beginning, left - 1))


# 문자열의 끝의 개행 문자를 제거하고 정수로 변환해 주는 함수입니다.
def convert(strings):
    return int(strings.strip())


# 먼저 파일 열기를 시도하고, 해당하는 파일이 없을 경우 새로운 파일을 생성해서 엽니다.
try:
    ascendingNumbersFile, descendingNumbersFile, randomizedNumbersFile = file_open()
    print('files are opened!')
except FileNotFoundError:
    print('there is not enough file of numbers for sorting. now creating them...')
    file_creation()
    print('files are created!')
    ascendingNumbersFile = open('./ascending.txt', 'r')
    descendingNumbersFile = open('./descending.txt', 'r')
    randomizedNumbersFile = open('./randomized.txt', 'r')

# 파일을 읽어들인 다음 파일로 저장되어 있는 정수들을 리스트로 저장합니다.
ascending = list(map(convert, ascendingNumbersFile.readlines()))
descending = list(map(convert, descendingNumbersFile.readlines()))
randomized = list(map(convert, randomizedNumbersFile.readlines()))

# 파일을 모두 닫습니다.
ascendingNumbersFile.close()
descendingNumbersFile.close()
randomizedNumbersFile.close()

# 정방향 배열과 역방향 배열을 퀵 정렬로 정렬합니다. 현재는 시간복잡도 문제로 이 부분을 비활성화한 상태입니다.
if False:
    print('정방향 배열을 정렬 중입니다...')
    timeConsumed = timeit.timeit('quick_sort(ascending)', globals=globals(), number=1)
    print('정방향 배열의 정렬이 완료되었습니다. (정렬 시간:', timeConsumed, ')')

    print('역방향 배열을 정렬 중입니다...')
    timeConsumed = timeit.timeit('quick_sort(descending)', globals=globals(), number=1)
    print('역방향 배열의 정렬이 완료되었습니다. (정렬 시간:', timeConsumed, ')')

# 무작위 배열을 퀵 정렬로 정렬합니다. timeit 모듈을 사용하여 실험적 시간복잡도를 측정합니다.
print('무작위 배열을 정렬 중입니다...')
timeConsumed = timeit.timeit('quick_sort(randomized)', globals=globals(), number=1)

# 메모리 할당과 사용을 추적합니다.
tracemalloc.start()
quick_sort(randomized)
# 추적 결과 현재 메모리 할당량과, 추적 과정에서 측정된 최대 메모리 할당량을 저장합니다.
current, peak = tracemalloc.get_traced_memory()
# 메모리 할당 추적을 종료합니다.
tracemalloc.stop()
# 종료 결과를 출력합니다.
print('무작위 배열의 정렬이 완료되었습니다.')
print('정렬 시간:', timeConsumed)
print('사용된 메모리:', peak - current)

# 정렬된 배열을 저장하기 위한 새로운 파일을 엽니다.
ascendingSortedFile = open('./ascending(sorted).txt', 'w')
descendingSortedFile = open('./descending(sorted).txt', 'w')
randomizedSortedFile = open('./randomized(sorted).txt', 'w')

# 열린 파일에 세 개의 배열을 각각 저장합니다.
for i, (num1, num2, num3) in enumerate(zip(ascending, descending, randomized)):
    ascendingSortedFile.write(str(num1) + '\n')
    descendingSortedFile.write(str(num2) + '\n')
    randomizedSortedFile.write(str(num3) + '\n')
    # 파일 저장의 진행 상황을 10%마다 출력합니다.
    if i % (10 ** 5) == 0:
        print(f'writing sorted file...({int(i / (10 ** 5)): 3d}%)', end='\r')

# 저장이 완료되었음을 출력하고 모든 파일을 닫습니다.
print(f'writing sorted file...(100%)')
ascendingSortedFile.close()
descendingSortedFile.close()
randomizedSortedFile.close()
