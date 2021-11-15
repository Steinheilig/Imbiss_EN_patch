# -*- coding: utf-8 -*-
"""
English patch for the German game:
"Imbiss" v. 5.4 by T. Bauer for IBM PC, 1991, Public Domain

ToDo:
    Quick& Dirty implementation ... Code refactoring/commenting needed
    Some English spell checking needed... at some point..
    Info and stop menu not yet translated... 

@author: Steinheilig, 2021
"""

import pickle

def comp_files(f1,f2,save_diff_fn):
    ## compare two file byte by byte
    # generate substitution list 
    sub = []
    sub_idx = []
    o = open(f1, 'rb')
    with open(f2, 'rb') as f:
       while True:
          byte_1 = o.read(1)
          if not byte_1:
             break
          byte_2 = f.read(1)
          if not byte_2:
             print("WARNING: Size of files differ 1>2")                                 
          if byte_1 != byte_2:
             print(f.tell(),byte_1,'vs',byte_2)    
             sub.append(byte_2)
             sub_idx.append(f.tell())
             
    f.close()
    o.close()
    
    sample_list = [sub,sub_idx]
    open_file = open(save_diff_fn, "wb")
    pickle.dump(sample_list, open_file)
    open_file.close()
   
def patch_file(in_f,out_f,save_diff_fn):
    ## creates pachted file f_out from f_in using save_diff_fn substitution list 
    open_file = open(save_diff_fn, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    sub = loaded_list[0]
    sub_idx = loaded_list[1]    
    
    pos_list = 0 
    o = open(out_f, 'wb')
    with open(in_f, 'rb') as f:
       while True:
          byte_1 = f.read(1)
          if not byte_1:
             break
          if f.tell() == sub_idx[pos_list]:
             byte_2 = sub[pos_list]
             pos_list += 1
             print("sub:",byte_1,"->",byte_2,'at',f.tell())
             if pos_list == len(sub):
                 print("all subs done...")
                 pos_list = 0 
          else:
             byte_2 = byte_1
          o.write(byte_2)
    f.close()
    o.close()
   

comp_files('C:\EigeneLokaleDaten\Imbiss\game\imbiss.exe','C:\EigeneLokaleDaten\Imbiss\game\imbiss2.exe','C:\EigeneLokaleDaten\Imbiss\patch\patch_data_r2.pkl')
patch_file('C:\EigeneLokaleDaten\Imbiss\game\imbiss.exe','C:\EigeneLokaleDaten\Imbiss\game\imbiss_patch2.exe','C:\EigeneLokaleDaten\Imbiss\patch\patch_data_r2.pkl')

