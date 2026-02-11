import torch
import torch.nn as nn
import sys
import os
from PIL import Image
import numpy as np

# Add male_boneage to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'male_boneage', 'male_boneage'))

from model import BoneAgeModel
from utils.augmentation import eval_transform
from utils.gradcam_utils import create_gradcam


class ModelInference:
    """Handles loading and inference for male and female bone age models"""
    
    def __init__(self, male_model_path, female_model_path=None, device='cpu'):
        """
        Initialize models
        
        Args:
            male_model_path: Path to male model weights
            female_model_path: Path to female model weights (optional)
            device: Device to run inference on ('cpu' or 'cuda')
        """
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load male model
        self.male_model = self._load_model(male_model_path, "Male")
        
        # Load female model (use male model if female not available)
        if female_model_path and os.path.exists(female_model_path):
            self.female_model = self._load_model(female_model_path, "Female")
        else:
            print("⚠ Female model not found, using male model for both predictions")
            self.female_model = self.male_model
        
        # Age group mapping (0-3 years ranges)
        self.age_groups = {
            0: (0, 5),
            1: (5, 10),
            2: (10, 15),
            3: (15, 20)
        }
        
        # Setup Grad-CAM
        self.male_gradcam = create_gradcam(self.male_model, self.male_model.ca)
        self.female_gradcam = create_gradcam(self.female_model, self.female_model.ca)
    
    def _load_model(self, model_path, model_name):
        """Load model from checkpoint"""
        try:
            model = BoneAgeModel()
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Handle different checkpoint formats
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
            elif isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
            else:
                model.load_state_dict(checkpoint)
            
            model.to(self.device)
            model.eval()
            print(f"✓ {model_name} model loaded successfully")
            return model
        except Exception as e:
            print(f"✗ Error loading {model_name} model: {e}")
            raise
    
    def preprocess_image(self, image_input):
        """
        Preprocess image for inference
        
        Args:
            image_input: PIL Image or file path
        
        Returns:
            torch.Tensor: Preprocessed image tensor [1, 1, 224, 224]
        """
        if isinstance(image_input, str):
            image = Image.open(image_input).convert('L')
        elif isinstance(image_input, Image.Image):
            image = image_input.convert('L')
        else:
            raise ValueError("Image must be PIL Image or file path")
        
        # Apply preprocessing
        tensor = eval_transform(image).unsqueeze(0)  # Add batch dimension
        return tensor.to(self.device), image
    
    def predict_age(self, grp_logits, unc_logits):
        """
        Convert model outputs to age prediction and uncertainty
        
        Args:
            grp_logits: Group classification logits [1, 4]
            unc_logits: Uncertainty regression outputs [1, 2]
        
        Returns:
            tuple: (predicted_age, uncertainty_range)
                  uncertainty_range is the ± value (e.g., 17±0.5 means 0.5)
        """
        # Get predicted group
        pred_group = grp_logits.argmax(dim=1).item()
        
        # Get age range for this group
        age_min, age_max = self.age_groups[pred_group]
        
        # Use group midpoint as base prediction
        base_age = (age_min + age_max) / 2
        
        # Calculate uncertainty from model's unc output
        # The model outputs 2 values - we'll use them to estimate confidence
        unc_val = unc_logits[0].abs().mean().item()  # Average of absolute values
        
        # Normalize uncertainty to a reasonable range (0-2.5 years)
        # Assuming training uncertainty values are in range 0-100
        # Map to ±0.5 to ±2.5 years based on confidence
        uncertainty_normalized = min(max(unc_val / 40.0, 0.5), 2.5)
        
        return base_age, uncertainty_normalized
    
    def infer_male(self, image_input):
        """
        Perform male model inference
        
        Args:
            image_input: PIL Image or file path
        
        Returns:
            dict: Male prediction results
        """
        with torch.no_grad():
            input_tensor, original_image = self.preprocess_image(image_input)
            grp_output, unc_output = self.male_model(input_tensor)
            
            # Get predictions
            age, uncertainty = self.predict_age(grp_output, unc_output)
            
            return {
                'age': age,
                'uncertainty': uncertainty,
                'grp_logits': grp_output,
                'input_tensor': input_tensor,
                'original_image': original_image
            }
    
    def infer_female(self, image_input):
        """
        Perform female model inference
        
        Args:
            image_input: PIL Image or file path
        
        Returns:
            dict: Female prediction results
        """
        with torch.no_grad():
            input_tensor, original_image = self.preprocess_image(image_input)
            grp_output, unc_output = self.female_model(input_tensor)
            
            # Get predictions
            age, uncertainty = self.predict_age(grp_output, unc_output)
            
            return {
                'age': age,
                'uncertainty': uncertainty,
                'grp_logits': grp_output,
                'input_tensor': input_tensor,
                'original_image': original_image
            }
    
    def generate_gradcam(self, input_tensor, original_image, model_type='male'):
        """
        Generate Grad-CAM heatmap
        
        Args:
            input_tensor: Preprocessed input tensor
            original_image: Original PIL Image
            model_type: 'male' or 'female'
        
        Returns:
            numpy array: Grad-CAM heatmap
        """
        gradcam = self.male_gradcam if model_type == 'male' else self.female_gradcam
        heatmap = gradcam.generate_heatmap(input_tensor)
        return heatmap


# Global inference instance
_inference_instance = None


def get_inference_model():
    """Get or create global inference instance"""
    global _inference_instance
    if _inference_instance is None:
        male_model_path = "male_boneage_model.pth"
        female_model_path = "female_boneage_model.pth"
        _inference_instance = ModelInference(male_model_path, female_model_path)
    return _inference_instance
