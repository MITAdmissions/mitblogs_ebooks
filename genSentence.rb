# encoding: UTF-8

require 'rubygems'
require 'twitter'
require 'punkt-segmenter'
#require 'twitter_init'
require 'markov'
require 'htmlentities'

#settings
$rand_limit ||= 10
$markov_index ||= 2
rand_key = rand($rand_limit)

#input

text = IO.read('someblogs.txt')

#how to end sentences

CLOSING_PUNCTUATION = ['.', ';', ':', '?', '!']

def random_closing_punctuation
  CLOSING_PUNCTUATION[rand(CLOSING_PUNCTUATION.length)]
end

markov = MarkovChainer.new($markov_index)
tokenizer = Punkt::SentenceTokenizer.new(text)  # init with corpus of all sentences

source_tweets.each do |twt|
  next if twt.nil? || twt == ''
  sentences = tokenizer.sentences_from_text(twt, :output => :sentences_text)
  sentences.each do |sentence|
    next if sentence =~ /@/
    markov.add_sentence(sentence)
  end
end

puts sentences