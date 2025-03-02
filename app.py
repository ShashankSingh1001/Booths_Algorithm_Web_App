from flask import Flask # type: ignore
import os, request, jsonify, render_template # type: ignore
from waitress import serve # type: ignore

app = Flask(__name__)

def to_twos_complement(num, bits):
    """Convert a number to its two's complement binary representation."""
    if num < 0:
        return bin((1 << bits) + num)[2:].zfill(bits)
    else:
        return bin(num)[2:].zfill(bits)

def bin_to_int(bin_str):
    """Convert a two's complement binary string to an integer."""
    n = len(bin_str)
    num = int(bin_str, 2)
    if bin_str[0] == '1':  # Negative number
        num -= (1 << n)
    return num

def booth_algorithm(m, r):
    # Determine the number of bits needed (including sign bit)
    bits_m = m.bit_length() + 1 if m != 0 else 1
    bits_r = r.bit_length() + 1 if r != 0 else 1
    n = max(bits_m, bits_r)
    
    # Convert to two's complement binary
    x = to_twos_complement(m, n)  # Multiplicand
    y = to_twos_complement(r, n)  # Multiplier

    # Initialize variables
    A = '0' * n
    Q = y
    Q_minus_1 = '0'
    steps = []

    steps.append(f"Initialization: A = {A}, Q = {Q}, Q-1 = {Q_minus_1}")

    for i in range(n):
        step_num = i + 1
        step_desc = []

        # Step 1: Check last two bits of Q and Q_minus_1
        q0 = Q[-1]
        if q0 == '1' and Q_minus_1 == '0':
            # Subtract multiplicand (A = A - M)
            A_int = bin_to_int(A)
            M_int = bin_to_int(x)
            A_int -= M_int
            A = format(A_int & ((1 << n) - 1), f'0{n}b')
            step_desc.append(f"Subtract M ({x}): A = {A}")
        elif q0 == '0' and Q_minus_1 == '1':
            # Add multiplicand (A = A + M)
            A_int = bin_to_int(A)
            M_int = bin_to_int(x)
            A_int += M_int
            A = format(A_int & ((1 << n) - 1), f'0{n}b')
            step_desc.append(f"Add M ({x}): A = {A}")

        # Step 2: Arithmetic right shift
        new_Q_minus_1 = Q[-1]
        Q = A[-1] + Q[:-1]
        A = A[0] + A[:-1]  # Preserve sign bit

        step_desc.append(f"Shift Right: A = {A}, Q = {Q}, Q-1 = {new_Q_minus_1}")
        steps.append(f"Step {step_num}: {' | '.join(step_desc)}")
        Q_minus_1 = new_Q_minus_1

    # Combine A and Q to get the final result (2n bits)
    result = A + Q
    return result, steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booth', methods=['POST'])
def booth():
    data = request.json
    m = int(data['m'])
    r = int(data['r'])
    result, steps = booth_algorithm(m, r)
    return jsonify({"result": result, "steps": steps})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000)) 
    serve(app, host="0.0.0.0", port=port)