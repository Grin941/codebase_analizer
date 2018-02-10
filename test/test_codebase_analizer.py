import ast

from code_base_analizer import CodeBaseAnalizer


class TestCodebaseAnalizer:
    def setup(self):
        function_token = ast.FunctionDef()
        setattr(function_token, 'name', 'foo_bar')

        class_token = ast.ClassDef()
        setattr(class_token, 'name', 'TestMySelf')

        self.codebase_analizer = CodeBaseAnalizer([function_token,
                                                   class_token])

    def test_get_codebase_token_names_returns_lowercased_token_names(self, monkeypatch):
        def monkey_token_filter(token_name):
            return lambda token_name: True
        monkeypatch.setattr(self.codebase_analizer, '_filter_token',
                            monkey_token_filter)

        assert set(self.codebase_analizer._get_codebase_tokens_names()) == \
            {'foo_bar', 'testmyself'}

    def test_get_top_words(self):
        assert set(self.codebase_analizer._get_top_words(['one',
            'two', 'two', 'three', 'three', 'three'], 10)) == \
            {('one', 1), ('two', 2), ('three', 3)}
