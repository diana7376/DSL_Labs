import random

def repeat(symbols, times):
    return ''.join(random.choice(symbols) for _ in range(times))

def bounded_repeat(symbols, min_count, max_count):
    count = random.randint(min_count, max_count)
    return repeat(symbols, count), count

def generate_with_steps():
    steps = []
    result = ""

    # M?
    m_char = random.choice(['', 'M'])
    result += m_char
    steps.append(f"Added 'M' {'once' if m_char else '0 times'}")

    # N{2}
    result += 'NN'
    steps.append("Added 'N' exactly 2 times")

    # (O|P){3}
    op_part = repeat(['O', 'P'], 3)
    result += op_part
    steps.append(f"Added 3 characters from (O|P): '{op_part}'")

    # O*
    o_part, o_count = bounded_repeat(['O'], 0, 5)
    result += o_part
    steps.append(f"Added 'O' {o_count} times for O*")

    # R+
    r_part, r_count = bounded_repeat(['R'], 1, 5)
    result += r_part
    steps.append(f"Added 'R' {r_count} times for R+")

    # (X|Y|Z){3}
    xyz_part = repeat(['X', 'Y', 'Z'], 3)
    result += xyz_part
    steps.append(f"Added 3 characters from (X|Y|Z): '{xyz_part}'")

    # 8+
    eight_part, eight_count = bounded_repeat(['8'], 1, 5)
    result += eight_part
    steps.append(f"Added '8' {eight_count} times for 8+")

    # (9|O){2}
    nine_o_part = repeat(['9', 'O'], 2)
    result += nine_o_part
    steps.append(f"Added 2 characters from (9|O): '{nine_o_part}'")

    # (H|I)
    hi_char = random.choice(['H', 'I'])
    result += hi_char
    steps.append(f"Added one character from (H|I): '{hi_char}'")

    # (J|K)
    jk_char = random.choice(['J', 'K'])
    result += jk_char
    steps.append(f"Added one character from (J|K): '{jk_char}'")

    # L*
    l_part, l_count = bounded_repeat(['L'], 0, 5)
    result += l_part
    steps.append(f"Added 'L' {l_count} times for L*")

    # N?
    n_char = random.choice(['', 'N'])
    result += n_char
    steps.append(f"Added 'N' {'once' if n_char else '0 times'} for N?")

    return result, steps
