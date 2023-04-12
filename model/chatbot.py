import openai
from config import api_credentials


class Chatbot:
    def enquiry(user_enquiry_message):
        openai.api_key = api_credentials.OPENAI_API_KEY

        messages = []
        system_msg = "Your are Jasper, a go-to chatbot for all things related to colleges and universities in Kerala, India. You are equipped with a wealth of information on a variety of topics, including admissions requirements, financial aid, campus life, and much more. Keep your responses within 100 words."
        messages.append({"role": "system", "content": system_msg})

        # while input != "quit()":
        message = user_enquiry_message
        messages.append({"role": "user", "content": message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

            reply = response["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})

        except:
            reply = "The chatbot is busy at this moment"

        finally:
            return str(reply)
