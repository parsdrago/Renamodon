import webview
import os
import ollama
import json

class Api:
    def get_files(self):
        folder = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
        self.directory = folder[0]
        files = [str(name) for name in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, name))]
        return files

    def complement(self, data):
        print(data)
        prompt = f"file names are converted by some rules. Here are some examples:\n\n{"\n".join(datum["fileName"]+" -> "+datum["converted"] for datum in data["converted"])}\n\nPlease estimated converted names for the following file names:\n\n{"\n".join(datum for datum in data["inconverted"])}\n\nResponse in the following format: {{'converted': ['converted1', 'converted2', ...]}}"
        print(prompt)
        response = ollama.generate(
            model='llama3',
            prompt=prompt,
            format='json',
            )
        print(response)
        result = {
            file_name: converted
            for file_name, converted in zip(data["inconverted"], json.loads(response["response"])["converted"])
        }
        print(result)
        return result

    def rename(self, data):
        for item in data:
            os.rename(
                os.path.join(self.directory, item["fileName"]),
                os.path.join(self.directory, item["candidate"])
            )
        return 'done'


api = Api()

html = open('assets/index.html', 'r', encoding='utf-8').read()

def load_css(window):
    window.load_css(open('assets/style.css', 'r', encoding='utf-8').read())

window = webview.create_window('Renamodon', html=html, js_api=api)
webview.start(load_css, window)
