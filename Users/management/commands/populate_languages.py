from django.core.management.base import BaseCommand
from Users.models import Language

class Command(BaseCommand):
    help = 'Populate the database with a predefined list of world languages.'

    def handle(self, *args, **kwargs):
        languages = [
            'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Azerbaijani', 'Basque', 'Belarusian',
            'Bengali', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Cebuano', 'Chichewa', 'Chinese', 'Corsican',
            'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Filipino', 'Finnish', 'French',
            'Frisian', 'Galician', 'Georgian', 'German', 'Greek', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hawaiian',
            'Hebrew', 'Hindi', 'Hmong', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Irish', 'Italian', 'Japanese',
            'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Kinyarwanda', 'Korean', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin',
            'Latvian', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese',
            'Maori', 'Marathi', 'Mongolian', 'Nepali', 'Norwegian', 'Odia', 'Pashto', 'Persian', 'Polish', 'Portuguese',
            'Punjabi', 'Romanian', 'Russian', 'Samoan', 'Scots Gaelic', 'Serbian', 'Sesotho', 'Shona', 'Sindhi',
            'Sinhala', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tajik', 'Tamil',
            'Tatar', 'Telugu', 'Thai', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese',
            'Welsh', 'Xhosa', 'Yiddish', 'Yoruba', 'Zulu'
        ]

        for lang in languages:
            Language.objects.get_or_create(language=lang)
        
        self.stdout.write(self.style.SUCCESS('World languages added successfully!'))
