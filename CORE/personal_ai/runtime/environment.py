import os,sys,shutil,platform
class Environment:
    @staticmethod
    def detect():
        cuda=False; gpus=0
        try:
            import torch; cuda=bool(torch.cuda.is_available()); gpus=int(torch.cuda.device_count()) if cuda else 0
        except Exception: pass
        return {'python':sys.version.split()[0],'platform':platform.platform(),'cuda':cuda,'gpu_count':gpus,'ffmpeg':shutil.which('ffmpeg') is not None,'git':shutil.which('git') is not None,'kaggle':bool(os.environ.get('KAGGLE_KERNEL_RUN_TYPE')),'colab':bool(os.environ.get('COLAB_RELEASE_TAG'))}
