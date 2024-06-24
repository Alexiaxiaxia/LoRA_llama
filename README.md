
# 项目简介
本项目旨在采用LoRA的方法微调大模型，用来达到离线部署垂直大模型的目的


## 服务器无法学术加速解决办法

* 换 modelsope：
    ```python
    # 模型下载
    from modelscope import snapshot_download
    cache_dir = '/root/autodl-tmp/finetuning/models'
    model_dir = snapshot_download('ChineseAlpacaGroup/llama-3-chinese-8b-instruct', cache_dir=cache_dir)
    ```
* 采用学术加速

    如果在Autodl终端中使用：
    ```bash
    source /etc/network_turbo
    ```

    取消学术加速，如果不再需要建议关闭学术加速，因为该加速可能对正常网络造成一定影响
    ```bash
    unset http_proxy && unset https_proxy
    ```

## 一些服务器问题
* 软连接：对于Autodl平台服务器系统盘可能会爆掉，但是更改ollama默认位置环境变量无效。因此采用软连接。
* 需要注意的是在服务器上软连接后，软连接设置不会随着系统盘换区的迁移。
* 建议一开始用一块大于350G的数据盘。目前140G数据，350G数据盘。
* 对于conda环境，服务器检测不到，想要执行ipynb需要如下步骤
```bash
    # 创建Conda新的虚拟环境（如已创建，请忽略！）
    conda create -n tf python=3.7             # 构建一个虚拟环境，名为：tf
    conda init bash && source /root/.bashrc   # 更新bashrc中的环境变量

    # 将新的Conda虚拟环境加入jupyterlab中
    conda activate tf                         # 切换到创建的虚拟环境：tf
    conda install ipykernel
    ipython kernel install --user --name=tf   # 设置kernel，--user表示当前用户，tf为虚拟环境名称
```

## 微调库选择

可以选择的库：peft、llama-factory。这里采用peft，直接兼容huggingface


## 微调流程 
0. 下载模型。
    部分模型下载方法可在`download.py`查看
1. 准备dataset QA对
    ```json
    {
        "instruction": "小姐，别的秀女都在求中选，唯有咱们小姐想被撂牌子，菩萨一定记得真真儿的——",
        "input": "",
        "output": "嘘——都说许愿说破是不灵的。"
    }
    ```

2. 执行微调文件，生成LoRA权重 
    `LLaMA3-8B-Instruct Lora.ipynb`
3. 合并LoRA权重和基座权重,并保存大模型
    `merge_model.ipynb`
4. 量化和变成ollama可部署的gguf文件，基于llama.cpp
<https://github.com/ggerganov/llama.cpp>
命令如下：
    ```bash
    python convert-hf-to-gguf.py /root/autodl-tmp/finetuning/llama3_zhenhuan --outtype f16 --outfile /root/autodl-tmp/finetuning/llama3_zhenhuan_gguf/llama3_zhenhuan.gguf
    ```
部分参数参考：
```bash
convert-hf-to-gguf.py [-h] [--vocab-only] [--awq-path AWQ_PATH] [--outfile OUTFILE] [--outtype {f32,f16,bf16,q8_0,auto}] [--bigendian] [--use-temp-file] [--no-lazy] [--model-name MODEL_NAME] [--verbose] model
```

## 最低显卡要求：
4090 不行，最低要用 L20，主要是4090显存不够。我用一张 L20 微调 8b 模型是够用的，L20一炉子丹大约15分钟,8b llama3。



## RAG Flow 部署

RAGflow 采取 Docker 启动，是一个以 OCR 为主的方法。注意事项：
- 对于 Mac 和 Windows，可以使用 `host.docker.internal` 替换 `127.0.0.1`，如 `//host.docker.internal:11434`。
- 部署 Ollama 时，默认端口为 `11434`。

# 服务器启动指南

详情参考
<https://github.com/infiniflow/ragflow>
注意：
```bash
$ cd ragflow/docker
$ chmod +x ./entrypoint.sh # windows可以不用这句话
$ docker compose up -d
```
核心镜像大小约为 9 GB，加载可能需要一段时间。



## Ollama 模型部署

当你使用 `ollama create` 命令创建模型时，模型的数据被复制并存储到 Ollama 的内部数据库或存储系统中。这个过程确保了模型文件的所有必要信息都被完整保存，因此删除原始的 Modelfile 文件不会影响模型的运行。具体来说：
1. 数据复制和存储：在创建模型的过程中，Ollama 会将 Modelfile 中的数据读取、处理，并存储到它的内部存储系统中。这个系统可以是一个数据库或一个特定的文件系统目录。
2. 模型注册：Ollama 会注册新的模型（如 Huan16），并将其关联到内部存储的模型数据。这使得 Ollama 可以在需要时快速访问和使用这些模型数据。
3. 独立运行：一旦模型数据被成功存储，Ollama 运行模型时不再依赖于原始的 Modelfile 文件，而是直接从内部存储系统中加载模型数据。

例如：
```bash
ollama create MODEL_NAME -f /root/autodl-tmp/finetuning/models/ChineseAlpacaGroup/llama-3-chinese-8b-instruct-gguf/Modelfile
```
Modelfile基本只需要准备一个路径
windows电脑需要提前安装相关AutoDL代理软件，安装后ollama在运行后即可连接RAGFLOW

### ollama 注意事项
* 本电脑也需要运行ollama，即使ollama部署在远程服务器上
* 经过本人测试RAG FLOW 可以运行在ollama模型本地运行和docker RAG 是没问题的
* 一旦出现无法运行的情况 请检查ollama的代理是否出了问题。AutoDL开放了6006端口作为交互，如果可以建议开通企业账户用ip的方式来做或许会比较容易链接。