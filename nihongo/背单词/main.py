from word_manage import WordManager

import random


def mainloop():
    wm = WordManager(wordFilePath="単語.xlsx", infoFilePath='wordsInfo.csv')
    sorted_word_df = wm.word_df.sort_values(by=['ratio', 'choose'], ascending=[False, True])

    num_words = len(sorted_word_df)
    num_choose = int(input('测试数量：'))
    HIGH, MID, LOW = 0.7, 0.2, 0.1
    high_words, high_choose = int(num_words * HIGH) + 1, int(num_choose * HIGH) + 1
    mid_words, mid_choose = int(num_words * MID) + 1, int(num_choose * MID) + 1
    low_words, low_choose = int(num_words * LOW) + 1, int(num_choose * LOW) + 1
    choose_idx =\
        (list(range(high_choose)) +
         list(range(high_words, high_words + mid_choose)) +
         list(range(high_words + mid_words, high_words + mid_words + low_choose)))
    # choose_idx =\
    #     (random.sample(range(high_words), high_choose) +
    #      random.sample(range(high_words, high_words + mid_words), mid_choose) +
    #      random.sample(range(high_words + mid_words, num_words), low_choose))

    for idx in choose_idx:
        word = sorted_word_df.iloc[idx]
        sorted_word_df.iloc[idx, 3] += 1
        kanji, kana = word['kanji'], word['kana']
        user_input = input(f'{kanji}\n>')
        if user_input == kana:
            print('Right!')
        else:
            print(f'Wrong! {kana}')
            sorted_word_df.iloc[idx, 2] += 1

    sorted_word_df['ratio'] = round(sorted_word_df['wrong'] / sorted_word_df['choose'], 2)
    sorted_word_df = sorted_word_df.fillna(1)
    sorted_word_df.to_csv('wordsInfo.csv')


if __name__ == '__main__':
    mainloop()

