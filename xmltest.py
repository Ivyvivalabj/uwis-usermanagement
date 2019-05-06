#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import xml.sax
 
class MovieHandler( xml.sax.ContentHandler ):
   def __init__(self):
      self.CurrentData = ""
      self.type = ""
   # 元素开始事件处理
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      
   # 元素结束事件处理
   def endElement(self, tag):
      print(self.CurrentData)
      if self.CurrentData == "type":
         global typeG
         typeG = self.type
         # print(self.type)
   # 内容事件处理
   def characters(self, content):
      # print(self.CurrentData)
      if self.CurrentData == "type":
         self.type = content
      
      
  
if ( __name__ == "__main__"):
   # 创建一个 XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   # 重写 ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler(Handler)
   parser.parse("movies.xml")
   print("typeG:"+typeG)