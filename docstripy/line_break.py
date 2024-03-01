"""Line break function."""

from typing import List

from docstripy.lines_routines import (
    add_eol,
    clean_trailing_empty,
    clean_trailing_spaces,
)


def line_break(
    lines: List[str], max_line_length: int, num_add_char: int = 0
) -> List[str]:
    """Break lines at a given length.

    Parameters
    ----------
    lines : List[str]
        List of lines to break.
    max_line_length : int
        Maximum line length.
    num_add_char : int, optional
        Number of additional characters to add at the first line that are not
        on the `lines` list. By default, 0.
    """
    if max_line_length <= 0 or not lines:
        return lines
    new_lines = lines.copy()
    new_lines = clean_trailing_spaces(new_lines)
    new_lines[0] = num_add_char * " " + new_lines[0]  # Will be removed at the end
    flat_line = "".join(new_lines)
    list_flat = []
    for i in range(len(flat_line)):
        if flat_line[i] != "\n":
            list_flat.append(flat_line[i])
        else:
            if i > 0 and flat_line[i - 1] == "\n":
                list_flat.append("\n")
            elif i < len(flat_line) - 1:
                next_chr_i = ord(flat_line[i + 1])
                next_is_alpha = 65 <= next_chr_i <= 90 or 97 <= next_chr_i <= 122
                if next_is_alpha:
                    list_flat.append(" ")
                else:
                    list_flat.append("\n")
            else:
                list_flat.append("\n")
    new_lines = "".join(list_flat).split("\n")
    sentences = [line.split(". ") for line in new_lines]
    for part in sentences:
        for i in range(len(part)):
            part[i] += "." if i < len(part) - 1 else ""
    sentences = [break_sentences(sentence, max_line_length) for sentence in sentences]
    sentences = [add_eol(sentence) for sentence in sentences]
    new_lines = [line for sublist in sentences for line in sublist]
    # Remove leading padding symbol
    new_lines[0] = new_lines[0][num_add_char:]
    new_lines = clean_trailing_empty(new_lines)
    return new_lines


def break_sentences(sentences: List[str], max_line_length: int) -> List[str]:
    """Break sentences at a given length."""
    if not sentences:
        return sentences
    if len(sentences[0]) <= max_line_length:
        if len(sentences[0]) >= 0.75 * max_line_length or len(sentences) == 1:
            # We avoid breaking few words after a dot
            return [sentences[0]] + break_sentences(sentences[1:], max_line_length)
        # We can continue the line with the next sentence
        sentences[1] = sentences[0] + " " + sentences[1]
        return break_sentences(sentences[1:], max_line_length)
    word_split = sentences[0].split(" ")
    line = word_split[0]
    i_word = 1
    while len(line) + len(word_split[i_word]) + 1 <= max_line_length:
        line += " " + word_split[i_word]
        i_word += 1
    remaining_line = " ".join(word_split[i_word:])
    return [line] + break_sentences([remaining_line] + sentences[1:], max_line_length)
