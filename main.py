from pprint import pprint


class CookBook:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def __str__(self):
        result = ''
        for recipe in self.recipes:
            result += f'{recipe.name}\n{recipe.count}\n'
            for ingredient in recipe.ingredients:
                result += f'{ingredient.name}, ' \
                          f'{ingredient.quantity}, ' \
                          f'{ingredient.measure}\n'
            result += '\n'
        return result


class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.count = 0

    def add_ingredients(self, *args):
        for recipe in args:
            self.ingredients.append(recipe)
            self.count += 1


class Ingredient:
    def __init__(self, name, quantity, measure):
        self.name = name
        self.quantity = quantity
        self.measure = measure


class Factory:

    @staticmethod
    def write_to_txt(file, book):
        result = ''
        for recipe in book.recipes:
            result += f'{recipe.name}\n{recipe.count}\n'
            for ingredient in recipe.ingredients:
                result += f'{ingredient.name} | ' \
                          f'{ingredient.quantity} | ' \
                          f'{ingredient.measure}\n'
            result += '\n'
        with open(file, 'w') as f:
            f.write(result.strip('\n'))
        return

    @staticmethod
    def get_dictionary_from_txt(file):
        with open(file, 'r') as f:
            data = {}
            for line in f:
                data[line.strip()] = []
                count = int(f.readline())
                for i in range(count):
                    name, count, measure = f.readline().strip().split(' | ')
                    ingredient = {
                        'ingredient_name': name,
                        'quantity': count,
                        'measure': measure
                    }
                    data[line.strip()].append(ingredient)
                f.readline()
            return data

    @staticmethod
    def get_shop_list_by_dishes(book, dishes, person_count):
        result = {}
        for recipe, ingredients in book.items():
            if recipe in dishes:
                for ingredient in ingredients:
                    name = ingredient["ingredient_name"]
                    quantity = int(ingredient["quantity"]) * person_count
                    measure = ingredient["measure"]
                    if name not in result.keys():
                        result[name] = {
                            "measure": measure,
                            "quantity": quantity
                        }
                    else:
                        result[name]["quantity"] += quantity
        return result

    @staticmethod
    def merge_files(*args, destination):
        lines = []
        for file in args:
            with open(file, 'r') as f:
                raw_data = f.readlines() + [f'\n{"-" * 30}\n']
                meta = [
                    f'имя - {file}\n',
                    f'количество строк - {len(raw_data) - 1}\n\n'
                ]
                data = meta + raw_data
                lines.append(data)
        lines.sort(key=len)
        lines[0] = [f'{"-" * 30}\n'] + lines[0]
        with open(destination, 'w') as f:
            for line in lines:
                f.writelines(line)


# Создаем пару рецептов
book = CookBook()
recipe = Recipe('Омлет')
ingr1 = Ingredient('Молоко', 100, 'мл')
ingr2 = Ingredient('Яйцо', 2, 'шт')
ingr3 = Ingredient('Помидор', 2, 'шт')
recipe.add_ingredients(ingr1, ingr2, ingr3)
book.add_recipe(recipe)
recipe = Recipe('Запеченый картофель')
ingr1 = Ingredient('Картофель', 1, 'кг')
ingr2 = Ingredient('Чеснок', 3, 'зубч')
ingr3 = Ingredient('Сыр гауда', 100, 'гр')
recipe.add_ingredients(ingr1, ingr2, ingr3)
book.add_recipe(recipe)
recipe = Recipe('Яичница')
ingr1 = Ingredient('Яйцо', 3, 'шт')
recipe.add_ingredients(ingr1)
book.add_recipe(recipe)
print(book)

# Запишем книгу в файл cookbook
Factory.write_to_txt('cookbook', book)

# Обратное чтение, на выходе получаем словарь для задачи 1
cook_book = Factory.get_dictionary_from_txt('cookbook')
pprint(cook_book, sort_dicts=False)

# Из этого словаря получаем словарь для задачи 2
# Внутрь передается сам словарь для избежания обращения к глобальным переменным
dishes = ['Омлет', 'Запеченый картофель', 'Яичница']
recipes_per_person = Factory.get_shop_list_by_dishes(cook_book, dishes, 2)
pprint(recipes_per_person, sort_dicts=False)

# Соединим cookbook и файл cookbook1, в файл cookbook 2, задача 3
Factory.merge_files('cookbook', 'cookbook1', destination='cookbook2')
