class Sentence:
    def __init__(self, jpn, chn, embedding, where):
        self.jpn = jpn
        self.chn = chn
        self.embedding = embedding
        self.where = where

    def __repr__(self):
        return f'Japanese:\t{self.jpn}\nChinese:\t{self.chn}\nGrammars:\t{self.embedding}\n\n'
