from numpy import prod

def is_prime(num: int) -> bool:
    """
    :num: if number is prime
    :return: yes/no -> True/False
    """
    qtd_div = 0
    for cont in range(1, num+1):
        if num % cont == 0:
            qtd_div += 1
    if qtd_div == 2:
        return True  # num is prime
    return False


def get_prime_nums(qt_primes: int, start: int = 2, max_num: int = 0) -> list:
    """
    :param: qt_primes -> (quantity) how many prime numbers does it need?
    :param: start -> start the search from?
    :param: max_num -> max num possible to return in list
    :return: list of prime numbers
    """
    max_num = 0 if max_num is None or max_num < start else max_num
    primes = []
    # cont_while = cw
    cw = num = start
    while cw < qt_primes + start:
        if is_prime(num):
            if num > max_num and max_num > 1:
                break
            primes.append(num)
            cw += 1
        num += 1
        # print(primes)
    return primes

def get_gcd(*nums):
    """
    :nums: 
    """
    # MDC
    def same_divisor(prmn) -> bool:
        # prmn = prime_num
        if not is_prime(prmn):
            pass
        for n in nums:
            if not n % prmn == 0:
                break
        else:
            yield prmn
    resp = [r for _val in range(2, int(max(nums)/2))
            for r in same_divisor(_val)]
    # mults = map(is_prime, resp)
    mults = filter(is_prime, resp)
    mults = list(mults)

    return prod(mults)
