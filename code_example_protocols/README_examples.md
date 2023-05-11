## This document is not finished ##

=> the point of this folder is to store different examples of completion to:
1. standardize them
2. convert them in Jsonline
3. repeat what has been done for the first fine tuning (the other folder of this GitHub):
    - data augmentation
    - cleaning/formatting
    - exportation for OpenAI API
    - finetuning

    /// ////

# 1. Import Libraries

What does 'sys.path.insert(0, os.getcwd())' does ?

By default, Python only searches for modules and packages in predefined sets of directories, so we add current working directory to beginning of system path to allow Python to find modules and packages that are located in the current working directory when running the script using 'sys.path.insert(0, os.getcwd())'