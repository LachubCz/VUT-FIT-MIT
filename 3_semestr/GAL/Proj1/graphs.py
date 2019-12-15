g_1 = {"a" : {"e", "b"},
       "b" : {"a", "e", "f", "c"},
       "c" : {"b", "g", "h"},
       "d" : {"e", "l"},
       "e" : {"a", "b", "i", "d"},
       "f" : {"b", "g"},
       "g" : {"c", "f", "j"},
       "h" : {"c", "k", "o"},
       "i" : {"e", "j", "l"},
       "j" : {"i", "g", "k"},
       "k" : {"j", "h", "o", "m"},
       "l" : {"d", "i", "m"},
       "m" : {"l", "k", "n"},
       "n" : {"m", "o"},
       "o" : {"h", "k", "n"}
      } #planar

g_2 = {"a" : {"e", "b"},
       "b" : {"a", "e", "f", "c"},
       "c" : {"b", "g", "h"},
       "d" : {"e", "l"},
       "e" : {"a", "b", "i", "d"},
       "f" : {"b", "g", "k"},
       "g" : {"c", "f", "j"},
       "h" : {"c", "k", "o"},
       "i" : {"e", "j", "l"},
       "j" : {"i", "g", "k"},
       "k" : {"j", "h", "o", "m", "f"},
       "l" : {"d", "i", "m"},
       "m" : {"l", "k", "n"},
       "n" : {"m", "o"},
       "o" : {"h", "k", "n"}
      } #non planar

g_3 = {"a" : {"e", "b"},
       "b" : {"a", "e", "f", "c"},
       "c" : {"b", "g"},
       "d" : {"l"},
       "e" : {"a", "b"},
       "f" : {"b", "g"},
       "g" : {"c", "f"},
       "h" : {"k", "o"},
       "i" : {"j", "l"},
       "j" : {"i", "k"},
       "k" : {"j", "h", "o", "m"},
       "l" : {"d", "i", "m"},
       "m" : {"l", "k", "n"},
       "n" : {"m", "o"},
       "o" : {"h", "k", "n"}
      } #planar, multiple components

g_4 = {"a" : {"b"},
       "b" : {"a", "c", "d"},
       "c" : {"b"},
       "d" : {"b", "d"},
       "e" : {}
      } #planar, self loop

g_5 = {"a" : {"f", "h", "b"},
       "b" : {"c", "a", "g"},
       "c" : {"h", "b", "d"},
       "h" : {"a", "c", "e"},
       "e" : {"d", "h", "f"},
       "f" : {"e", "g", "a"},
       "g" : {"b", "d", "f"},
       "d" : {"g", "e", "c"}
      } #planar, lowpoints test
    
g_6 = {"a" : {"b", "d"}, 
       "b" : {"a", "c"}, 
       "c" : {"b", "d", "e", "f"}, 
       "d" : {"a", "c"}, 
       "e" : {"c", "f"}, 
       "f" : {"c", "e"}
      } #planar, multiple bicomponents

K_5 = {"a" : {"b", "c", "d", "e"}, 
       "b" : {"a", "c", "d", "e"}, 
       "c" : {"a", "b", "d", "e"}, 
       "d" : {"a", "b", "c", "e"}, 
       "e" : {"a", "b", "c", "d"}
       }

K_3_3 = {"a" : {"d", "e", "f"}, 
         "b" : {"d", "e", "f"}, 
         "c" : {"d", "e", "f"}, 
         "d" : {"a", "b", "c"}, 
         "e" : {"a", "b", "c"},
         "f" : {"a", "b", "c"}
        }