class Rule:
    def __init__(self, category, comparison_operator, threshold):
        self.category = category
        self.comparison_operator = comparison_operator
        self.threshold = threshold

    def check(self, spending_percentages):
        if self.comparison_operator == '<':
            return spending_percentages[self.category] < self.threshold
        elif self.comparison_operator == '>':
            return spending_percentages[self.category] > self.threshold
        else:
            return False

class ExpertSystem:
    def __init__(self):
        self.rules = []
    
    def add_rule(self, category, comparison_operator, threshold):
        self.rules.append(Rule(category, comparison_operator, threshold))

    def evaluate(self, spending_percentages):
        for rule in self.rules:
            if not rule.check(spending_percentages):
                return 'Budgeting rule violated: {} {} {}'.format(rule.category, rule.comparison_operator, rule.threshold)
        return 'Budgeting rules satisfied.'

# Create an instance of the ExpertSystem class
expert_system = ExpertSystem()

# Add some rules
expert_system.add_rule('Entertainment', '<', 0.1)
expert_system.add_rule('Housing', '<', 0.4)

# Evaluate the spending habits
spending_percentages = {'Entertainment': 0.12, 'Housing': 0.3}
print(expert_system.evaluate(spending_percentages)) # Budgeting rule violated: Entertainment < 0.1
