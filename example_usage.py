from client import StripeAgenticDynamicPaymentRoutingOptimizer

def main():
    optimizer = StripeAgenticDynamicPaymentRoutingOptimizer()
    intent = {
        "amount_usd": 500.0,
        "currency": "USD",
        "card_network": "visa_debit",
        "country": "US"
    }
    res = optimizer.optimize_payment_route(intent)
    print("--- Stripe Dynamic Interchange Payment Routing ---")
    print(f"Optimal Rail: {res['selected_optimal_rail']['rail_name']}")
    print(f"Processing Fee: ${res['selected_optimal_rail']['processing_fee_usd']} (Effective: {res['selected_optimal_rail']['fee_effective_pct']}%)")
    print(f"Estimated Savings: ${res['savings_vs_standard_card_usd']} per transaction")

if __name__ == "__main__":
    main()
