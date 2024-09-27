import os
import unittest

from file_filter import file_filter


class TestFileFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_text_path = os.path.join(os.path.dirname(__file__), 'text.txt')

    def test_open_with_filename(self):
        gen = file_filter(self.file_text_path, ['цветов', 'ромашки'], [])
        self.assertEqual(list(gen), [
            'цветов Они были яркими и красочными',
            'Там были ромашки колокольчики и васильки',
        ])

    def test_open_with_file_object(self):
        with open(self.file_text_path, encoding='utf-8') as file:
            gen = file_filter(file, ['среди'], [])
            self.assertEqual(list(gen), [
                'Среди них бегали маленькие зайчата Они',
            ])

    def test_one_word_at_line_without_stop(self):
        with open(self.file_text_path, encoding='utf-8') as file:
            gen = file_filter(file, ['цветов', 'все'], [])
            self.assertEqual(list(gen), [
                'цветов Они были яркими и красочными',
                'согревали землю и все живое',
                'Все в этом месте было так естественно',
                'клонилось к горизонту заливая все',
            ])

    def test_one_word_at_line_with_stop(self):
        with open(self.file_text_path, encoding='utf-8') as file:
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
        with open(self.file_text_path, encoding='utf-8') as file:
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
        with open(self.file_text_path, encoding='utf-8') as file:
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

    def test_register(self):
        gen = file_filter(self.file_text_path, ['Среди'], [])
        self.assertEqual(list(gen), [
            'Среди них бегали маленькие зайчата Они',
        ])

        gen = file_filter(self.file_text_path, ['среди'], [])
        self.assertEqual(list(gen), [
            'Среди них бегали маленькие зайчата Они',
        ])

        gen = file_filter(self.file_text_path, ['вдалеке'], [])
        self.assertEqual(list(gen), [
            'вокруг Вдалеке виднелась речка Ее воды',
        ])

        gen = file_filter(self.file_text_path, ['но'], [])
        self.assertEqual(list(gen), [
            'покой и умиротворение но в то же',
            'и тишину Но и она была',
        ])

        gen = file_filter(self.file_text_path, ['Но'], [])
        self.assertEqual(list(gen), [
            'покой и умиротворение но в то же',
            'и тишину Но и она была',
        ])

    def test_find_all_string(self):
        gen = file_filter(self.file_text_path,
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон'],
                          [])
        self.assertEqual(list(gen), [
            'свои песни создавая мелодичный фон',
        ])

        gen = file_filter(self.file_text_path,
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон'],
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон'])
        self.assertEqual(list(gen), [])

        gen = file_filter(self.file_text_path,
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон',
                           'изредка', 'поднимая', 'головы', 'чтобы',
                           'оглядеться'],
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон'])
        self.assertEqual(list(gen),
                         ['изредка поднимая головы чтобы оглядеться'])

        gen = file_filter(self.file_text_path,
                          ['свои', 'песни', 'создавая', 'мелодичный', 'фон',
                           'изредка', 'поднимая', 'головы', 'чтобы',
                           'оглядеться'],
                          ['песни', 'чтобы'])
        self.assertEqual(list(gen), [])
