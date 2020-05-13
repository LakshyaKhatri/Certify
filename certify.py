from PIL import Image, ImageDraw, ImageFont
import json
import sys


class Certify:
    def __init__(self, template, input, output):
        self.__template = template
        self.__input = input
        self.__output = output
        self.__has_more_input = True
        self.__fields = []
        self.__config()

    def __ask_for_input(self):
        print('[certify] Enter field values:')
        for i in range(len(self.__fields)):
            self.__fields[i]['text'] = input(
                '[certify] ' + self.__fields[i]['name'] + ':'
            )
        return False

    def __config(self):
        try:
            with open('template-config.json') as configFile:
                # configure fields for specified template
                self.__fields = json.load(configFile)[self.__template]
        except FileNotFoundError:
            sys.exit("[certify] Configuration Error: Missing configuration file")
        except json.decoder.JSONDecodeError as e:
            print("[certify] Configuration Error: Invalid JSON Format")
            sys.exit(str(e))
        except Exception as e:
            sys.exit(str(e))
        print("[certify] Using template " + self.__template + '.jpg')

    def __parse_csv(self):
        pass

    def has_next_input(self):
        return self.__has_more_input

    def generate_certificate(self):
        try:
            certificate = Image.open('templates/' + self.__template + '.jpg')
            drawHandler = ImageDraw.Draw(certificate)

            print("[certify] Generating certificate " + self.__fields[0]['text'] + '.pdf ...')
            for field in self.__fields:
                font = ImageFont.truetype('fonts/' + field['font'], field['size'])
                textWidth, textHeight = drawHandler.textsize(
                    field['text'],
                    font=font
                )
                drawHandler.text((
                    field['x'] - (textWidth // 2),
                    field['y'] - (textHeight // 2)),
                    field['text'],
                    fill=field['color'],
                    font=font
                )
                certificate.save(self.__output + self.__fields[0]['text'] + '.pdf')
                print('[certify] Certificate generated successfully')
        except Exception:
            print('[certify] Error generating certificate')
            sys.exit('Exiting')

    def next_input(self):
        # if input CSV file is not provided
        if not self.__input:
            # ask user for prividing values
            self.__has_more_input = self.__ask_for_input()
        else:
            # set values from CSV file
            self.__has_more_input = self.__parse_csv()
