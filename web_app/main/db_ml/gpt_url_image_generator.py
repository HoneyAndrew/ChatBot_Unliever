import openai
import json


class Image:
    def generate_image(self, name_of_product):
        openai_api_key = "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"
        openai.api_key = openai_api_key

        name_of_product = 'soap'
        prompt = f'hello, please generate for us a product card called {name_of_product} for marketplaces, which will look stylish and modern, add the product name and brand name there'

        response = openai.Image.create(

            # Указываем сгенерированный текстовый промт
            prompt=prompt,

            # Указываем кол-во карточек, в нашем случае будем делать 5 разных
            n=1,

            # Указываем размер в пикселях
            size='512x512',
        )

        with open("data.json", 'w') as file:
            json.dump(response, file, indent=4, ensure_ascii=False)

        with open("data.json", 'r') as file:
            json.dump(response, file, indent=4, ensure_ascii=False)

