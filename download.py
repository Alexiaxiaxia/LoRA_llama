# # Use a pipeline as a high-level helper
# from transformers import pipeline

# messages = [
#     {"role": "user", "content": "Who are you?"},
# ]
# pipe = pipeline("text-generation", model="hfl/llama-3-chinese-8b-instruct-v2")
# pipe(messages)


# from modelscope import snapshot_download

# # 指定下载目录
# cache_dir = '/root/autodl-tmp/finetuning/models'

# # 下载模型到指定目录
# model_dir = snapshot_download('baicai003/Llama3-Chinese_v2', cache_dir=cache_dir)

# # 打印模型下载地址 
# print(f"模型下载地址: {model_dir}")


# #SDK模型下载
# from modelscope import snapshot_download
# cache_dir = '/root/autodl-tmp/finetuning/models'
# model_dir = snapshot_download('shareAI/llama-3-8b-Instruct-dpo-chinese-loftq-gguf',cache_dir=cache_dir)
# print(f"模型下载地址: {model_dir}")


#模型下载
# from modelscope import snapshot_download
# cache_dir = '/root/autodl-tmp/finetuning/models'
# model_dir = snapshot_download('ChineseAlpacaGroup/llama-3-chinese-8b-instruct-gguf', cache_dir=cache_dir)
# print(f"模型下载地址: {model_dir}")


#模型下载
from modelscope import snapshot_download
cache_dir = '/root/autodl-tmp/finetuning/models'
model_dir = snapshot_download('ChineseAlpacaGroup/llama-3-chinese-8b-instruct', cache_dir=cache_dir)