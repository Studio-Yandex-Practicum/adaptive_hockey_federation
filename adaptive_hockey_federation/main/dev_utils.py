import factory

MIN_WORD = 3
MAX_WORD = 5


def check_len_name(obj):
    words = obj.name.split()
    count = MIN_WORD - len(words)
    if len(words) < MIN_WORD:
        words.append(factory.Faker('word', nb=count))
    if len(words) > MAX_WORD:
        del words[4]
    obj.name = ' '.join(words)
