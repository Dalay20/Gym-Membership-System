"""Main module for gym membership system user interface."""
from gym_membership import menu


def main():
    """Main function to handle user interaction for membership selection.

    This is the entry point for the gym membership system.
    It calls the interactive menu from gym_membership module which handles:
    - Plan selection and validation
    - Feature selection (normal and premium)
    - Multiple membership purchases
    - Group discounts (10% for multiple memberships of same type)
    - Special discounts ($20 for total > $200, $50 for total > $400)
    - Premium surcharge (15% when premium features are included)
    """
    menu()


if __name__ == "__main__":
    main()
