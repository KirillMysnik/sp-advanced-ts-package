from translations.strings import TranslationStrings


__all__ = ['RecursiveTS', ]


class RecursiveTS(TranslationStrings):
    """
    This class provides recursive get_string method.
    """
    def get_string(self, language=None, **tokens):
        """
        Exposes packed tokens (self.tokens) and additional tokens (**tokens).
        """

        # Deeply expose all TranslationStrings instances in self.tokens
        for token_name, token in self.tokens.items():
            if isinstance(token, TranslationStrings):
                new_tokens = self.tokens.copy()
                del new_tokens[token_name]

                # Pass additional tokens - these will NOT be used to
                # continue deep exposition but will be used to call
                # super().get_string.
                token = token.get_string(language, **tokens)
                self.tokens[token_name] = token

        # Then shallowly expose all TranslationsStrings instances in **tokens
        for token_name, token in tokens.items():
            if isinstance(token, TranslationStrings):

                # Don't pass any additional tokens.
                # The token should either be trivial (regular
                # TranslationStrings instance) or rely on itself (self.tokens).
                tokens[token_name] = token.get_string(language)

        # Finally with all of the tokens exposed, call the original get_string
        return super().get_string(language, **tokens)

    def tokenize(self, **tokens):
        """Return new TranslationStrings object with updated tokens."""
        rs = type(self)()
        for key, value in self.items():
            rs[key] = value

        rs.tokens = self.tokens.copy()
        rs.tokens.update(tokens)
        return rs
