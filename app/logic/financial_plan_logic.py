from typing import Dict, List, Union


class FinancialPlan:
    @staticmethod
    def calculate_financing(
            car_price: float,
            down_payment: float,
            annual_rate: float = 0.10,
            terms: List[int] = None
    ) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        Returns a dictionary with financing plans for different terms.

        Fixed installment formula:
        monthly_installment = principal * [monthly_rate*(1+monthly_rate)^total_months / ((1+monthly_rate)^total_months - 1)]

        Where:
        - principal = car_price - down_payment
        - monthly_rate = annual_rate / 12
        - total_months = years * 12
        """
        terms = terms or [3, 4, 5, 6]
        financing_plans: Dict[str, Dict[str, Union[int, float]]] = {}
        principal: float = car_price - down_payment
        monthly_rate: float = annual_rate / 12.0

        for years in terms:
            total_months: int = years * 12
            monthly_installment: float = 0.0
            if principal > 0:
                monthly_installment = principal * (monthly_rate * (1 + monthly_rate) ** total_months) / (
                    (1 + monthly_rate) ** total_months - 1)

            financing_plans[f"{years} years"] = {
                "term_months": total_months,
                "approx_monthly_installment": round(monthly_installment, 2),
                "total_cost": round(monthly_installment * total_months, 2)
            }

        return financing_plans
