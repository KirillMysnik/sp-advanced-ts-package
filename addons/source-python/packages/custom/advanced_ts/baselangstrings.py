from translations.strings import LangStrings
from translations.strings import TranslationStrings

from advanced_ts.recursive import RecursiveTS


__all__ = ['BaseLangStrings', ]


class BaseLangStrings(LangStrings):
    """
    This is a LangStrings class but after initialization replaces
    all TranslationStrings values with instances of the given
    dict-inherited base class.
    """
    def __init__(self, infile, encoding='utf_8', base=RecursiveTS):
        super().__init__(infile, encoding)

        for key, value in self.items():
            if isinstance(value, TranslationStrings):
                new_translation_strings = base()

                for key_, value_ in value.items():
                    new_translation_strings[key_] = value_

                self[key] = new_translation_strings
