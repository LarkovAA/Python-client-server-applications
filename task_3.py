import yaml
import random

data_dict = {
    'one_key': ['открыться', 'королевский', 'общий', 'решаться', 'невероятный'],
    'two_key': random.randint(0, 1000000),
    'three_key': {
        'Inverted_exclamation_mark': '¡',
        'Copyright mark': '©',
        'Latin letter reverse guttural bow with a dash': 'ʢ',
        'Tamil symbol of the Year': '௵',
        'Bangladeshi taka': '৳'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as f_y:
    yaml.dump(data_dict, f_y, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f_n:
    print(f_n.read())
