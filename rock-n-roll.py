# Original author: Tianle Cai @ctlllll (Github)
# This is just a slightly more readable copy.

from tiktoken import get_encoding
from tiktoken.model import MODEL_TO_ENCODING

encodings = list(
    dict.fromkeys(MODEL_TO_ENCODING.values())
)

def is_chinese(ch: str):
    code_point = ord(ch)
    return (
        0x4E00 <= code_point <= 0x9FFF or
        0x3400 <= code_point <= 0x4DBF or
        0x20000 <= code_point <= 0x2A6DF or
        0x2A700 <= code_point <= 0x2B73F or
        0x2B740 <= code_point <= 0x2B81F or
        0x2B820 <= code_point <= 0x2CEAF or
        0x2CEB0 <= code_point <= 0x2EBEF or
        0xF900 <= code_point <= 0xFAFF
    )

def main():
    for enc_name in encodings:
        encoder = get_encoding(enc_name)
        models = [
            model for model, enc in MODEL_TO_ENCODING.items()
            if enc == enc_name
        ]

        print(f'Encoding "{enc_name}", {encoder.max_token_value=}')
        print('  Used by:', ', '.join(models), end='')

        tokens = []
        for i in range(encoder.max_token_value + 1):
            try:
                tokens.append(
                    # Try to decode all tokens.
                    encoder.decode([i])
                )
            except:
                pass
            
        cn_words = []
        for token in tokens:
            chn = ''.join(filter(is_chinese, token))

            # Keep this token if:
            # 1. >= 2 chinese characters
            # 2. Not too many other characters
            if (len(chn) >= 2 and
                len(chn) >= len(token) - 1):
                cn_words.append(chn)

        cn_words.sort(key=lambda x: -len(x))

        for i, word in enumerate(cn_words):
            if len(word) != len(cn_words[i - 1]):
                print(f'\n{len(word):4}: ', end='')
            print(word, end=' ')

        print('\n')

if __name__ == '__main__':
    main()
