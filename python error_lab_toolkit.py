import sys

# ---------------- Parity ----------------
def parity_encode(data: str, parity: str = "even") -> str:
    if not set(data) <= {"0", "1"}:
        raise ValueError("Data must be binary.")
    ones = data.count("1")
    if parity == "even":
        bit = "0" if ones % 2 == 0 else "1"
    else:
        bit = "1" if ones % 2 == 0 else "0"
    return data + bit

def parity_check(code: str, parity: str = "even") -> bool:
    ones = code.count("1")
    if parity == "even":
        return ones % 2 == 0
    return ones % 2 == 1

# ---------------- Checksum (16-bit words) ----------------
def checksum_16(words):
    # words: list of 16-bit binary strings
    s = 0
    for w in words:
        if len(w) != 16 or not set(w) <= {"0", "1"}:
            raise ValueError("Each word must be 16-bit binary.")
        s += int(w, 2)
    # wrap-around
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    # one's complement
    s = ~s & 0xFFFF
    return format(s, "016b")

def checksum_verify(words, received_checksum):
    s = 0
    for w in words:
        s += int(w, 2)
    s += int(received_checksum, 2)
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (s & 0xFFFF) == 0xFFFF  # sum should be all 1s

# ---------------- CRC ----------------
def xor(a, b):
    return "".join("0" if i == j else "1" for i, j in zip(a, b))

def crc_remainder(data, divisor):
    pick = len(divisor)
    tmp = data[:pick]
    while pick < len(data):
        if tmp[0] == "1":
            tmp = xor(divisor, tmp) + data[pick]
        else:
            tmp = xor("0"*pick, tmp) + data[pick]
        pick += 1
    if tmp[0] == "1":
        tmp = xor(divisor, tmp)
    else:
        tmp = xor("0"*pick, tmp)
    return tmp

def crc_transmit(data_bits, generator):
    r = crc_remainder(data_bits + "0"*(len(generator)-1), generator)
    return data_bits + r, r

def crc_verify(received_bits, generator):
    r = crc_remainder(received_bits, generator)
    # "no error detected" if remainder is all zeros
    return set(r) == {"0"}, r

# ---------------- Hamming (7,4) ----------------
def hamming_74_encode(data4):
    if len(data4) != 4 or not set(data4) <= {"0", "1"}:
        raise ValueError("Provide 4-bit binary data (e.g., 1011).")
    d = list(map(int, data4))
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    code = f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"
    return code

def hamming_74_decode(code7):
    if len(code7) != 7 or not set(code7) <= {"0", "1"}:
        raise ValueError("Provide 7-bit binary code.")
    c = list(map(int, code7))
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]
    pos = s1*1 + s2*2 + s3*4
    if pos != 0:
        c[pos-1] ^= 1  # correct
    return "".join(map(str, c)), pos

# ---------------- Utils ----------------
def flip_bit(s, index):
    if index < 0 or index >= len(s):
        raise IndexError("Index out of range.")
    lst = list(s)
    lst[index] = "1" if lst[index] == "0" else "0"
    return "".join(lst)

def print_line():
    print("-"*60)

def demo_all():
    print_line()
    print("PARITY (even) demo")
    data = "1011001"
    code = parity_encode(data, "even")
    print(f"Data: {data}  -> Encoded: {code}")
    rx = flip_bit(code, 2)
    print(f"Received (bit 2 flipped): {rx}")
    print("Error detected?" , "YES" if not parity_check(rx, "even") else "NO")
    print_line()

    print("CHECKSUM (16-bit) demo")
    words = ["1010101010101010", "1100110011001100"]
    csum = checksum_16(words)
    print(f"Words: {words}")
    print(f"Checksum: {csum}")
    # induce error in first word
    rx_words = [flip_bit(words[0], 3), words[1]]
    ok = checksum_verify(rx_words, csum)
    print(f"After error: {rx_words}, verify -> {'OK (no error detected)' if ok else 'ERROR DETECTED'}")
    print_line()

    print("CRC demo (generator 1011)")
    d = "1101011011"
    g = "1011"
    frame, rem = crc_transmit(d, g)
    print(f"Data: {d}, Generator: {g}, Remainder: {rem}")
    print(f"Transmitted frame: {frame}")
    rx = flip_bit(frame, 5)
    ok, r = crc_verify(rx, g)
    print(f"Received (bit 5 flipped): {rx}, remainder: {r}, -> {'NO ERROR DETECTED' if ok else 'ERROR DETECTED'}")
    print_line()

    print("HAMMING (7,4) demo")
    d4 = "1011"
    code7 = hamming_74_encode(d4)
    print(f"Data: {d4}  -> Encoded: {code7}")
    rx = flip_bit(code7, 2)
    fixed, pos = hamming_74_decode(rx)
    print(f"Received (bit 2 flipped): {rx}  -> Corrected: {fixed}, Error position: {pos if pos else 'None'}")
    print_line()

def main():
    print("\nError Detection & Correction Toolkit")
    print_line()
    print("1) Parity (even/odd)")
    print("2) Checksum (16-bit words)")
    print("3) CRC")
    print("4) Hamming (7,4)")
    print("5) Demo all (quick showcase)")
    print("0) Exit")
    print_line()

    choice = input("Choose an option: ").strip()
    if choice == "1":
        data = input("Enter binary data (e.g., 1011001): ").strip()
        parity = input("Parity type [even/odd] (default=even): ").strip().lower() or "even"
        code = parity_encode(data, parity)
        print(f"Encoded: {code}")
        if input("Flip a bit? [y/N]: ").strip().lower() == "y":
            idx = int(input(f"Enter index 0..{len(code)-1}: "))
            rx = flip_bit(code, idx)
        else:
            rx = code
        ok = parity_check(rx, parity)
        print(f"Received: {rx}  -> {'OK (no error detected)' if ok else 'ERROR DETECTED'}")

    elif choice == "2":
        print("Enter two 16-bit words (binary). Press Enter for defaults.")
        w1 = input("Word 1 [default 1010101010101010]: ").strip() or "1010101010101010"
        w2 = input("Word 2 [default 1100110011001100]: ").strip() or "1100110011001100"
        csum = checksum_16([w1, w2])
        print(f"Checksum: {csum}")
        if input("Induce an error in Word 1? [y/N]: ").strip().lower() == "y":
            idx = int(input("Bit index to flip (0..15): "))
            w1 = flip_bit(w1, idx)
        ok = checksum_verify([w1, w2], csum)
        print(f"Verify -> {'OK (no error detected)' if ok else 'ERROR DETECTED'}")

    elif choice == "3":
        d = input("Enter data bits (e.g., 1101011011) [Enter for default]: ").strip() or "1101011011"
        g = input("Enter generator (e.g., 1011) [Enter for default]: ").strip() or "1011"
        frame, rem = crc_transmit(d, g)
        print(f"Transmitted frame: {frame} (remainder {rem})")
        if input("Flip a bit in the frame? [y/N]: ").strip().lower() == "y":
            idx = int(input(f"Bit index to flip (0..{len(frame)-1}): "))
            rx = flip_bit(frame, idx)
        else:
            rx = frame
        ok, r = crc_verify(rx, g)
        print(f"Received: {rx}  -> remainder {r} -> {'OK (no error detected)' if ok else 'ERROR DETECTED'}")

    elif choice == "4":
        d4 = input("Enter 4-bit data (e.g., 1011) [Enter for default]: ").strip() or "1011"
        code7 = hamming_74_encode(d4)
        print(f"Encoded: {code7}")
        if input("Flip a bit? [y/N]: ").strip().lower() == "y":
            idx = int(input(f"Bit index to flip (0..{len(code7)-1}): "))
            rx = flip_bit(code7, idx)
        else:
            rx = code7
        fixed, pos = hamming_74_decode(rx)
        print(f"Received: {rx} -> Corrected: {fixed}, Error position: {pos if pos else 'None'}")

    elif choice == "5":
        demo_all()
    else:
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
