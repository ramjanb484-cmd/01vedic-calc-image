from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class VedicStep:
    """Represents a single step in the Vedic calculation process."""
    explanation: str
    calculation: str
    result: any

class VedicCalculator:
    def __init__(self):
        self.steps: List[VedicStep] = []

    def clear_steps(self):
        self.steps = []

    def get_explanation_report(self) -> str:
        """Generates a formatted string report of the calculation steps."""
        if not self.steps:
            return "No calculation performed."
        
        report = ["--- Vedic Mathematics Explanation ---"]
        for i, step in enumerate(self.steps, 1):
            report.append(f"Step {i}: {step.explanation}")
            report.append(f"        {step.calculation}")
            if step.result is not None:
                report.append(f"        → Result: {step.result}")
        report.append("-------------------------------")
        return "\n".join(report)

    # --- Sutra 1: Ekadhikena Purvena (Squaring numbers ending in 5) ---
    # Example: 55 * 55
    def square_ending_in_5(self, n: int) -> Optional[int]:
        if not (isinstance(n, int) and n % 10 == 5):
            return None
        
        self.clear_steps()
        prefix = n // 10
        next_prefix = prefix + 1
        
        self.steps.append(VedicStep(
            explanation="Identify the number ends in 5. Separate the prefix (digits before 5).",
            calculation=f"Number: {n}, Prefix: {prefix}",
            result=None
        ))
        
        self.steps.append(VedicStep(
            explanation="Apply Sutra 'Ekadhikena Purvena': Multiply the prefix by one more than itself.",
            calculation=f"{prefix} × ({prefix} + 1) = {prefix} × {next_prefix}",
            result=prefix * next_prefix
        ))
        
        lhs = prefix * next_prefix
        self.steps.append(VedicStep(
            explanation="The right-hand side is always 25 (5 squared).",
            calculation="5² = 25",
            result=25
        ))
        
        final_res = int(f"{lhs}25")
        self.steps.append(VedicStep(
            explanation="Concatenate the Left-Hand Side (LHS) and Right-Hand Side (RHS).",
            calculation=f"LHS ({lhs}) || RHS (25) = {final_res}",
            result=final_res
        ))
        
        return final_res

    # --- Sutra 2: Urdhva-Tiryagbhyam (Vertically and Crosswise) ---
    # General multiplication, good for 94 * 62
    def multiply_general(self, a: int, b: int) -> int:
        self.clear_steps()
        str_a, str_b = str(a), str(b)
        len_a, len_b = len(str_a), len(str_b)
        
        self.steps.append(VedicStep(
            explanation="Apply 'Urdhva-Tiryagbhyam' (Vertically and Crosswise).",
            calculation=f"Multiplying {a} × {b}",
            result=None
        ))

        # Normalize lengths for logic (simple 2-digit implementation for demo clarity)
        if len_a == 2 and len_b == 2:
            a1, a0 = int(str_a[0]), int(str_a[1])
            b1, b0 = int(str_b[0]), int(str_b[1])
            
            # Step 1: Vertical (Right)
            rhs = a0 * b0
            carry = rhs // 10
            digit = rhs % 10
            self.steps.append(VedicStep(
                explanation="Multiply unit digits vertically.",
                calculation=f"{a0} × {b0} = {rhs}. Write {digit}, carry {carry}.",
                result=digit
            ))
            
            # Step 2: Crosswise
            cross = (a1 * b0) + (a0 * b1) + carry
            new_carry = cross // 10
            mid_digit = cross % 10
            self.steps.append(VedicStep(
                explanation="Cross-multiply tens and units, add previous carry.",
                calculation=f"({a1}×{b0}) + ({a0}×{b1}) + {carry} = {cross}. Write {mid_digit}, carry {new_carry}.",
                result=mid_digit
            ))
            
            # Step 3: Vertical (Left)
            lhs = (a1 * b1) + new_carry
            self.steps.append(VedicStep(
                explanation="Multiply tens digits vertically and add carry.",
                calculation=f"({a1}×{b1}) + {new_carry} = {lhs}",
                result=lhs
            ))
            
            final_val = int(f"{lhs}{mid_digit}{digit}")
            self.steps.append(VedicStep(
                explanation="Combine the digits to form the final answer.",
                calculation=f"Result: {final_val}",
                result=final_val
            ))
            return final_val
        
        # Fallback for non-2-digit numbers in this demo
        res = a * b
        self.steps.append(VedicStep(
            explanation="Standard multiplication used for non-2-digit pairs in this demo.",
            calculation=f"{a} × {b}",
            result=res
        ))
        return res

    # --- Sutra 3: Addition with Ekadhika Dots (Mental Carry) ---
    # Example: 5 + 8 = 13 (handling carries visually)
    def add_with_ekadhika(self, numbers: List[int]) -> int:
        self.clear_steps()
        self.steps.append(VedicStep(
            explanation="Add numbers column-wise using 'Ekadhika' (dot) method for carries.",
            calculation=f"Summing: {' + '.join(map(str, numbers))}",
            result=None
        ))
        
        total = 0
        carry_log = []
        
        # Simulating a mental running total with carry explanation
        current_sum = 0
        for i, num in enumerate(numbers):
            old_sum = current_sum
            current_sum += num
            
            if current_sum >= 10:
                carry = current_sum // 10
                remainder = current_sum % 10
                # In Vedic mental math, you might keep the remainder and 'dot' the carry to the next column
                # Here we simulate the logic of breaking it down
                self.steps.append(VedicStep(
                    explanation=f"Add {num} to running total. Sum exceeds 10.",
                    calculation=f"{old_sum} + {num} = {current_sum}. Keep {remainder}, carry {carry} (Ekadhika).",
                    result=f"Partial: {remainder}, Carry: {carry}"
                ))
            else:
                self.steps.append(VedicStep(
                    explanation=f"Add {num} to running total.",
                    calculation=f"{old_sum} + {num} = {current_sum}",
                    result=current_sum
                ))
        
        self.steps.append(VedicStep(
            explanation="Final accumulation of all parts.",
            calculation=f"Total Sum",
            result=sum(numbers)
        ))
        
        return sum(numbers)

# --- Usage Demonstration ---

def run_demo():
    calc = VedicCalculator()

    print("=== CASE 1: Squaring 55 (Ekadhikena Purvena) ===")
    res1 = calc.square_ending_in_5(55)
    print(f"Result: {res1}")
    print(calc.get_explanation_report())
    print("\n")

    print("=== CASE 2: Multiplying 94 × 62 (Urdhva-Tiryagbhyam) ===")
    res2 = calc.multiply_general(94, 62)
    print(f"Result: {res2}")
    print(calc.get_explanation_report())
    print("\n")

    print("=== CASE 3: Addition Logic (5 + 8 + 2 + 3) ===")
    # User asked for "5+8 = 8 +2 and + 3 = 13" logic demonstration
    res3 = calc.add_with_ekadhika([5, 8, 2, 3])
    print(f"Result: {res3}")
    print(calc.get_explanation_report())

if __name__ == "__main__":
    run_demo()   