#!/usr/bin/env python3
import json
import sys
from client import StripeAgenticDynamicPaymentRoutingOptimizer

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        optimizer = StripeAgenticDynamicPaymentRoutingOptimizer()
        intent = {"amount_usd": 250.0, "currency": "USD", "country": "US", "card_network": "debit"}
        res = optimizer.optimize_payment_route(intent)
        assert res["selected_optimal_rail"] is not None
        assert res["routing_verdict"] == "OPTIMAL_INTERCHANGE_ROUTING_LOCKED"
        print(f"[TEST PASS] Stripe Payment Routing Optimal Rail: {res['selected_optimal_rail']['rail_name']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-stripe-payment-router", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "optimize_payment_route", "description": "Stripe dynamic payment routing & interchange fee optimizer"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                optimizer = StripeAgenticDynamicPaymentRoutingOptimizer()
                out = optimizer.optimize_payment_route(args.get("payment_intent", {}), args.get("available_rails"))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
