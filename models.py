"""Model classes for gym membership system."""


class Item:
    """Represents a membership item with plan and features."""

    plan = {
        "Basic": {
            "benefits": 'Access to standard gym equipment and locker room.',
            "cost": 25
        },
        "Premium": {
            "benefits": 'Includes Basic + Sauna access and free towel service.',
            "cost": 30
        },
        "Student": {
            "benefits": 'Access to standard gym equipment and locker room + early hours access.',
            "cost": 20
        },
        "Family": {
            "benefits": 'Access for up to 4 family members + Pool access.',
            "cost": 40
        }
    }

    ADDITIONAL_FEATURES = {
        'Personal Training': 30,
        'Group Classes': 20,
        'Access to Pool': 15,
        'Specialized Program': 40
    }

    PREMIUM_FEATURES = {
        'Exclusive Gym Facilities': 100,
        'Specialized Training Programs': 80
    }

    # Optional availability maps. Leave empty to assume everything is available.
    # You can set e.g. Item.PLAN_AVAILABLE['Premium'] = False to mark unavailable.
    PLAN_AVAILABLE = {}
    FEATURE_AVAILABLE = {}

    def __init__(self, plan_name, additional_features, premium_membership_features):
        self.plan_name = plan_name
        self.additional_features = additional_features
        self.premium_membership_features = premium_membership_features

    def get_plan_cost(self):
        """Get the cost of a specific plan.

        Returns:
            Cost of the plan, or 0 if plan not found.
        """
        if self.plan_name in self.plan:
            return self.plan[self.plan_name]['cost']
        return 0

    def get_features_cost(self):
        """Calculate total cost of all features (normal and premium)."""
        features_cost = 0
        # Sumar features adicionales normales
        for feature in self.additional_features:
            features_cost += self.get_feature_cost(feature)
        # Sumar features premium
        for feature in self.premium_membership_features:
            features_cost += self.get_feature_cost(feature)
        return features_cost

    def get_feature_cost(self, feature):
        """Get the cost of a specific feature."""
        if feature in self.ADDITIONAL_FEATURES:
            return self.ADDITIONAL_FEATURES[feature]
        if feature in self.PREMIUM_FEATURES:
            return self.PREMIUM_FEATURES[feature]
        return 0

    def calculate_total_membership_cost(self):
        """Calculate the total cost including plan and all features."""
        base_plan_cost = self.get_plan_cost()
        features_cost = self.get_features_cost()
        cost = features_cost + base_plan_cost
        return cost


class Buyer:
    """Represents a buyer with multiple membership items and discount logic."""

    DISCOUNT_GROUP_MEMBERSHIP = 0.10
    NOTIFICATION_GROUP_MEMBERSHIP = (
        f"Adquiere planes de membresía con tus amigos y recibe "
        f"descuentos de: {DISCOUNT_GROUP_MEMBERSHIP * 100}%"
    )

    def __init__(self, items):
        self.items = items
        self.special_discount_amount = 0.0
        self.premium_surcharge_amount = 0.0

    def apply_discount(self, cost):
        """Calculate the group membership discount amount."""
        return cost * self.DISCOUNT_GROUP_MEMBERSHIP

    def notify_discount(self):
        """Display group membership discount notification."""
        print(self.NOTIFICATION_GROUP_MEMBERSHIP)

    def count_membership(self):
        """Count how many memberships of each type are in the purchase.

        Returns:
            dict: Dictionary with format { 'PlanName': quantity }
                  Example: { 'Premium': 2, 'Basic': 1 }
        """
        plan_counts = {}

        for item in self.items:
            if item.plan_name in plan_counts:
                plan_counts[item.plan_name] += 1
            else:
                plan_counts[item.plan_name] = 1

        return plan_counts

    def validate_discount_membership_group(self, plan_counts):
        """Identify plans that qualify for group discounts (quantity > 1)."""
        valid_plans_discount_membership_group = []
        for plan_name in plan_counts:
            quantity = plan_counts[plan_name]
            if quantity > 1:
                valid_plans_discount_membership_group.append(plan_name)
        return valid_plans_discount_membership_group

    def calculate_costs(self):
        """Calculate costs per plan type with group discounts applied."""
        plan_counts = self.count_membership()
        valid_plans = self.validate_discount_membership_group(plan_counts)
        costs = {"Basic": 0.0, "Premium": 0.0, "Student": 0.0, "Family": 0.0}

        for item in self.items:
            item_total_membership_cost = item.calculate_total_membership_cost()
            if item.plan_name in costs:
                costs[item.plan_name] += item_total_membership_cost

        for plan_name in valid_plans:
            if plan_name in costs:
                discount_amount = self.apply_discount(costs[plan_name])
                costs[plan_name] -= discount_amount
        return costs

    def sum_costs(self, costs):
        """Sum all costs and apply premium surcharge and special discounts."""
        total = 0.0
        for plan_name in costs:
            total += costs[plan_name]

        # Aplicar recargo premium del 15% si hay features premium
        if self.has_premium_features():
            self.premium_surcharge_amount = total * 0.15
            total += self.premium_surcharge_amount

        # Aplicar descuentos especiales basados en el coste total
        discounted_total = self.apply_special_discount(total)
        return discounted_total

    def apply_special_discount(self, total):
        """Apply special fixed discounts based on total.

        Rules:
        - If total cost exceeds $400, subtract $50.
        - If total cost exceeds $200, subtract $20.

        The discount amount is stored in `self.special_discount_amount`.
        """
        self.special_discount_amount = 0.0
        if total > 400:
            self.special_discount_amount = 50.0
        elif total > 200:
            self.special_discount_amount = 20.0

        return max(0.0, total - self.special_discount_amount)

    def has_premium_features(self):
        """Check if any item has premium features."""
        for item in self.items:
            for feature in item.premium_membership_features:
                if feature in Item.PREMIUM_FEATURES:
                    return True
        return False
