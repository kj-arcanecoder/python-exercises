def means(*nums):
    if not nums:
        return 0
    int_nums = list(int(item) for item in nums)
    return sum(int_nums) / len(nums)