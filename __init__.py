import logging
import re
from pathlib import Path

import numpy as np
import torch
from aesthetic_predictor_v2_5 import convert_v2_5_from_siglip
from PIL import Image

CURRENT_DIR = Path(__file__).parent

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}


logger = logging.getLogger(__name__)


class CustomNodeMeta(type):
    def __new__(
        cls,
        name: str,
        bases: list,
        attrs: dict,
    ) -> "CustomNodeMeta":
        global NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        new_class = super().__new__(cls, name, bases, attrs)
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = cls.__format_class_name(name)
        return new_class

    def __format_class_name(class_name: str) -> str:
        formatted_name = re.sub(r"(?<!^)(?=[A-Z])", " ", class_name)
        return formatted_name


class AestheticsPredictorV2_5Node(metaclass=CustomNodeMeta):
    RETURN_TYPES: tuple[str] = ("STRING",)
    RETURN_NAMES: tuple[str] = ("score",)
    FUNCTION: str = "predict"
    OUTPUT_NODE: bool = True

    def __init__(self):
        self.predictor = AestheticPredictorV2_5()

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    def predict(self, image: torch.Tensor) -> tuple[str]:
        score = self.predictor(image)
        return (str(score),)


class AestheticPredictorV2_5:
    def __init__(self):
        # load model and preprocessor
        self._model, self._preprocessor = convert_v2_5_from_siglip(
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        if torch.cuda.is_available():
            self._model = self._model.to(torch.bfloat16).cuda()

    def __call__(self, image_tensor: torch.Tensor) -> float:
        """
        Predicts the aesthetic score of an image.

        Parameters
        ----------
        image_tensor : torch.Tensor
            The image(s) to predict the aesthetic score of.

        Returns
        -------
        float
            The aesthetic score of the image.
        """
        image_tensor = (image_tensor.detach().cpu().squeeze().numpy() * 255).astype(
            np.uint8
        )
        image = Image.fromarray(image_tensor).convert("RGB")
        # preprocess image
        pixel_values = self._preprocessor(images=image, return_tensors="pt").pixel_values

        if torch.cuda.is_available():
            pixel_values = pixel_values.to(torch.bfloat16).cuda()

        # predict aesthetic score
        with torch.inference_mode():
            score = self._model(pixel_values).logits.squeeze().float().cpu().numpy()

        return score


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
