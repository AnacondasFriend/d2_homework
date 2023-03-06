from django import template
 
register = template.Library()
 
 
@register.filter(name='Censor')  
def Censor(value):
    all_words = value.split(' ')
    result = ''
    for word in all_words:
        if word == 'блять':
            word = '*****'
            result += ' ' + word
        elif word == 'блять,':
            word = '*****,'
            result += ' ' + word

        elif word == 'блять!':
            word = '*****,'
            result += ' ' + word

        elif word == 'блять.':
            word = '*****,'
            result += ' ' + word

        elif word == 'блять?':
            word = '*****,'
            result += ' ' + word
        
        else:
            result += ' ' + word
    #value = ' '.join(all_words)
    return result