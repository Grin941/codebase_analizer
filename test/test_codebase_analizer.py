from code_base_analizer import CodeBaseAnalizer


class TestCodebaseAnalizer:
    def setup(self):
        self.codebase_analizer = CodeBaseAnalizer([])

    #def test_whether_word_is_verb(self):
    #    nltk_tags = {
    #        'VB': 'go',
    #        'VBG': 'focusing',
    #        'VBN': 'desired',
    #        'NN': 'Fulton',
    #        'AT': 'The',
    #    }

    #    for tag, word in nltk_tags.items():
    #        if tag.startswith('VB'):
    #            assert self.codebase_analizer._is_verb(word)
    #        else:
    #            assert not self.codebase_analizer._is_verb(word)

    #def test_is_verb_returns_false_if_no_word_was_passed(self):
    #    assert not self.codebase_analizer._is_verb()
