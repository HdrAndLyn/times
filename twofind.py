# 二分查找法
class Two():
    def binary_search(exlist, item):
        low = 0
        high = len(exlist) - 1
        while low <= high:
            mid = int((low + high) / 2)
            if mid == item:
                return mid
            if mid < item:
                low = mid + 1
            if mid > item:
                high = mid - 1
        return None
