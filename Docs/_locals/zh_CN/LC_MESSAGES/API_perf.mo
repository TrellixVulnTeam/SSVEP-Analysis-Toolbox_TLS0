��          |               �   l   �   �   J     �      	   5     ?  
   Y     d  �  z  �   j  \   ]  �  �  ?   B  E   �     �  0   �  	   	     	     2	     9	  �  F	  �     T   �   A list of datasets. Each element is a instance of one dataset class introduced in `"Datasets" <#datasets>`_. A list of recognition models/methods. Each element is a instance of one recognition model/method class introduced in `"Recognition algorithms" <#recognition-algorithms>`_. A list of trials. The format is A list of trials. The format is  .. code-block:: python      [[train_trial_info, test_trial_info],      [train_trial_info, test_trial_info],      ...,      [train_trial_info, test_trial_info]]  where ``train_trial_info`` and ``test_trial_info`` are instances of the ``TrialInfo`` class. Evaluator Initialize the evaluator. Parameters Performance Evalution The ``BaseEvaluator`` class is a trial based evaluator. Evaluator contains several evaluation trials and evaluate performance trial by trial. Each trial contains several training and testing trials. In each trial, the ``BaseEvaluator`` uses the given training trials to train all models one by one and then tests their performance in testing trials. The training time, evaluation time, ture labels and predicted labels will be stored. The recognition accuracies and ITRs can be further computed. This toolbox provides a ``BaseEvaluator`` class for evaluating recognition performance. Users can use this class as the father class to write your own evaluator or use the above given functions or classes to write your own evaluation process. where ``train_trial_info`` and ``test_trial_info`` are instances of the ``TrialInfo`` class. Project-Id-Version: SSVEP Analysis Toolbox 
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
 数据集列表。每个元素是一个数据集类的实例。 识别算法列表。每个元素是一个识别算法类的实例。 trial 的列表。格式为 trial 列表。更具体的请参阅英文版。 评估器 初始化评估器 参数 表现评估 ``BaseEvaluator`` 类是一个基于 trial 的评估器。评估器包含多个评估 trial，其逐个 trial 评估表现。每个 trial 包含多个训练与测试 trial。每个 trial， ``BaseEvaluator`` 使用给定的训练 trial 来一个个训练所有的模型，然后在测试 trial 中测试他们的表现。训练时间、测试时间、真实标签与预测标签将会被保存。识别准确度与信息传输率可以被进一步计算。 此工具箱提供了 ``BaseEvaluator`` 类用来评估识别表现。用户可以使用此类作为父类来编写自己的评估器，或是使用提供的函数或类来编写自己的评估过程。 其中 ``train_trial_info`` 和 ``test_trial_info`` 是``TrialInfo`` 类的实例。 