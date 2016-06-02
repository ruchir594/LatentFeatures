require 'nokogiri'
require 'open-uri'


aFile = File.open("data/testsent.txt", "r+")
  a = aFile.read
aFile.close
puts a.class
words = a.split(/\W+/)
puts words[0]
puts words[1]
