Þ    /                      #        1  ]   O  ±   ­     _     ~  #        ¸     Ë  õ   Þ  K   Ô        ~   -  s   ¬           <     V     o  :     c   Â     &     >  
   R  >   ]          ¤     ³     Ë     ç     û  ò  	  .   ú  $   )     N  n  `    Ï  O  g  +  ·  !   ã       [   !  H   }  F   Æ          )  	   F    P  $   Ø     ý  S     ²   l          <     I     h     u  ê     K   s  	   ¿  r   É  {   <     ¸     Ô     í  !     6   %  Z   \     ·     Í     ã  9   ê     $     +     8  *   T       
     ½  £  -   a            9  ©  v  ã  R  Z   =  ­!  "   ë"     #  Q   '#  C   y#  D   ½#  #   $     &$     A$   + ``data``: Loaded dictionary data. + ``mean_X``: Average result. + ``ref_sig``: Reference signals of one stimulus. The dimention is (2N :raw-html:`&#215;` L). + ``sorted_X``: Sorted ``X``. + ``sort_idx``: List of indices that can transfer ``X`` to ``sorted_X``. + ``return_idx``: List of indices that can transfer ``sorted_X`` to ``X``. + ``sum_X``: Summation result. Computation functions Dictionary data that will be saved. Download functions Download one file. Generate sine-cosine-based reference signal of one stimulus. This function is similar as `"get_ref_sig" function <#get_ref_sig>`_ in dataset class. But this function is more flexible, requires more input parameters, and is only for one stimulus. Hash code of the downloaded file. Set ``None`` if the hash code is unknown. IO functions Iteratively calculate average value of a list. If the input list contains lists, these contained lists will be averaged first. Iteratively sum all values in a list. If the input list contains lists, these contained lists will be summed first. List that will be averaged. List that will be sorted. List that will be sumed. Load a local data file. Local data path including the absolute path and file name. Local path for storing the downloaded file. The path should be an absolute path with the file name. One stimulus frequency. One stimulus phase. Parameters Path of saving file including the absolute path and file name. Returns Sampling rate. Save a dictionary data. Signal length (in samples). Sort the given list Source URL. There are two options of the local data type:  + ``'mat'``: Local data is a matlab ``.mat`` file. The varaible names are the key values of the dictionary. The variable values are the values of the dictionary. If use this option, this function will work like `"scipy.io.loadmat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html>`_ or `"mat73.loadmat" <https://github.com/skjerns/mat7.3>`_.  + ``'np'``: Local data is a numpy ``.npy`` binary file. If use this option, this function will work like `"numpy.load" <https://numpy.org/doc/stable/reference/generated/numpy.load.html>`_. For pickle ``.pkl`` binary file, you may directly use `"pickle.load" <https://docs.python.org/3/library/pickle.html#pickle.load>`_ to load the data. There are two options of the saving data type: Total number of harmonic components. Utility Functions ``'mat'``: Local data is a matlab ``.mat`` file. The varaible names are the key values of the dictionary. The variable values are the values of the dictionary. If use this option, this function will work like `"scipy.io.loadmat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html>`_ or `"mat73.loadmat" <https://github.com/skjerns/mat7.3>`_. ``'mat'``: Save data as a matlab ``.mat`` file. The varaible names are the key values of the dictionary. The variable values are the values of the dictionary. If use this option, this function will work like `"scipy.io.savemat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.savemat.html>`_. If the data cannot be saved as ``.mat`` file, the data will be saved as numpy ``.npy`` binary file. ``'np'``: Local data is a numpy ``.npy`` binary file. If use this option, this function will work like `"numpy.load" <https://numpy.org/doc/stable/reference/generated/numpy.load.html>`_. For pickle ``.pkl`` binary file, you may directly use `"pickle.load" <https://docs.python.org/3/library/pickle.html#pickle.load>`_ to load the data. ``'np'``: Save data as a numpy ``.npy`` binary file. If use this option, this function will work like `"numpy.save" <https://numpy.org/doc/stable/reference/generated/numpy.save.html>`_. If the data cannot be saved as numpy ``.npy`` binary file, the data will be saved as pickle ``.pkl`` binary file. ``data``: Loaded dictionary data. ``mean_X``: Average result. ``ref_sig``: Reference signals of one stimulus. The dimention is (2N :raw-html:`&#215;` L). ``return_idx``: List of indices that can transfer ``sorted_X`` to ``X``. ``sort_idx``: List of indices that can transfer ``X`` to ``sorted_X``. ``sorted_X``: Sorted ``X``. ``sum_X``: Summation result. save_type Project-Id-Version: SSVEP Analysis Toolbox 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2022-10-13 10:25+0800
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: zh_CN
Language-Team: zh_CN <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.1
 + ``data``: å è½½çå­å¸æä»¶ã + ``mean_X``: å¹³åå¼ã + ``ref_sig``: ä¸ä¸ªåºæ¿çåèä¿¡å·ï¼å½¢ç¶ä¸º (2N :raw-html:`&#215;` L)ã + ``sorted_X``: æåºåç ``X``ã + ``sort_idx``: å° ``X`` åæ¢ä¸º ``sorted_X`` çç´¢å¼æ°åè¡¨ã + ``return_idx``: å° ``sorted_X`` åæ¢ä¸º ``X`` çç´¢å¼åè¡¨ã + ``sum_X``: æ±åç»æã è®¡ç®å½æ° å°è¦ä¿å­çå­å¸æ°æ®ã ä¸è½½å½æ° ä¸è½½ä¸ä¸ªæä»¶ ä¸ºä¸ä¸ªåºæ¿çææ­£ä½å¼¦åèä¿¡å·ãè¿ä¸ªå½æ°ç±»ä¼¼äºæ°æ®éç±»ä¸­ç `"get_ref_sig" å½æ° <#get_ref_sig>`_ãä½æ¯æ­¤å½æ°æ´çµæ´»ï¼ä½ä¹éè¦æ´å¤è¾å¥åæ°ï¼å¹¶ä¸ä»è½ä¸ºä¸ä¸ªåºæ¿çæåèä¿¡å·ã ä¸è½½æä»¶çåå¸å¼ãå¦æåå¸å¼æªç¥å¯ä»¥è®¾ç½®ä¸º ``None``ã IO å½æ° å¨ä¸ä¸ªåè¡¨ä¸­å¾ªç¯è®¡ç®å¹³åå¼ãå¦æè¾å¥åè¡¨åå«åè¡¨ï¼è¿äºè¢«åå«çåè¡¨åè¢«å¹³åã å¨ä¸ä¸ªåè¡¨ä¸­å¾ªç¯è®¡ç®ææå¼å¾å åãå¦æè¾å¥åè¡¨åå«åè¡¨ï¼è¿äºè¢«åå«çåè¡¨åè¢«æ±åã å°è¢«æ±å¹³åçåè¡¨ã å°è¢«æåºçåè¡¨ã å°è¢«æ±åçåè¡¨ å è½½ä¸ä¸ªæ¬å°æ°æ®æä»¶ã æ¬å°æ°æ®è·¯å¾ï¼åæ¬æä»¶åçç»å¯¹è·¯å¾ã ç¨æ¥ä¿å­ä¸è½½æä»¶çæ¬å°è·¯å¾ãè·¯å¾å¿é¡»æ¯åå«æä»¶åçç»å¯¹è·¯å¾ã ä¸ä¸ªåºæ¿é¢çã ä¸ä¸ªåºæ¿ç¸ä½ã åæ° ä¿å­æä»¶çè·¯å¾ï¼åå«æä»¶åçç»å¯¹è·¯å¾ã è¿å éæ ·çã ä¿å­ä¸ä¸ªå­å¸æ°æ®ã ä¿¡å·é¿åº¦ï¼ä»¥éæ ·ç¹ä¸ºåä½ï¼ã å¯¹ç»å®çåè¡¨æåº æº URLã æä¸¤ä¸ªå¯éæ©çæ¬å°æ°æ®ç±»åï¼  + ``'mat'``: æ¬å°æ°æ®ä¸º ``.mat`` æä»¶ãåéåä¸ºå­å¸çé®åï¼åéå¼ä¸ºå­å¸çé®å¼ãå¦æä½¿ç¨æ­¤éé¡¹ï¼æ­¤å½æ°å°ç±»ä¼¼äº`"scipy.io.loadmat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html>`_ æè `"mat73.loadmat" <https://github.com/skjerns/mat7.3>`_ã  + ``'np'``: æ¬å°æ°æ®ä¸º numpy ç `.npy`` äºè¿å¶æä»¶ï¼å¦æä½¿ç¨æ­¤éé¡¹ï¼æ­¤å½æ°ç±»ä¼¼äº `"numpy.load" <https://numpy.org/doc/stable/reference/generated/numpy.load.html>`_. å¯¹äº pickle ç ``.pkl`` çäºè¿å¶æä»¶ï¼ä½ å¯ä»¥ç´æ¥ä½¿ç¨ `"pickle.load" <https://docs.python.org/3/library/pickle.html#pickle.load>`_ã ç°å¨æä¸¤ç§å¯éçä¿å­æ°æ®æ ¼å¼ï¼ è°æ³¢æ°ã å®ç¨å½æ° ``'mat'``: æ¬å°æ°æ®ä¸º ``.mat`` æä»¶ãåéåä¸ºå­å¸çé®åï¼åéå¼ä¸ºå­å¸çé®å¼ãå¦æä½¿ç¨æ­¤éé¡¹ï¼æ­¤å½æ°å°ç±»ä¼¼äº`"scipy.io.loadmat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html>`_ æè `"mat73.loadmat" <https://github.com/skjerns/mat7.3>`_ã ``'mat'``: ä¿å­æ°æ®ä¸º matlab ç ``.mat`` æä»¶ãåéåä¸ºå­å¸çé®åãåéçå¼ä¸ºå­å¸ä¸­å¯¹åºå»ºçå¼ãå¦æä½¿ç¨æ­¤æ ¼å¼ï¼æ­¤å½æ°ç±»ä¼¼äº `"scipy.io.savemat" <https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.savemat.html>`_ãå¦ææ°æ®æ æ³ä¿å­ä¸º ``.mat`` æä»¶ï¼æ°æ®å°ä¿å­ä¸º numpy ç ``.npy`` äºè¿å¶æä»¶ã ``'np'``: æ¬å°æ°æ®ä¸º numpy ç `.npy`` äºè¿å¶æä»¶ï¼å¦æä½¿ç¨æ­¤éé¡¹ï¼æ­¤å½æ°ç±»ä¼¼äº `"numpy.load" <https://numpy.org/doc/stable/reference/generated/numpy.load.html>`_. å¯¹äº pickle ç ``.pkl`` çäºè¿å¶æä»¶ï¼ä½ å¯ä»¥ç´æ¥ä½¿ç¨ `"pickle.load" <https://docs.python.org/3/library/pickle.html#pickle.load>`_ã ``'np'``: ä¿å­æ°æ®ä¸º numpy ç `.npy`` äºè¿å¶æä»¶ãå¦æä½¿ç¨æ­¤æ ¼å¼ï¼æ­¤å½æ°ç±»ä¼¼äº `"numpy.save" <https://numpy.org/doc/stable/reference/generated/numpy.save.html>`_ãå¦ææ°æ®æ æ³ä¿å­ä¸º numpy ç `.npy`` äºè¿å¶æä»¶ï¼æ°æ®å°è¢«ä¿å­ä¸º pickle ç ``.pkl`` çäºè¿å¶æä»¶ã ``data``: å è½½çå­å¸æä»¶ã ``mean_X``: å¹³åå¼ã ``ref_sig``: ä¸ä¸ªåºæ¿çåèä¿¡å·ï¼å½¢ç¶ä¸º (2N :raw-html:`&#215;` L)ã ``return_idx``: å° ``sorted_X`` åæ¢ä¸º ``X`` çç´¢å¼åè¡¨ã ``sort_idx``: å° ``X`` åæ¢ä¸º ``sorted_X`` çç´¢å¼æ°åè¡¨ã ``sorted_X``: æåºåç ``X``ã ``sum_X``: æ±åç»æã ä¿å­æ ¼å¼ 