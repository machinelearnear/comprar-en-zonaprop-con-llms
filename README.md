# Open 🤗 Spaces in SageMaker Studio Lab

`HF Spaces` are a great way to showcase your ML work and are quickly becoming the platform of choice for that. This repository is a short step by step tutorial about how to run an ML application hosted on [Hugging Face Spaces](https://huggingface.co/spaces) inside SageMaker Studio Lab. This is relevant because Studio Lab offers free GPU (Nvidia T4, better than Google Colab) for 4 hours at a time plus 15G of persistant storage. Have a look at this [other repo](https://github.com/machinelearnear/use-gradio-streamlit-sagemaker-studiolab) to understand more about what we are doing here.

https://user-images.githubusercontent.com/78419164/162445810-18ebea84-1b4f-4b1c-b24d-0feff6ad3ff6.mov

## Watch YouTube Explainer Video
[![[#08] Cómo usar 🤗 Spaces + GPU sin costo en minutos con SM Studio Lab](https://img.youtube.com/vi/skaYsdSuE70/0.jpg)](https://www.youtube.com/watch?v=skaYsdSuE70)

## Getting started
- [SageMaker StudioLab Explainer Video](https://www.youtube.com/watch?v=FUEIwAsrMP4)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces#reference)
- [Gradio Documentation](https://gradio.app/getting_started/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Use Gradio or Streamlit on Studio Lab](https://github.com/machinelearnear/use-gradio-streamlit-sagemaker-studiolab)

## Step by step tutorial

### Setup your environment

First, you need to get a [SageMaker Studio Lab](https://studiolab.sagemaker.aws/) account. This is completely free and you don't need an AWS account. Because this new service is still in Preview and AWS is looking to reduce fraud (e.g. crypto mining), you will need to wait 1-3 days for your account to be approved. You can see [this video](https://www.youtube.com/watch?v=FUEIwAsrMP4&ab_channel=machinelearnear) for more information.

Now that you have your Studio Lab account, you can follow the steps shown in `launch_app.ipynb` [![Open In SageMaker Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/machinelearnear/open-hf-spaces-in-studiolab/blob/main/launch_app.ipynb).

Click on `Copy to project` in the top right corner. This will open the Studio Lab web interface and ask you whether you want to clone the entire repo or just the Notebook. Clone the entire repo and click `Yes` when asked about building the `Conda` environment automatically. You will now be running on top of a `Python` environment with `Streamlit` and `Gradio` already installed along with other libraries.

In order to browse to Streamlit or Gradio, you will need to add `proxy/6006/` at the end of your Studio Lab url. It will look like this:

```python
studiolab_url = f'https://{studiolab_domain}.studio.{studiolab_region}.sagemaker.aws/studiolab/default/jupyter/proxy/6006/'
```

### Clone repo and install dependencies

We first point to the Spaces url that we want to run on Studio Lab:

```python
hf_spaces_url = 'https://huggingface.co/spaces/swzamir/Restormer' # choose any demo you like from https://huggingface.co/spaces
hf_spaces_folder = hf_spaces_url.split('/')[-1]
```

Clone the repo and install dependencies.

```python
import os
from os.path import exists as path_exists
if not path_exists(hf_spaces_folder):
    os.system(f'git clone {hf_spaces_url}')
    os.system(f'pip install -r {hf_spaces_folder}/requirements.txt')
```

Within every `Space` there's a `README.md` with information about the app. Example below:

```
---
title: Image Restoration with Restormer
emoji: 🌍
colorFrom: yellow
colorTo: yellow
sdk: gradio
sdk_version: 2.9.0
app_file: app.py
pinned: false
license: afl-3.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces#reference
```

We parse that file into a dict to make our lives easier down the line. We use:

```python
def info_from_readme(fname):
    readme = {}
    with open(fname) as f:
        for line in f:
            if not line.find(':') > 0 or 'Check' in line: continue
            (k,v) = line.split(':')
            readme[(k)] = v.strip().replace('\n','')
    
    return readme
```

### Launch your ML application

So now we have our repo, we have installed the required libraries, and all we have to do is launch our app. For that we define a very simple function that takes the local path to the repo, prints the Studio Lab url your application will run on, and then launches either Streamlit or Gradio on the right server port depending on the type of `sdk` that was used on HF Spaces:

```python
def launch_demo(folder_name, url=studiolab_url):
    if path_exists(folder_name):
        readme = info_from_readme(f'{folder_name}/README.md')
    else:
        print('No `README.md` file')
        return
    
    print('\033[1m' + f'Demo: {readme["title"]}\n' + '\033[0m')
    print(f'Please wait a few seconds before you click the link below to load your demo \n{url}\n')
        
    if readme["sdk"] == 'gradio':
        os.system(f'export GRADIO_SERVER_PORT=6006 && cd {folder_name} && python {readme["app_file"]}')
    elif readme["title"] == 'streamlit':
        os.sytem(f'cd {folder_name} && streamlit run {readme["app_file"]} --server.port 6006') # 6006 or 80/8080 are open
    else:
        print('This notebook will not work with static apps hosted on `Spaces`')
```

All we need to do now is to run `launch_demo(hf_spaces_folder)`.

## References
- See more about Restormer here: https://huggingface.co/spaces/swzamir/Restormer

## Disclaimer
- The content provided in this repository is for demonstration purposes and not meant for production. You should use your own discretion when using the content.
- The ideas and opinions outlined in these examples are my own and do not represent the opinions of AWS.
