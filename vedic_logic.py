from dataclasses import dataclass
from typing import List, Union

@dataclass
class VedicStep:
    explanation: str
    calculation: str
    result: Union[int, str, List[int]]

class VedicEngine:
    def __init__(self):
        self.steps: List[VedicStep] = []

    def clear_steps(self):
        self.steps = []

    def get_report(self) -> List[dict]:
        return [{"explanation": s.explanation, "calculation": s.calculation, "result": str(s.result)} for s in self.steps]

    # --- 1. GENERAL SQUARING (Duplex Method / Yavadunam) ---
    # Works for ANY number: 67, 104, 998, etc.
    def square_any(self, n: int):
        self.clear_steps()
        if n < 0: return None
        
        self.steps.append(VedicStep(
            explanation=f"Calculating {n}² using the Vedic 'Duplex Method' (Dwandwa Yoga).",
            calculation=f"Input: {n}",
            result=None
        ))

        s = str(n)
        digits = [int(d) for d in s]
        L = len(digits)
        
        # Calculate Duplex values for each position
        duplex_values = []
        for i in range(L):
            left_idx = i
            right_idx = L - 1 - i
            
            if left_idx == right_idx:
                val = digits[left_idx] ** 2
                duplex_values.append(val)
            elif left_idx < right_idx:
                val = 2 * digits[left_idx] * digits[right_idx]
                duplex_values.append(val)
        
        self.steps.append(VedicStep(
            explanation="Step 1: Calculate the 'Duplex' (D) for each symmetric position.",
            calculation=f"Digits: {digits} → Duplex Sequence: {duplex_values}",
            result=duplex_values
        ))

        # Process carries from right to left
        final_digits = []
        carry = 0
        duplex_values.reverse() 
        
        for i, val in enumerate(duplex_values):
            total = val + carry
            digit = total % 10
            carry = total // 10
            final_digits.append(digit)
            self.steps.append(VedicStep(
                explanation=f"Step {i+2}: Process position (Right-to-Left). Add carry to {val}.",
                calculation=f"{val} + {carry if i > 0 else 0} = {total} → Write {digit}, Carry {total // 10}",
                result=f"Digit: {digit}, Carry: {total // 10}"
            ))
            carry = total // 10

        while carry > 0:
            digit = carry % 10
            carry = carry // 10
            final_digits.append(digit)
            self.steps.append(VedicStep(
                explanation="Handling remaining carry.",
                calculation=f"Remaining carry: {digit}",
                result=digit
            ))

        final_digits.reverse()
        final_val = int("".join(map(str, final_digits)))

        self.steps.append(VedicStep(
            explanation="Final Result: Combine the digits.",
            calculation=f"{''.join(map(str, final_digits))}",
            result=final_val
        ))
        return final_val

    # --- 2. GENERAL MULTIPLICATION (Urdhva-Tiryagbhyam) ---
    # Works for ANY two numbers: 94*62, 123*456
    def multiply_any(self, a: int, b: int):
        self.clear_steps()
        s_a, s_b = str(a), str(b)
        digits_a = [int(x) for x in s_a]
        digits_b = [int(x) for x in s_b]
        
        len_a, len_b = len(digits_a), len(digits_b)
        total_digits = len_a + len_b
        result_parts = [0] * total_digits

        self.steps.append(VedicStep(
            explanation=f"Calculating {a} × {b} using 'Urdhva-Tiryagbhyam' (Vertically and Crosswise).",
            calculation=f"Numbers: {a}, {b}",
            result=None
        ))

        # Cross multiplication logic (Right to Left)
        rev_a = digits_a[::-1]
        rev_b = digits_b[::-1]
        
        for k in range(total_digits - 1, -1, -1):
            sum_val = 0
            pairs = []
            current_pos = (total_digits - 1) - k 
            
            for i in range(len(rev_a)):
                j = current_pos - i
                if 0 <= j < len(rev_b):
                    sum_val += rev_a[i] * rev_b[j]
                    pairs.append(f"{rev_a[i]}×{rev_b[j]}")

            result_parts[k] = sum_val
            if pairs:
                self.steps.append(VedicStep(
                    explanation=f"Position {current_pos} ({10**current_pos}s place): Sum of cross products.",
                    calculation=f"{' + '.join(pairs)} = {sum_val}",
                    result=sum_val
                ))

        # Handle carries
        self.steps.append(VedicStep(
            explanation="Resolve carries from right to left.",
            calculation=f"Raw values: {result_parts}",
            result=None
        ))

        carry = 0
        final_digits = []
        for i in range(len(result_parts) - 1, -1, -1):
            total = result_parts[i] + carry
            digit = total % 10
            carry = total // 10
            final_digits.append(digit)
            if i > 0 or carry == 0:
                 self.steps.append(VedicStep(
                    explanation=f"Resolve position: {total} → Keep {digit}, Carry {carry}",
                    calculation=f"{result_parts[i]} + {carry if i != len(result_parts)-1 else 0} = {total}",
                    result=digit
                ))
        
        while carry > 0:
            final_digits.append(carry % 10)
            carry //= 10

        final_digits.reverse()
        while len(final_digits) > 1 and final_digits[0] == 0:
            final_digits.pop(0)
            
        final_val = int("".join(map(str, final_digits)))
        
        self.steps.append(VedicStep(
            explanation="Final Answer constructed.",
            calculation=f"Result: {final_val}",
            result=final_val
        ))
        return final_val

    # --- 3. ADDITION ---
    def add_any(self, numbers: List[int]):
        self.clear_steps()
        self.steps.append(VedicStep(
            explanation=f"Adding {numbers} using column addition logic.",
            calculation=f"Sum: {' + '.join(map(str, numbers))}",
            result=None
        ))
        total = sum(numbers)
        self.steps.append(VedicStep(
            explanation="Final Sum.",
            calculation=f"Total = {total}",
            result=total
        ))
        return total

class VedicCalculator:
    def __init__(self):
        self.engine = VedicEngine()
        self.steps = []

    def clear_steps(self):
        self.steps = []
        self.engine.clear_steps()

    def get_explanation_report(self) -> List[dict]:
        return self.engine.get_report()

    def calculate(self, operation: str, input_str: str):
        self.clear_steps()
        try:
            if operation == 'square':
                n = int(input_str)
                res = self.engine.square_any(n)
                self.steps = self.engine.steps
                return res
            elif operation == 'multiply':
                parts = [int(x) for x in input_str.replace(' ', '').split(',')]
                if len(parts) != 2: raise ValueError("Enter two numbers separated by comma.")
                res = self.engine.multiply_any(parts[0], parts[1])
                self.steps = self.engine.steps
                return res
            elif operation == 'add':
                parts = [int(x) for x in input_str.replace(' ', '').split(',')]
                res = self.engine.add_any(parts)
                self.steps = self.engine.steps
                return res
            else:
                raise ValueError("Unknown operation")
        except Exception as e:
            self.steps.append(VedicStep("Error", str(e), None))
            self.steps = self.engine.steps
            return None   