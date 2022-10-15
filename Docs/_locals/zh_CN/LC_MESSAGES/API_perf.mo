��    j      l              �  �   �  �   H  �   H  �   &	  l   �	  �   Z
         &  L   E  �   �  �        �  "   �     �  	   �  '     $   *    O  }   S  o   �  �   A  ;   �  �     �   �  2   ^  �   �  R    ;   j     �  !   �  %   �  %     )   .  n   X  '   �  1   �  3   !     U  (   g  "   �  <   �  3   �  1   $     V  (   o  0  �  
   �     �     �        ;     �   K  �     �   �  4   q  7   �     �     �  L   f  #   �     �  �  �  �   �     z   ,   �   _   �   ^   !  r   {!  �   �!  �   �"  �   Z#     M$  "   _$  #   �$     �$     �$  (   �$  (   	%  v   2%  �   �%  �   8&  �   �&  ,   �'  U   �'  `   (  b   q(  �   �(  �   a)  g   &*  b   �*  F   �*  z   8+  �   �+  �   S,  �   �,  �   }-  �   .  �   �.  8   6/  "   o/  �   �/  v   U0  \   �0  �   )1  ]   �1  �  (2  \   �3  �   4  �   �4  �   �5  ?   �6  E   �6     >7  0   Z7  C   �7  �   �7  �   \8     �8     �8     9  	   59  *   ?9  #   j9  �   �9  y   �:  s   ;  k   z;  B   �;  �   )<  �   �<  ?   \=  �   �=  �   .>  F   �>     &?     9?  &   R?  &   y?  0   �?  l   �?  *   >@  $   i@  $   �@     �@  *   �@  '   �@  <   A  *   VA  $   �A     �A     �A  �   �A     �B     �B     �B     �B  H   �B  �   2C  �   �C  �   tD  6   E  1   RE     �E  k   �E  V   �E     NF     jF  �  wF  r   @H     �H  !   �H  O   �H  U   5I  h   �I  �   �I  c   �J  �   @K     L  *   L  &   CL  !   jL     �L  *   �L  *   �L  v   �L  k   pM  d   �M  �   AN  )    O  ;   JO  B   �O  v   �O  }   @P  �   �P  Z   dQ  j   �Q  1   *R  x   \R  �   �R  �   aS  �   �S  k   rT  z   �T  �   YU  5   �U     V  �   2V  q   �V  T   DW  �   �W  \   (X   *Please ignore this parameter and leave this parameter as the default value. The function related to this parameter is under development.* + ``X``: List of all EEG trials. + ``Y``: List of all labels. + ``ref_sig``: This function will use the first dataset in ``dataset_idx`` to generate reference signals. + ``freqs``: List of stimulus frequencies corresponding to generated reference signals. + ``acc``: Classification accuracy. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal length). + ``itr``: ITR. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal length). + ``confusion_matrix``: Confusion matrices. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal lengths :raw-html:`&#215;` true classes :raw-html:`&#215;` predicted classes). A list of datasets. Each element is a instance of one dataset class introduced in `"Datasets" <#datasets>`_. A list of recognition models/methods. Each element is a instance of one recognition model/method class introduced in `"Recognition algorithms" <#recognition-algorithms>`_. A list of trials. The format is A list of trials. The format is  .. code-block:: python      [[train_trial_info, test_trial_info],      [train_trial_info, test_trial_info],      ...,      [train_trial_info, test_trial_info]]  where ``train_trial_info`` and ``test_trial_info`` are instances of the ``TrialInfo`` class. Based on the trial information, get all data, labels, and reference signals. Calculate confusion matrices of ``BaseEvaluator`` whose ``trial_container`` is generated by ``gen_trials_onedataset_individual_diffsiglen``. Calculate evaluation performance of ``BaseEvaluator`` whose ``trial_container`` is generated by ``gen_trials_onedataset_individual_diffsiglen``. Dataset index. Dataset index. One integer number. Default is ``False``. Evaluator Figure size. Default is ``[6.4, 4.8]``. Format of lines. Default is ``'-'``. Generate ``trial_container`` for ``BaseEvaluator``. These evaluation trials only use one dataset. One block is used for testing. Other blocks for training. All blocks will be tested one by one. All subjects will be evaluated one by one for each signal length. If ``"train"``, evaluate confusion matrices of training trials. If ``"test"``, evaluate confusion matrices of testing trials. If ``"train"``, evaluate performance of training trials. If ``"test"``, evaluate performance of testing trials. If ``'std'``, calculate the variation using the standard derivation. If ``'95ci'``, calculate the variation using the 95% confidence interval. If ``False``, ``trained_model_container`` is an empty list. If ``True``, a progress bar will be shown in console to illustrate the evaluation process. Otherwise, the progress bar will be shown. Default is ``True``. If ``True``, stimulus phases of generating reference signals will be set as 0 during the evalution. Otherwise, stimulus phases will use the dataset information. Default is ``False``. If ``True``, the order of trials will be shuffled. If ``True``, trained models in all trials will be stored in ``trained_model_container``. The format of ``trained_model_container`` is If ``True``, trained models in all trials will be stored in ``trained_model_container``. The format of ``trained_model_container`` is  .. code-block:: python      [[trained_model_method_1, trained_model_method_2, ...],      [trained_model_method_1, trained_model_method_2, ...],      ...,      [trained_model_method_1, trained_model_method_2, ...]]  where ``trained_model_method_1``, ``trained_model_method_2``, ... are instances of recognition model/method classes, which order is same as ``model_container``.  If ``False``, ``trained_model_container`` is an empty list.  Default is ``False``. If ``True``, trials will be shuffled. Default is ``False``. Initialize the evaluator. It contains following attributes: Label of x axis. Default is ``None``. Label of y axis. Default is ``None``. Latency time (in second). A float number. Latency time (in second). A float number. If ``None``, the suggested latency time of the dataset will be used. List of bar names. Default is ``None``. List of block indices. A list of integer numbers. List of channel indices. A list of integer numbers. List of datasets. List of line names. Default is ``None``. List of signal lengths (in second) List of signal lengths (in second). A list of float numbers. List of subject indices. A list of integer numbers. List of trial indices. A list of integer numbers. List of variable values. Number of harmonics. One integer number. Number of threadings using for recognition methods. If the given value is larger than 1, the parallel computation will be applied to improve the computational speed. Default is ``None``, which means the parallel computation will not be applied. The evaluator will reset ``n_jobs`` in recognition methods. Parameters Performance Container Performance Evalution Plot Functions Plot bars with error bars. Each group plots one color bars. Plot data. The shape is (groups :raw-html:`&#215;` observations :raw-html:`&#215;` variables). The bar height is the mean across observations. The error bar is the variation across observations. Plot data. The shape is (groups :raw-html:`&#215;` observations :raw-html:`&#215;` variables). The line is the mean across observations. The shadow is the variation across observations. Plot data. The shape is (observations :raw-html:`&#215;` variables). The bar height is the mean across observations. The error bar is the variation across observations. Plot shadow lines. Each group plots one shadow line. Push one dataset information into the trial information Returns Run the evaluation process. Performance will be stored in ``performance_container``. The format of ``performance_container`` is Saving models by setting ``save_model`` as ``True`` may occupy large memory. Separate distence of adjacent bars. Supplementary functions The ``BaseEvaluator`` class is a trial based evaluator. Evaluator contains several evaluation trials and evaluate performance trial by trial. Each trial contains several training and testing trials. In each trial, the ``BaseEvaluator`` uses the given training trials to train all models one by one and then tests their performance in testing trials. The training time, evaluation time, ture labels and predicted labels will be stored. The recognition accuracies and ITRs can be further computed. The harmonic number is used to generate reference signals. This input parameter will update ``harmonic_num`` of the trial information. One integer number. The instance itself. The instance of the class ``BaseEvaluator``. The instances of this class are the basic elements of ``trial_container`` in ``BaseEvaluator``. The instances of this class are the element of ``performance_container`` in ``BaseEvaluator``. The signal length (in second). This input parameter will update ``tw`` of the trial information. One float number. This ``TrialInfo`` will only use the first dataset to generate reference signals. If datasets have different stimuli, please separate them into different trials. The more safety way is that one ``TrialInfo`` cotains only one dataset. This function is similar as ``bar_plot_with_errorbar``. But this function only plots one group data and does not plot error bars. This toolbox provides a ``BaseEvaluator`` class for evaluating recognition performance. Users can use this class as the father class to write your own evaluator or use the above given functions or classes to write your own evaluation process. Trial Information Whether grid. Default is ``True``. X tick labels. Default is ``None``. ``X``: List of all EEG trials. ``Y``: List of all labels. ``[min_x, max_x]``. Default is ``None``. ``[min_y, max_y]``. Default is ``None``. ``acc``: Classification accuracy. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal length). ``block_idx``: A list of all datasets' block index list. The format is same as ``sub_idx`` but the integer numbers in lists are block indices. ``ch_idx``: A list of all datasets' channel index list. The format is same as ``sub_idx`` but the integer numbers in lists are channel indices. ``confusion_matrix``: Confusion matrices. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal lengths :raw-html:`&#215;` true classes :raw-html:`&#215;` predicted classes). ``dataset_idx``: A list of dataset indeices. ``freqs``: List of stimulus frequencies corresponding to generated reference signals. ``harmonic_num``: The harmonic number is used to generate reference signals. One integer number. ``itr``: ITR. The shape is (methods :raw-html:`&#215;` subjects :raw-html:`&#215;` signal length). ``pred_label_test``: The list of predicted labels of testing trials is stored in this attribute. The format is same as ``true_label_train``. ``pred_label_train``: After training, to evaluate the training performance, the list of predicted labels of training trials is stored in this attribute. The format is same as ``true_label_train``. ``ref_sig``: This function will use the first dataset in ``dataset_idx`` to generate reference signals. ``shuffle``: A list of shuffle flag. Each element is a bool value denoting whether shuffle trials. ``sub_idx``: A list of all datasets' subject index list. The format is ``t_latency``: A list of latency times of datasets. Each element is a float number denoting a latency time of one dataset. ``test_time_test``: A list of storing time of using the testing trials to test the model. Each element in the list is one testing time of one evaluation trial. ``test_time_train``: A list of storing time of using the training trials to testing the model. Each element in the list is one testing time of one evaluation trial. ``train_time``: A list of storing time of training the model. Each element in the list is one training time of one evaluation trial. ``trial_idx``: A list of all datasets' trial index list. The format is same as ``sub_idx`` but the integer numbers in lists are trial indices. ``true_label_test``: The list of true labels of testing trials is stored in this attribute. The format is same as ``true_label_train``. ``true_label_train``: After training, to evaluate the training performance, the list of true labels of training trials is stored in this attribute. The format is ``tw``: The signal length (in second). One float number. dataset index. One integer number. where ``performance_method_1``, ``performance_method_2``, ... are instances of the ``PerformanceContainer`` class for different recognition models/methods. The order follows ``model_container``. where ``sub_idx_1``, ``sub_idx_2``, ... are subject indices for different datasets. The order follows ``dataset_idx``. where ``train_trial_info`` and ``test_trial_info`` are instances of the ``TrialInfo`` class. where ``trained_model_method_1``, ``trained_model_method_2``, ... are instances of recognition model/method classes, which order is same as ``model_container``. where ``true_label_1``, ``true_label_2``, ... are true labels of different evaluation trials. Project-Id-Version: SSVEP Analysis Toolbox 
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
 *请忽略此参数并保留此参数为默认值。有关此参数的功能还在开发中* + ``X``: 全部 EEG trial 列表。 + ``Y``: 标签列表。 + ``ref_sig``: 利用 ``dataset_idx`` 中的第一个数据集的信息生成参考信号。 + ``freqs``: 生成参考信号对应的刺激频率列表。 + ``acc``: 分类准确率，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数)。 + ``itr``: 信息传输率，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数)。 + ``confusion_matrix``: 混淆矩阵，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数 :raw-html:`&#215;` 标签（真实标签）数 :raw-html:`&#215;` 标签（识别标签）数)。 数据集列表。每个元素是一个数据集类的实例。 识别算法列表。每个元素是一个识别算法类的实例。 trial 的列表。格式为 trial 列表。更具体的请参阅英文版。 基于 trial 信息，获取全部数据、标签、参考信号。 计算 ``BaseEvaluator`` 的混淆矩阵，其中 ``trial_container`` 必须是由 ``gen_trials_onedataset_individual_diffsiglen`` 生成。 计算 ``BaseEvaluator`` 的评估表现，其中的 ``trial_container`` 必须是由 ``gen_trials_onedataset_individual_diffsiglen`` 生成。 数据集索引数 数据集索引数，整数。 默认为 ``False``。 评估器 图片大小，默认为 ``[6.4, 4.8]``。 线的格式，默认为 ``'-'``。 为 ``BaseEvaluator`` 生成 ``trial_container``。这些评估 trial 仅包含一个数据集。一个 block 用于测试，其余 block 用于测试。所有 block 一个个测试。对于不同的信号长度，所有受试者将一个个被评估。 如果 ``"train"``，将会计算训练 trial 的混淆矩阵。如果 ``"test"``，计算测试 trial 的混淆矩阵。 如果 ``"train"``，将会评估训练 trial 的表现。如果 ``"test"``，将会评估测试 trial 的表现。 如果 ``'std'``，使用标准差计算变化。如果 ``'95ci'``，使用 95% 置信区间计算变化。 如果 ``False``， ``trained_model_container`` 是一个空集。 如果 ``True``，一个进度条将会显示在终端上来显示评估进度。否则，进度条将不会显示。默认为 ``True``。 如果 ``True``，在评估中生成的参考信号的刺激相位将会被设定为0。否则，刺激相位将会使用数据集中的信息。默认为 ``False``。 如果 ``True``，trial 的顺序将会被重新随机打乱。 如果 ``True``，所有 trial 的训练得到的模型将会被保存在 ``trained_model_container``。 ``trained_model_container`` 的格式为 如果 ``True``，所有 trial 的训练得到的模型将会被保存在 ``trained_model_container``。否则， ``trained_model_container`` 是空集。默认为 ``False``。 如果 ``True``，trial 将会被重新打乱。默认为 ``False``。 初始化评估器 它包含下列属性： x 轴的标签，默认为 ``None``。 y 轴的列表，默认为 ``None``。 延迟时间（以秒为单位）。浮点数。 延迟时间（以秒为单位），浮点数。如果 ``None``，将使用数据集的默认延迟时间。 条的名字列表，默认为 ``None``。 block 索引列表，整数列表。 通道索引列表，整数列表。 数据集列表。 线名字的列表，默认为 ``None``。 信号长度列表（以秒为单位） 信号长度列表（以秒为单位），浮点数列表。 受试者索引数列表，整数列表。 trial 索引列表，整数列表。 变量列表。 谐波数，整数。 识别算法中使用的线程数。如果给定的值大于1，多线程并行计算将会被使用来提升计算速度。默认为 ``None``，即不使用多线程并行计算。评估器将会重设识别算法中 ``n_jobs`` 的值。 参数 表现容器 表现评估 绘制函数 绘制带误差线的条状图。每一组绘制一种颜色的条形。 绘制数据，形状为 (类别数 :raw-html:`&#215;` 观测数 :raw-html:`&#215;` 变量数)，条的高度代表观测的平均，误差线代表观测的变化。 绘制数据，形状为 (类别数 :raw-html:`&#215;` 观测数 :raw-html:`&#215;` 变量数)，线代表观测的平均，阴影代表观测的变化。 绘制数据，形状为 (类别数 :raw-html:`&#215;` 观测数 :raw-html:`&#215;` 变量数)，条的高度代表观测的平均，误差线代表观测的变化。 绘制阴影线。每一个组绘制一条阴影线。 将一个数据集的信息推入 trial 信息。 返回 运行评估过程。表现将会保存在 ``performance_container``。 ``performance_container`` 格式为 如果将 ``save_model`` 设为 ``True`` 来保存模型，将会占用大量内存。 临近条之间的距离。 补充功能 ``BaseEvaluator`` 类是一个基于 trial 的评估器。评估器包含多个评估 trial，其逐个 trial 评估表现。每个 trial 包含多个训练与测试 trial。每个 trial， ``BaseEvaluator`` 使用给定的训练 trial 来一个个训练所有的模型，然后在测试 trial 中测试他们的表现。训练时间、测试时间、真实标签与预测标签将会被保存。识别准确度与信息传输率可以被进一步计算。 用来生成参考信号的谐波数。此输入参数将会更新 trial 信息中的 ``harmonic_num``。整数。 实例自身。 ``BaseEvaluator`` 类的实例。 此类的实例是 ``BaseEvaluator`` 中 ``trial_container`` 的基础元素。 此类的实例是 ``BaseEvaluator`` 中 ``performance_container`` 的基础元素。 信号长度（以秒为单位）。此输入参数将会更新 trial 信息中的 ``tw``。浮点数。 ``TrialInfo`` 将仅使用第一个数据集来生成参考信号。如果不同的数据集使用不同的刺激，请将他们分开到不同的 trial 中。更安全的做法是让一个 ``TrialInfo`` 仅包含一个数据集。 此函数类似于 ``bar_plot_with_errorbar``，但此函数仅绘制条形，不绘制误差线。 此工具箱提供了 ``BaseEvaluator`` 类用来评估识别表现。用户可以使用此类作为父类来编写自己的评估器，或是使用提供的函数或类来编写自己的评估过程。 trial 信息 是否绘制网格，默认为 ``True``。 x 轴的刻度，默认为 ``None``。 ``X``: 全部 EEG trial 列表。 ``Y``: 标签列表。 ``[min_x, max_x]``，默认为 ``None``。 ``[min_y, max_y]``，默认为 ``None``。 ``acc``: 分类准确率，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数)。 ``block_idx``: block 索引数列表。格式和 ``sub_idx`` 一致，除了数字代表 block 索引数。 ``ch_idx``: 通道索引列表。格式和 ``sub_idx`` 一致，除了数字代表通道索引数。 ``confusion_matrix``: 混淆矩阵，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数 :raw-html:`&#215;` 标签（真实标签）数 :raw-html:`&#215;` 标签（识别标签）数)。 ``dataset_idx``: 数据集索引数列表 ``freqs``: 生成参考信号对应的刺激频率列表。 ``harmonic_num``: 用于生成参考信号的谐波数，整数。 ``itr``: 信息传输率，形状为 (方法数 :raw-html:`&#215;` 受试者数 :raw-html:`&#215;` 信号长度数)。 ``pred_label_test``: 测试 trial 的识别获得的标签被保存在此属性中。格式与 ``true_label_train`` 一致。 ``pred_label_train``: 训练后，为了评估训练表现，训练 trial 的识别获得的标签被保存在此属性中。格式与 ``true_label_train`` 一致。 ``ref_sig``: 利用 ``dataset_idx`` 中的第一个数据集的信息生成参考信号。 ``shuffle``: 重新打乱标记列表。每个元素是一个布尔值，代表是否重新打乱 trial。 ``sub_idx``: 受试者索引数列表。格式为 ``t_latency``: 数据集的延迟时间列表。每个元素是一个浮点数，代表一个数据集的延迟时间。 ``test_time_test``: 测试测试 trial 花费的时间保存在此列表中。列表中每个元素是一个评估 trial 的测试时间。 ``test_time_train``: 测试训练 trial 花费的时间保存在此列表中。列表中每个元素是一个评估 trial 的测试时间。 ``train_time``: 训练模型花费的时间保存在此列表中。列表中的每个元素是一个评估 trial 的训练时间。 ``trial_idx``: trial 索引数列表。格式和 ``sub_idx`` 一致，除了数字代表 trial 索引数。 ``true_label_test``: 测试 trial 的真实标签列表被保存于此属性中。格式与 ``true_label_train`` 一致。 ``true_label_train``: 训练后，为了评估训练表现，用于训练 trial 的真实标签被保存在此属性中。格式为 ``tw``: 信号长度（以秒为单位），浮点数 数据集索引数，整数。 其中，``performance_method_1``, ``performance_method_2``, ... 是不同算法的 ``PerformanceContainer`` 类的实例。顺序遵循 ``model_container``。 其中，``sub_idx_1``, ``sub_idx_2``, ... 是不同数据集的受试者索引。顺序遵循 ``dataset_idx``。 其中 ``train_trial_info`` 和 ``test_trial_info`` 是``TrialInfo`` 类的实例。 其中， ``trained_model_method_1``, ``trained_model_method_2``, ... 是识别算法类的实例，其顺序与 ``model_container`` 一致。 其中，``true_label_1``, ``true_label_2``, ... 是不同的评估 trial 的真实列表。 