from functools import reduce, total_ordering
from operator import xor

pizza_database = {
    'Sunday': {'name': 'SundayPizza',
               'ingredients': ['meat', 'cheese', 'tomato'],
               'cost': 101},
    'Monday': {'name': 'MondayPizza',
               'ingredients': ['meat', 'cheese', 'potato'],
               'cost': 102},
    'Tuesday': {'name': 'TuesdayPizza',
                'ingredients': ['cheese', 'tomato', 'beef', 'onion'],
                'cost': 103},
    'Wednesday': {'name': 'WednesdayPizza',
                  'ingredients': ['cheese', 'tomato', 'chicken', 'pineapple'],
                  'cost': 104},
    'Thursday': {'name': 'ThursdayPizza',
                 'ingredients': ['cheese', 'tomato', 'anchovy', 'mushroom'],
                 'cost': 105},
    'Friday': {'name': 'FridaysPizza',
               'ingredients': ['cheese', 'tomato', 'anchovy', 'onion'],
               'cost': 106},
    'Saturday': {'name': 'SaturdayPizza',
                 'ingredients': ['cheese', 'tomato', 'ham', 'onion', 'pineapple'],
                 'cost': 107}
}

ingredients_database = {
    'chicken': {'cost': 10, 'mass': 100},
    'banana': {'cost': 20, 'mass': 100},
    'meat': {'cost': 10, 'mass': 100},
    'potato': {'cost': 10, 'mass': 100},
    'cheese': {'cost': 10, 'mass': 100},
    'tomato': {'cost': 10, 'mass': 100},
    'anchovy': {'cost': 10, 'mass': 100},
    'beef': {'cost': 10, 'mass': 100},
    'onion': {'cost': 10, 'mass': 100},
    'pineapple': {'cost': 10, 'mass': 100},
    'mushroom': {'cost': 10, 'mass': 100},
    'ham': {'cost': 10, 'mass': 100},
}
ingredients = list(ingredients_database.keys())


class Customer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I am Customer {self.name}"

    @staticmethod
    def create_order(pizzeria):
        order = Order(pizzeria)
        while True:
            extra_ing_indicator = pizzeria.binary_question("Add some extra ingredients? (Y/N) ")
            if extra_ing_indicator:
                Customer.order_custom_pizza(order, pizzeria)
            else:
                order.push(Pizza(pizzeria.today))
            repeat_indicator = pizzeria.binary_question("Do you want to order another one pizza? (Y/N) ")
            if repeat_indicator:
                continue
            break
        return order

    @staticmethod
    def order_custom_pizza(order, pizzeria):
        while True:
            # Choosing the extra ingredients
            print("Which of the following ingredients do you want to add? (Example: 'chicken, onion')")
            extra_ingredients = input(f"Available ingredients: {', '.join(ingredients)}.\n")
            # Check if some unknown ingredients in extra_ingredients
            extra_ingredients = pizzeria.parse_string(extra_ingredients)
            exit_flag = pizzeria.check_ingredients_availability(extra_ingredients)
            if exit_flag:
                # Making a custom pizza (add some extra ingredients)
                custom_pizza = Pizza(pizzeria.today)
                for name in extra_ingredients:
                    custom_pizza += Ingredient(name)
                custom_pizza.type = 'CustomPizza'
                order.push(custom_pizza)
                return


class Ingredient:
    def __init__(self, name):
        self.name = name
        self.cost = ingredients_database[name]['cost']
        self.mass = ingredients_database[name]['mass']

    def __str__(self):
        return f'Ingredient {self.name}'


class Order:
    def __init__(self, pizzeria):
        self.pizza_dict = {}
        self.pizzeria = pizzeria

    @property
    def total_cost(self):
        return sum([pizza.cost * self.pizza_dict[pizza] for pizza in self.pizza_dict.keys()])

    def add_pizza(self, pizza, number=1):
        try:
            self.pizza_dict[pizza] += number
        except KeyError:
            self.pizza_dict[pizza] = number

    def push(self, pizza):
        # Get the number of regular pizzas
        number_of_pizzas = self.pizzeria.ask_number_of_pizzas()
        # Push pizza to order list
        self.add_pizza(pizza, number_of_pizzas)

    def __str__(self):
        printable_order_list = []
        for pizza in self.pizza_dict.keys():
            printable_order_list.append(f"{self.pizza_dict[pizza]}\t{pizza}")
        return '*' * 80 + '\nOrder:\n' + '\n'.join(
            printable_order_list) + f'\nTotal cost: {self.total_cost}\n' + '*' * 80


class Pizzeria:
    possible_answers = ['Y', 'y', 'yes', 'YES', 'N', 'n', 'no', 'NO']
    positive_answers = ['Y', 'y', 'yes', 'YES']
    negative_answers = ['N', 'n', 'no', 'NO']

    def __init__(self, name, today):
        self.name = name
        self.today = today
        self.today_pizza = Pizza(today)

    @staticmethod
    def execute(order):
        print("Executing pizza...")
        for pizza in order.pizza_dict:
            print(pizza)
            for ingredient, portions in pizza:
                if portions != 1:
                    print(f'\tAdd {portions}x {ingredient} to pizza')
                else:
                    print(f'\tAdd {ingredient} to pizza')
        print('Bon appetit! =)')

    @staticmethod
    def binary_question(promp):
        while True:
            answer = input(promp)
            if answer in Pizzeria.possible_answers:
                break
        return answer in Pizzeria.positive_answers

    @staticmethod
    def ask_number_of_pizzas():
        while True:
            try:
                number_of_pizzas = int(input("How much pizza's you want? "))
            except ValueError:
                continue
            if number_of_pizzas < 1:
                print("Please try again.")
                continue
            return number_of_pizzas

    @staticmethod
    def parse_string(string):
        elements_list = [elem.strip() for elem in string.split(',')]
        return [elem for elem in elements_list if elem]

    @staticmethod
    def check_ingredients_availability(ingredients_list):
        for ingredient in ingredients_list:
            if ingredient not in ingredients_database.keys():
                print(f"Sorry, but {ingredient} isn't available. Please try again.")
                return False
        return True

    def __str__(self):
        return f"Welcome to the '{self.name}' Pizzeria"


@total_ordering
class Pizza:
    def __init__(self, day):
        self.day = day
        self.type = pizza_database[day]['name']
        pizza_ingredients = pizza_database[day]['ingredients']
        self.ingredients = dict(zip(pizza_ingredients, [1] * len(pizza_ingredients)))
        self.size = len(self.ingredients)
        self.cost = pizza_database[day]['cost']

    def __str__(self):
        return f"{self.type} with {', '.join(self.ingredients)}."

    def __len__(self):
        return len(self.ingredients)

    def __add__(self, other):
        if isinstance(other, Ingredient):
            if other.name in self.ingredients.keys():
                self.ingredients[other.name] += 1
            else:
                self.ingredients[other.name] = 1
            self.cost += other.cost
            return self
        raise NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        return iter(self.ingredients.items())

    def __eq__(self, other):
        if isinstance(other, Pizza):
            ingredients1 = sorted(self.ingredients.keys())
            ingredients2 = sorted(other.ingredients.keys())
            if ingredients1 == ingredients2:
                for key in ingredients1:
                    if self.ingredients[key] != other.ingredients[key]:
                        return False
                return True
        raise NotImplemented

    def __gt__(self, other):
        return len(self) > len(other)

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return reduce(xor, hashes, 0)

    def __contains__(self, item):
        if isinstance(item, Ingredient):
            return item.name in self.ingredients.keys()


if __name__ == '__main__':
    from random import choice
    # Define today
    current_day = choice(list(pizza_database.keys()))
    print(f"Today is {current_day}.")

    new_customer = Customer('Alex Cherniuk')
    print(new_customer)

    new_pizzeria = Pizzeria('Uncle Johns pizza', today=current_day)
    print(new_pizzeria)
    print(f"Today we have pizza with {', '.join(new_pizzeria.today_pizza.ingredients)}")

    new_order = new_customer.create_order(new_pizzeria)
    print(new_order)
    new_pizzeria.execute(new_order)


# Today is Friday.
# I am Customer Alex Cherniuk
# Welcome to the 'Uncle Johns pizza' Pizzeria
# Today we have pizza with cheese, tomato, anchovy, onion
# Add some extra ingredients? (Y/N) n
# How much pizza's you want? 10
# Do you want to order another one pizza? (Y/N) y
# Add some extra ingredients? (Y/N) y
# Which of the following ingredients do you want to add? (Example: 'chicken, onion')
# Available ingredients: chicken, banana, meat, potato, cheese, tomato, anchovy, beef, onion, pineapple, mushroom, ham.
# chicken, onion, mushroom
# How much pizza's you want? 2
# Do you want to order another one pizza? (Y/N) y
# Add some extra ingredients? (Y/N) y
# Which of the following ingredients do you want to add? (Example: 'chicken, onion')
# Available ingredients: chicken, banana, meat, potato, cheese, tomato, anchovy, beef, onion, pineapple, mushroom, ham.
# tomato, cheese, ham
# How much pizza's you want? 3
# Do you want to order another one pizza? (Y/N) n
# ********************************************************************************
# Order:
# 10  FridaysPizza with cheese, tomato, anchovy, onion.
# 2   CustomPizza with cheese, tomato, anchovy, onion, chicken, mushroom.
# 3   CustomPizza with cheese, tomato, anchovy, onion, ham.
# Total cost: 1740
# ********************************************************************************
# Executing pizza...
# FridaysPizza with cheese, tomato, anchovy, onion.
#     Add cheese to pizza
#     Add tomato to pizza
#     Add anchovy to pizza
#     Add onion to pizza
# CustomPizza with cheese, tomato, anchovy, onion, chicken, mushroom.
#     Add cheese to pizza
#     Add tomato to pizza
#     Add anchovy to pizza
#     Add 2x onion to pizza
#     Add chicken to pizza
#     Add mushroom to pizza
# CustomPizza with cheese, tomato, anchovy, onion, ham.
#     Add 2x cheese to pizza
#     Add 2x tomato to pizza
#     Add anchovy to pizza
#     Add onion to pizza
#     Add ham to pizza
# Bon appetit! =)
