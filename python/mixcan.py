from hashlib import sha1
import hmac


class MixCAN(object):

    """
    SHA-1 k=26 n=64 max-num 6bits
    """
    SHA1_LEN = 160

    def __init__(self, key, num_of_hashes=26, filter_len=64):
        self._key = key
        self._num_of_hashes = num_of_hashes
        self._filter_len = filter_len
        self._filter = [0] * filter_len
        self._count = 0

    def insert(self, data):
        tag = hmac.new(self._key, data.encode(), sha1).hexdigest()
        bins = MixCAN._hex_to_bin(tag)

        for i in range(0, MixCAN.SHA1_LEN-4, 6):
            decimal_data = int(bins[i:i+6], 2)
            self._filter[decimal_data] = 1

        self._count = self._count + 1

    def contains(self, data):
        tag = hmac.new(self._key, data.encode(), sha1).hexdigest()
        bins = MixCAN._hex_to_bin(tag)

        for i in range(0, MixCAN.SHA1_LEN - 4, 6):
            decimal_data = int(bins[i:i + 6], 2)
            if self._filter[decimal_data] != 1:
                return False

        return True

    @property
    def count(self):
        return self._count

    @property
    def filter(self):
        return self._filter

    @staticmethod
    def _hex_to_bin(hex_data):
        scale = 16
        num_of_bits = 8
        return bin(int(hex_data, scale))[2:].zfill(num_of_bits)

    def to_can(self):
        can_msg = []
        for i in range(0, 64, 8):
            bin_str = ""
            filter_chunk = self._filter[i:i+8]
            for i in filter_chunk:
                bin_str += str(i)

            hex_data = hex(int(bin_str, 2))
            can_msg.append(hex_data)

        return can_msg


if __name__ == "__main__":
    key = bytes("e179017a-62b0-4996-8a38-e91aa9f1", "UTF-8")
    mixcan = MixCAN(key)
    mixcan.insert("a")
    print(mixcan.contains("a"))
    print(mixcan.filter)
    print(str(mixcan.to_can()))
