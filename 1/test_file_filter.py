import unittest
from file_filter import file_filter


class TestFileFilter(unittest.TestCase):
    def test_one_word_at_line_without_stop(self):
        with open('text.txt', encoding='utf-8') as file:
            gen = file_filter(file, ['цветов', 'все'], [])
            self.assertEqual(list(gen), [
                'цветов Они были яркими и красочными',
                'согревали землю и все живое',
                'Все в этом месте было так естественно',
                'клонилось к горизонту заливая все',
            ])

    def test_one_word_at_line_with_stop(self):
        with open('text.txt', encoding='utf-8') as file:
            gen = file_filter(
                file,
                ['цветов', 'ромашки', 'догонялки'],
                ['стопслово']
            )
            self.assertEqual(list(gen), [
                'цветов Они были яркими и красочными',
                'Там были ромашки колокольчики и васильки',
            ])

    def test_many_words_at_line_without_stop(self):
        with open('text.txt', encoding='utf-8') as file:
            gen = file_filter(
                file,
                ['цветов', 'они', 'зайчата', 'олени', 'траву'],
                []
            )
            self.assertEqual(list(gen), [
                'цветов Они были яркими и красочными',
                'Среди них бегали маленькие зайчата Они',
                'ветвях деревьев сидели птицы Они пели',
                'рыбы Они резво сновали между камнями',
                'паслись олени Они мирно щипали траву',
                'на небе появились первые звезды Они',
            ])

    def test_many_words_at_line_with_stop(self):
        with open('text.txt', encoding='utf-8') as file:
            gen = file_filter(
                file,
                ['цветов', 'они', 'зайчата', 'олени', 'траву'],
                ['бегали', 'сидели', 'птицы']
            )
            self.assertEqual(list(gen), [
                'цветов Они были яркими и красочными',
                'рыбы Они резво сновали между камнями',
                'паслись олени Они мирно щипали траву',
                'на небе появились первые звезды Они',
            ])
