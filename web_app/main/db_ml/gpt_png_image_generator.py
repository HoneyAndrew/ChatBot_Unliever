import openai
from base64 import b64decode


class Image:
    def image_generate(self):
        openai_api_key = "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"
        openai.api_key = openai_api_key

        prompt = f'hello, please generate for us a product card called {self} for marketplaces, which will look stylish and modern, add the product name and brand name there'

        response = openai.Image.create(

            # Указываем сгенерированный текстовый промт
            prompt=prompt,

            # Указываем кол-во карточек, в нашем случае будем делать 5 разных
            n=1,

            # Указываем размер в пикселях
            size='512x512',

            # # Использую кодировку бейз 64 для удобного сохранения картинки
            response_format='b64_json'
        )

        image_data = b64decode(response['data'][0]['b64_json'])
        file_name = '_'.join(prompt.split(' '))

        with open(f'{file_name}.png', 'wb') as file:
            file.write(image_data)
