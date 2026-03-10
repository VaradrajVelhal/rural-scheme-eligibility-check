from .models import Scheme

def evaluate_schemes(user_data):
    results = []

    user_state = user_data.get("state")

    schemes = Scheme.objects.all()

    for scheme in schemes:
        rule_results = []

        # State filtering
        if not scheme.is_central:
            if user_state not in scheme.states.all():
                continue

        rules = scheme.eligibilityrule_set.all()
        is_eligible = True

        for rule in rules:

            field_value = user_data.get(rule.field_name)

            if rule.field_name in ["income", "age"]:
                field_value = int(field_value)
                rule_value = int(rule.value)
            else:
                rule_value = rule.value

            passed = True

            if rule.operator == "lt":
                passed = field_value < rule_value
            elif rule.operator == "gt":
                passed = field_value > rule_value
            elif rule.operator == "lte":
                passed = field_value <= rule_value
            elif rule.operator == "gte":
                passed = field_value >= rule_value
            elif rule.operator == "eq":
                passed = str(field_value).lower() == str(rule_value).lower()
            elif rule.operator == "in":
                values = [v.strip().lower() for v in rule.value.split(",")]
                passed = str(field_value).lower() in values

            rule_results.append({
                "rule": f"{rule.field_name} {rule.operator} {rule.value}",
                "passed": passed
            })

            if not passed:
                is_eligible = False

        results.append({
            "scheme": scheme,
            "is_eligible": is_eligible,
            "rules": rule_results
        })

    return results