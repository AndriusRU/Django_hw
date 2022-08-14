from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def get_recipe(name_dish, count_person):
    recipe = DATA.get(name_dish)
    my_recipe = dict()

    for key, value in recipe.items():
        my_recipe[key] = round(float(value) * count_person, 2)

    return my_recipe


def recipe(requests, recipe, count = 1):
    count = int(requests.GET.get('servings', 1))
    context = dict()
    context['recipe'] = get_recipe(recipe, count)
    return render(requests, 'calculator/index.html', context)

# def omlet(requests):
#     count = int(requests.GET.get('servings', 1))
#     context = dict()
#     context['recipe'] = get_recipe('omlet', count)
#     return render(requests, 'calculator/index.html', context)
#
# def pasta(requests):
#     count = int(requests.GET.get('servings', 1))
#     context = dict()
#     context['recipe'] = get_recipe('pasta', count)
#     return render(requests, 'calculator/index.html', context)
#
# def buter(requests):
#     count = int(requests.GET.get('servings', 1))
#     context = dict()
#     context['recipe'] = get_recipe('buter', count)
#     return render(requests, 'calculator/index.html', context)


