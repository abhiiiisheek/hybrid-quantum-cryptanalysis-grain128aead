def swapsb(n):
    val = 0
    for i in range(8):
        val |= ((n >> i) & 1) << (7 - i)
    return val


def byte_to_bits_msb(b):
    return [(b >> (7 - i)) & 1 for i in range(8)]


def bits_to_byte_msb(bits):
    v = 0
    for i in range(8):
        v |= bits[i] << (7 - i)
    return v


def encode_der(length):
    if length < 128:
        return [swapsb(length)]
    out = []
    tmp = length
    while tmp > 0:
        out.append(swapsb(tmp & 0xff))
        tmp >>= 8
    out.reverse()
    return [swapsb(0x80 | len(out))] + out




class Grain128AEADv2:
    INIT = 0
    ADDKEY = 1
    NORMAL = 2

    def __init__(self, key, nonce):
        self.round = self.INIT

        self.lfsr = [0] * 128
        self.nfsr = [0] * 128
        self.auth_acc = [0] * 64
        self.auth_sr = [0] * 64

        key = bytes(swapsb(x) for x in key)
        nonce = bytes(swapsb(x) for x in nonce)

        key_bits = []
        iv_bits = []

        for b in key:
            key_bits += byte_to_bits_msb(b)
        for b in nonce:
            iv_bits += byte_to_bits_msb(b)


        for i in range(96):
            self.lfsr[i] = iv_bits[i]
        for i in range(96, 127):
            self.lfsr[i] = 1
        self.lfsr[127] = 0


        for i in range(128):
            self.nfsr[i] = key_bits[i]


        for _ in range(320):
            self.next_z(0, 0)


        self.round = self.ADDKEY
        for i in range(64):
            self.next_z(key_bits[i], key_bits[64 + i])


        self.round = self.NORMAL
        for i in range(64):
            self.auth_acc[i] = self.next_z(0, 0)
        for i in range(64):
            self.auth_sr[i] = self.next_z(0, 0)



    def next_lfsr_fb(self):
        s = self.lfsr
        return s[96] ^ s[81] ^ s[70] ^ s[38] ^ s[7] ^ s[0]

    def next_nfsr_fb(self):
        b = self.nfsr
        return (
            b[96] ^ b[91] ^ b[56] ^ b[26] ^ b[0]
            ^ (b[84] & b[68])
            ^ (b[67] & b[3])
            ^ (b[65] & b[61])
            ^ (b[59] & b[27])
            ^ (b[48] & b[40])
            ^ (b[18] & b[17])
            ^ (b[13] & b[11])
            ^ (b[82] & b[78] & b[70])
            ^ (b[25] & b[24] & b[22])
            ^ (b[95] & b[93] & b[92] & b[88])
        )

    def next_h(self):
        b = self.nfsr
        s = self.lfsr

        x0 = b[12]
        x1 = s[8]
        x2 = s[13]
        x3 = s[20]
        x4 = b[95]
        x5 = s[42]
        x6 = s[60]
        x7 = s[79]
        x8 = s[94]

        return (x0 & x1) ^ (x2 & x3) ^ (x4 & x5) ^ (x6 & x7) ^ (x0 & x4 & x8)

    def shift(self, reg, fb):
        out = reg[0]
        for i in range(127):
            reg[i] = reg[i + 1]
        reg[127] = fb
        return out

    def auth_shift(self, fb):
        for i in range(63):
            self.auth_sr[i] = self.auth_sr[i + 1]
        self.auth_sr[63] = fb

    def accumulate(self):
        for i in range(64):
            self.auth_acc[i] ^= self.auth_sr[i]

    def next_z(self, keybit, keybit_64):
        lfsr_fb = self.next_lfsr_fb()
        nfsr_fb = self.next_nfsr_fb()
        h = self.next_h()

        A = [2, 15, 36, 45, 64, 73, 89]
        nfsr_tmp = 0
        for a in A:
            nfsr_tmp ^= self.nfsr[a]

        y = h ^ self.lfsr[93] ^ nfsr_tmp

        if self.round == self.INIT:
            lfsr_out = self.shift(self.lfsr, lfsr_fb ^ y)
            self.shift(self.nfsr, nfsr_fb ^ lfsr_out ^ y)

        elif self.round == self.ADDKEY:
            lfsr_out = self.shift(self.lfsr, lfsr_fb ^ y ^ keybit_64)
            self.shift(self.nfsr, nfsr_fb ^ lfsr_out ^ y ^ keybit)

        else:
            lfsr_out = self.shift(self.lfsr, lfsr_fb)
            self.shift(self.nfsr, nfsr_fb ^ lfsr_out)

        return y



    def encrypt(self, ad, pt):


        ad = bytes(swapsb(x) for x in ad)
        pt = bytes(swapsb(x) for x in pt)


        ader = encode_der(len(ad)) + list(ad)


        ad_cnt = 0

        for _ in range(len(ader)):
            for j in range(16):
                z = self.next_z(0, 0)

                if j % 2 == 1:
                    byte = ader[ad_cnt // 8]
                    bit  = (byte >> (7 - (ad_cnt % 8))) & 1

                    if bit == 1:
                        self.accumulate()

                    self.auth_shift(z)
                    ad_cnt += 1


        msg_bits = []
        for b in pt:
            msg_bits += byte_to_bits_msb(b)
        msg_bits.append(1)

        ct_bits = []
        m_cnt = 0
        ac_cnt = 0

        for _ in range(len(pt)):
            for j in range(16):
                z = self.next_z(0, 0)

                if j % 2 == 0:
                    ct_bits.append(msg_bits[m_cnt] ^ z)
                    m_cnt += 1
                else:
                    if msg_bits[ac_cnt] == 1:
                        self.accumulate()
                    self.auth_shift(z)
                    ac_cnt += 1


        self.next_z(0, 0)


        self.accumulate()


        ct = []
        for i in range(0, len(ct_bits), 8):
            b = bits_to_byte_msb(ct_bits[i:i+8])
            ct.append(swapsb(b))


        tag = []
        for i in range(8):
            b = bits_to_byte_msb(self.auth_acc[i*8:(i+1)*8])
            tag.append(swapsb(b))

        return bytes(ct), bytes(tag)
