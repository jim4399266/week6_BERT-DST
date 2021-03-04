中文数据集使用中文crosswoz，利用xbot中的readable_preprocess.py转换为readable文件进行处理。  
get_ontology.py文件获取ontology  
dataset_cn.py文件整理中文数据集  

# BERT-DST

The code has been tested with Python 3 and PyTorch 1.5.0. Note that the code in the folder `pytorch_pretrained_bert` was originally from the [Hugging Face team](https://github.com/huggingface). With minor modifications, you can use the latest version of [huggingface/transformers](https://github.com/huggingface/transformers).

## Commands
An example training command (using BERT-Base) is:
`python main.py --do_train --data_dir=data/woz/ --bert_model=bert-base-uncased --output_dir=outputs`

An example training command (using BERT-Large) is:
`python main.py --do_train --data_dir=data/woz/ --bert_model=bert-large-uncased --output_dir=outputs`

中文模型训练命令（使用chinese-bert-wwm-ext），添加了--language参数：
python main.py --do_train --data_dir=data/readable_data --bert_model=./chinese-bert-wwm-ext  --output_dir=./outputs --language=cn

## Results

The table below shows the results on the WoZ restaurant reservation datasets.

Model | Joint Goal (WoZ) | Turn Request (WoZ)|
:---: |:---: | :---: |
Neural Belief Tracker - DNN | 84.4% | 91.2% |
Neural Belief Tracker - CNN | 84.2% | 91.6% |
GLAD | 88.1 ± 0.4% | 97.1 ± 0.2% |
*Simple BERT Model* (BERT-Base) | 90.5% | 97.6% |



https://github.com/jim4399266/week6_BERT-DST/blob/main/images/%E8%8B%B1%E6%96%87crosswoz.png

中文数据集卡在Start traing
