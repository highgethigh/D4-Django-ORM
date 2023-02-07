from django import template
# если мы не зарегистрируем наши фильтры, то django никогда не узнает где именно их искать и фильтры потеряются :(
register = template.Library()
ban_words = ['мразь', 'дурака', 'шакал']



# регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
@register.filter(name='censor')
# первый аргумент здесь — это то значение, к которому надо применить фильтр,
# второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|multiply:arg
def censor(value, arg):
    for i in value.split():
        if i.lower() in ban_words:
            value = value.replace(i, arg)
    return value

#
