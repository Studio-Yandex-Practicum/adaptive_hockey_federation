def check_len(field, max, min):
    words = field.split()
    count = min - len(words)
    if len(words) < min:
        add_words = words[:count]
        words.append(' '.join(add_words))
    if len(words) > max:
        del words[max:]
    field = ' '.join(words)
    return field
