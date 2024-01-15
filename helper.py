#@title Un poco de código para configurar todo, clonar el repo, instalar las librerias, etc.
# source: https://www.youtube.com/c/machinelearnear

import os
import sys
import shutil
import subprocess
import re

try:
    import gradio as gr
except ImportError:
    subprocess.run(["pip", "install", "gradio"])
    import gradio as gr

from os.path import exists as path_exists
from pathlib import Path
from typing import Dict

newline, bold, unbold = "\n", "\033[1m", "\033[0m"

class RepoHandler:
    def __init__(self, repo_url: str) -> None:
        """
        Initialize the RepoHandler class with the provided repository URL and requirements file.
        Args:
        - repo_url: URL of the git repository to clone.
        Returns:
        None
        """
        self.is_google_colab = False
        self.fix_for_gr, self.fix_for_st = None, None
        self.app_file = "app.py"
        if 'google.colab' in str(get_ipython()):
            print(f'{bold}Running on: "Google Colab"{unbold}')
            self.is_google_colab = True
        else:
            print(f'{bold}Running on: Local or "SM Studio Lab"{unbold}')
        self.repo_url = repo_url
        self.repo_name = self.repo_url.split('/')[-1]

    def __str__(self):
        if os.path.exists(self.repo_name):
            return self.retrieve_readme(f'{self.repo_name}/README.md')
        else:
            print(f"{bold}The repo '{self.repo_name}' has not been cloned yet.{unbold}")
            return None
            
    def retrieve_readme(self, filename) -> Dict:
        readme = {}
        if path_exists(filename):
            with open(filename) as f:
                for line in f:
                    if not line.find(':') > 0 or 'Check' in line: continue
                    (k,v) = line.split(':')
                    readme[(k)] = v.strip().replace('\n','')
        else:
            print(f"{bold}No 'readme.md' file{unbold}")
            
        return readme
        
    def clone_repo(self, overwrite=False) -> None:
        """
        Clone the git repository specified in the repo_url attribute.
        Returns:
        None
        """
        # Check if repository has already been cloned locally
        if overwrite and os.path.exists(self.repo_name): 
            try:
                shutil.rmtree(self.repo_name)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        if os.path.exists(self.repo_name):
            print(f"{bold}Repository '{self.repo_name}' has already been cloned.{unbold}")
        else:
            print(f"{bold}Cloning repo... may take a few minutes... remember to set your Space to 'public'...{unbold}")
            subprocess.run(["apt-get", "install", "git-lfs"])
            subprocess.run(["git", "lfs", "install", "--system", "--skip-repo"])
            subprocess.run(["git", "clone", "--recurse-submodules", self.repo_url])

    def install_requirements(self, requirements_file: str = None, install_xformers: bool = False) -> None:
        """
        Install the requirements specified in the requirements_file attribute.
        
        Args:
        - requirements_file: Name of the file containing the requirements to install. This file must be 
        located in the root directory of the repository. Defaults to "requirements.txt".
        Returns:
        None
        """
        if not requirements_file: requirements_file = f"{self.repo_name}/requirements.txt"
        
        # install requirements
        print(f"{bold}Installing requirements... may take a few minutes...{unbold}")
        subprocess.run(["pip", "install", "-r", requirements_file])
        if install_xformers: self.install_xformers()

    def run_web_demo(self, aws_domain=None, aws_region=None) -> None:
        """
        Launch the Gradio or Streamlit web demo for the cloned repository.
        Works with Google Colab or SageMaker Studio Lab.
        Returns:
        None
        """
        import torch
        if torch.cuda.is_available(): print(f"{bold}Using: {unbold}{self.get_gpu_memory_map()}")
        else: print(f"{bold}Not using the GPU{unbold}")
        
        readme = self.__str__()
        self.app_file = readme["app_file"]
        print(f"{bold}Demo: `{readme['title']}`{newline}{unbold}")
        print(f"{bold}Downloading models... might take up to 10 minutes to finish...{unbold}")
        print(f"{bold}Once finished, click the link below to open your application (in SM Studio Lab):{newline}{unbold}")
        if all([aws_domain, aws_region]):
              print(f'{bold}https://{aws_domain}.studio.{aws_region}.sagemaker.aws/studiolab/default/jupyter/proxy/6006/{unbold}')
                
        self.unset_environment_variables()
        
        if readme["sdk"] == 'gradio':
            gr.close_all()
            if not self.is_google_colab:
                !export GRADIO_SERVER_PORT=6006 && cd $self.repo_name && python $self.app_file
                # os.system(f'export GRADIO_SERVER_PORT=6006 && cd {self.repo_name} && python {readme["app_file"]}')
            else:
                new_filename = self.replace_gradio_launcher(f'{self.repo_name}/{readme["app_file"]}')
                !cd $self.repo_name && python $new_filename
                # os.system(f'cd {self.repo_name} && python {readme["app_file"]}')
        elif readme["title"] == 'streamlit':
            if not self.is_google_colab:
                !cd $self.repo_name && streamlit run $self.app_file --server.port 6006
                # os.system(f'cd {self.repo_name} && streamlit run {readme["app_file"]} --server.port 6006')
            else:
                !cd $self.repo_name && streamlit run $self.app_file
                # os.system(f'cd {self.repo_name} && streamlit run {readme["app_file"]}')
        else:
            print('This notebook will not work with static apps hosted on "Spaces"')

    def get_gpu_memory_map(self) -> Dict[str, int]:
        """Get the current gpu usage.
        Return:
            A dictionary in which the keys are device ids as integers and
            values are memory usage as integers in MB.
        """
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader",],
            encoding="utf-8",
            # capture_output=True,          # valid for python version >=3.7
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # for backward compatibility with python version 3.6
            check=True,
        )
        # Convert lines into a dictionary, return f"{}"
        gpu_memory = [x for x in result.stdout.strip().split(os.linesep)]
        gpu_memory_map = {f"gpu_{index}": memory for index, memory in enumerate(gpu_memory)}
        
        return gpu_memory_map

    def replace_gradio_launcher(self, old_filename) -> str:
        # Read the contents of the file
        with open(old_filename, "r") as f:
            contents = f.read()
        # Define the regular expression pattern
        pattern = r"\.launch\((.*?)\)"
        # Use the sub method to replace the text
        contents = re.sub(pattern, ".launch(share=True)", contents)
        # Write the modified contents back to the file
        new_filename = Path(old_filename).parent / f"{Path(old_filename).stem}_modified.py"
        with open(new_filename, "w") as f:
            f.write(contents)

        return new_filename.name
    
    def unset_environment_variables(self) -> None:
        os.unsetenv("SHARED_UI")
        os.environ.pop("SHARED_UI", None)
        
        os.unsetenv("IS_SHARED")
        os.environ.pop("IS_SHARED", None)

    def install_xformers(self) -> None:
        from subprocess import getoutput
        from IPython.display import HTML
        from IPython.display import clear_output
        import time

        subprocess.run(["pip", "install", "-U", "--pre", "triton"])

        s = getoutput('nvidia-smi')
        if 'T4' in s: gpu = 'T4'
        elif 'P100' in s: gpu = 'P100'
        elif 'V100' in s: gpu = 'V100'
        elif 'A100' in s: gpu = 'A100'

        while True:
            try: 
                gpu=='T4'or gpu=='P100'or gpu=='V100'or gpu=='A100'
                break
            except:
                pass
            print(f'{bold} Seems that your GPU is not supported at the moment.{unbold}')
            time.sleep(5)

        if (gpu=='T4'): 
            precompiled_wheels = "https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/T4/xformers-0.0.13.dev0-py3-none-any.whl"
        elif (gpu=='P100'): 
            precompiled_wheels = "https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/P100/xformers-0.0.13.dev0-py3-none-any.whl"
        elif (gpu=='V100'): 
            precompiled_wheels = "https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/V100/xformers-0.0.13.dev0-py3-none-any.whl"
        elif (gpu=='A100'): 
            precompiled_wheels = "https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/A100/xformers-0.0.13.dev0-py3-none-any.whl"

        subprocess.run(["pip", "install", "-q", precompiled_wheels])