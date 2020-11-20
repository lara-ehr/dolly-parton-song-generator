# Dolly Parton Song Generator

Neural network that generates Dolly Parton songs. This is a work in progress!

## Aim: Shining an AI spotlight on the songwriting genius of Dolly Parton

Country legend Dolly Parton has been performing since she was 10 years old and to date, has written over 3000 songs -- often romping across genre boundaries. But unlike fellow country music songwriting giants Johnny Cash, Hank Williams or John Prine, she rarely gets credit for her sophisticated lyrics. This project is out to change that. And hopefully provide a little competition in the songwriting department.

## Approach

- **Corpus building:** I scraped as many songs as I could find off a crowd-sourced [lyrics website.](metrolyrics.com) At >600 unique songs, this is around 20% of Dolly's œuvre, but I hope to get my hands on more data in the future.
  - Tools: BeautifulSoup, SpaCy
- **Analysis: *(under development)*** A quantitative analysis of Dolly's lyrical genius.
  - Tools: SpaCy
- **Neural network: *(under development)*** I trained a neural network on sequences of Dolly lyrics.
  - Tools: Keras/Tensorflow
- **Songwriter script: *(under development)*** This script takes user input and writes an entire new song.
  - Tools: Keras/Tensorflow, SpaCy

## Run your own generator

Customisability is under development! Future plan: Adapt this so that anyone can download their favourite artist's work and generate more songs.

## Tools
- Keras/Tensorflow
- SpaCy
- BeautifulSoup

## Further Material for Dolly Fans

- ["Dolly Parton's America"](https://www.wnycstudios.org/podcasts/dolly-partons-america)
  - Podcast about Dolly's life, songs and unlikely status as a feminist who doesn't call herself a feminist.
- [*She Come By It Natural* by Sarah Smarsh](https://sarahsmarsh.com/she-come-by-it-natural)
  - Read an excerpt on Slate [here.](https://slate.com/culture/2020/10/dolly-parton-biography-she-come-by-it-natural-excerpt.html)
