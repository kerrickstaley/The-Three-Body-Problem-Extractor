#!/usr/bin/env python3
import argparse
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(
    description='Reformat text from a PDF copy of the novel The Three Body Problem (三体) by Cixin Liu')
parser.add_argument('pdf_file', help='Path to PDF file')


class State:
  def __init__(self):
    # 0 indicates we have not yet reached page 1, otherwise pagenum indicates which page we're processing
    self.page_num = 0
    # whether we've printed the page number for the current page
    # we print the page number after finishing the paragraph from the previous page
    self.has_output_page_num = 0


class BookDescription:
  # ideally this is pluggable so we can eventually process other books in the series
  # not intended to generalize to all books, just the San Ti series
  def __init__(self, start_text, illustration_pages, ignore_lines):
    self.start_text = start_text
    self.illustration_pages = illustration_pages
    self.ignore_lines = ignore_lines


book1_description = BookDescription(
    '汪淼觉得',
    [83, 104, 105, 158, 159, 208, 209],
    [
      '中国科幻基石丛书',
      '地球往事·三体',
    ])

EVEN_INDENTATION = 11


def process_line(line, state, desc):
  # process a single line, update `state`, and return the text that should be output

  # find start of text
  if state.page_num == 0:
    if not line.strip().startswith(desc.start_text):
      return
    state.page_num = 1

  # process page update
  if line.strip() == str(state.page_num):
    state.page_num += 1
    # we potentially need to update the page number multiple times for a given line of text, hence this loop
    while state.page_num in desc.illustration_pages:
      state.page_num += 1
    state.has_output_page_num = False
    return

  # process empty lines
  if not line.strip():
    return

  # process ignored lines
  if line.strip() in desc.ignore_lines:
    return

  # remove '\x0c' character, which occurs at the start of new pages (but we don't actually need it)
  line = line.lstrip('\x0c')

  indentation = len(line) - len(line.lstrip())

  # de-indent even pages
  if state.page_num % 2 == 0:
    # sanity check
    if indentation < EVEN_INDENTATION:
      raise Exception(f'even-page line with less than EVEN_INDENTATION: {line.strip()}')
    indentation -= EVEN_INDENTATION

  if indentation == 0 or indentation > 4:
    # continuation of current paragraph
    return line.strip()
  else:
    # new paragraph
    # TODO split the formatting logic out of this function
    rv = '\n\n' + line.strip()
    if not state.has_output_page_num:
      rv = f'\n\nPage {state.page_num}{rv}'
      state.has_output_page_num = True
    return rv


def run_pdftotext(input_file):
  output_file = tempfile.mktemp()

  try:
    subprocess.check_call(['pdftotext', '-layout', input_file, output_file])
  except OSError as e:
    if e.errno == 2:
      print('Error: you need to install the program pdftotext', file=sys.stderr)
    raise

  return output_file


if __name__ == '__main__':
  args = parser.parse_args()

  text_file = run_pdftotext(args.pdf_file)

  state = State()
  for line in open(text_file):
    txt = process_line(line, state, book1_description)
    if txt:
      print(txt, end='')

