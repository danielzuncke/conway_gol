def test(**kwargs):
    if kwargs.get('test'):
        print('True')
    elif kwargs.get('test'):
        print('False')
    else:
        print('not parsed')
    return


test(test=False)
