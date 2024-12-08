from math import isclose

from app.logic.financial_plan_logic import FinancialPlan


class TestCalculateFinancing:
    """
    Test suite for the FinancialPlan.calculate_financing method.

    These tests validate that the method returns correct financing plans
    for different conditions, such as custom terms, no principal scenarios,
    and varying annual interest rates.
    """

    def test_default_terms(self):
        """
        Test that the default terms (3, 4, 5, 6 years) are returned correctly
        and produce a non-empty dictionary.
        """
        car_price = 30000.0
        down_payment = 5000.0
        result = FinancialPlan.calculate_financing(car_price, down_payment)

        assert isinstance(result, dict)
        assert len(result) == 4
        for key in ["3 years", "4 years", "5 years", "6 years"]:
            assert key in result
            assert isinstance(result[key]["term_months"], int)
            assert isinstance(result[key]["approx_monthly_installment"], float)
            assert isinstance(result[key]["total_cost"], float)

    def test_zero_principal(self):
        """
        If the down_payment equals the car_price, the principal should be zero
        and the monthly installment should also be zero.
        """
        car_price = 30000.0
        down_payment = 30000.0
        result = FinancialPlan.calculate_financing(car_price, down_payment)

        for plan in result.values():
            assert plan["approx_monthly_installment"] == 0.0
            assert plan["total_cost"] == 0.0

    def test_custom_terms(self):
        """
        Test providing custom terms (2, 10 years) and ensuring those terms are reflected correctly.
        """
        car_price = 50000.0
        down_payment = 10000.0
        custom_terms = [2, 10]
        result = FinancialPlan.calculate_financing(
            car_price, down_payment, annual_rate=0.1, terms=custom_terms)

        assert len(result) == 2
        assert "2 years" in result
        assert "10 years" in result
        assert result["2 years"]["term_months"] == 24
        assert result["10 years"]["term_months"] == 120

    def test_installment_calculation_accuracy(self):
        """
        Test that the returned installment is approximately correct by comparing
        the total cost and the expected formula outcome with a small tolerance.
        """
        car_price = 40000.0
        down_payment = 10000.0
        annual_rate = 0.1
        term_years = [3]
        result = FinancialPlan.calculate_financing(
            car_price, down_payment, annual_rate=annual_rate, terms=term_years)

        term_key = "3 years"
        plan = result[term_key]
        term_months = plan["term_months"]
        monthly_rate = annual_rate / 12.0
        principal = car_price - down_payment

        # Recalculate the monthly installment here to verify correctness:
        expected_installment = 0.0
        if principal > 0:
            expected_installment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / (
                (1 + monthly_rate) ** term_months - 1)

        # Check if the returned installment is close to the expected value
        assert isclose(plan["approx_monthly_installment"],
                       round(expected_installment, 2), rel_tol=1e-5)

    def test_negative_down_payment(self):
        """
        Even though not a realistic scenario, test that the calculation runs
        with a negative down payment and returns a larger principal.
        """
        car_price = 20000.0
        down_payment = -1000.0
        result = FinancialPlan.calculate_financing(car_price, down_payment)

        for plan in result.values():
            # Monthly installment and total cost should be > 0 due to increased principal
            assert plan["approx_monthly_installment"] > 0
            assert plan["total_cost"] > 0

    def test_zero_annual_rate(self):
        """
        Test calculation with zero annual interest rate, ensuring the installment
        equals the principal divided by the number of months.
        """
        car_price = 30000.0
        down_payment = 10000.0
        annual_rate = 0.0
        terms = [5]  # 5 years = 60 months
        result = FinancialPlan.calculate_financing(
            car_price, down_payment, annual_rate=annual_rate, terms=terms)

        plan = result["5 years"]
        principal = car_price - down_payment
        expected_installment = principal / 60
        assert isclose(plan["approx_monthly_installment"],
                       round(expected_installment, 2), rel_tol=1e-5)
        assert isclose(plan["total_cost"], round(
            expected_installment * 60, 2), rel_tol=1e-5)
