class ChiaUtils:

    @staticmethod
    def size_in_bytes(size: str) -> int:

        res = size.split()
        power = 3

        if res[1] == "GiB":
            power = 3
        elif res[1] == "TiB":
            power = 4
        elif res[1] == "PiB":
            power = 5
        elif res[1] == "EiB":
            power = 6
        elif res[1] == "ZiB":
            power = 7

        clean: str = res[0].replace('.', '')
        return int(clean) * pow(1024, power)

    @staticmethod
    def size_in_gbytes(size: str) -> int:

        size_in_bytes = ChiaUtils.size_in_bytes(size)
        size_in_gbytes = size_in_bytes / pow(1024, 3)
        return round(size_in_gbytes)
