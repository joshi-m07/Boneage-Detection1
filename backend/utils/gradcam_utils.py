import torch
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64


class GradCAMGenerator:
    """Enhanced Grad-CAM implementation for bone age models"""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None
        
        # Register hooks
        target_layer.register_forward_hook(self._save_activations)
        target_layer.register_full_backward_hook(self._save_gradients)
    
    def _save_activations(self, module, inp, out):
        """Save forward pass activations"""
        self.activations = out.detach()
    
    def _save_gradients(self, module, grad_in, grad_out):
        """Save backward pass gradients"""
        self.gradients = grad_out[0].detach()
    
    def generate_heatmap(self, input_tensor, class_idx=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            input_tensor: Input image tensor [1, 1, 224, 224]
            class_idx: Target class index (default: argmax of predictions)
        
        Returns:
            numpy array: Heatmap [H, W]
        """
        self.model.eval()
        self.model.zero_grad()
        
        # Forward pass
        grp_output, unc_output = self.model(input_tensor)
        
        # Use argmax class if not specified
        if class_idx is None:
            class_idx = grp_output.argmax(dim=1).item()
        
        # Backward pass
        grp_output[:, class_idx].backward()
        
        # Generate CAM
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1).squeeze()
        
        # Apply ReLU and normalize
        cam = torch.relu(cam)
        cam = cam.cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        
        return cam
    
    def overlay_heatmap(self, original_image, heatmap, alpha=0.4):
        """
        Overlay heatmap on original image
        
        Args:
            original_image: PIL Image or numpy array
            heatmap: Grad-CAM heatmap [H, W]
            alpha: Transparency of heatmap overlay
        
        Returns:
            numpy array: Overlayed image
        """
        # Convert PIL to numpy if needed
        if isinstance(original_image, Image.Image):
            original_image = np.array(original_image)
        
        # Resize heatmap to match image size
        h, w = original_image.shape[:2]
        heatmap_resized = cv2.resize(heatmap, (w, h))
        
        # Convert heatmap to color
        heatmap_colored = cv2.applyColorMap(
            (heatmap_resized * 255).astype(np.uint8), 
            cv2.COLORMAP_JET
        )
        
        # Convert grayscale to RGB if needed
        if len(original_image.shape) == 2:
            original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)
        elif original_image.shape[2] == 1:
            original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2RGB)
        
        # Overlay
        overlayed = cv2.addWeighted(original_image, 1-alpha, heatmap_colored, alpha, 0)
        
        return overlayed
    
    def save_visualization(self, original_image, heatmap, save_path):
        """
        Save Grad-CAM visualization
        
        Args:
            original_image: PIL Image or numpy array
            heatmap: Grad-CAM heatmap
            save_path: Output file path
        """
        overlayed = self.overlay_heatmap(original_image, heatmap)
        cv2.imwrite(save_path, cv2.cvtColor(overlayed, cv2.COLOR_RGB2BGR))
        return save_path
    
    def get_base64_image(self, original_image, heatmap):
        """
        Get base64 encoded Grad-CAM visualization
        
        Args:
            original_image: PIL Image or numpy array
            heatmap: Grad-CAM heatmap
        
        Returns:
            str: Base64 encoded image
        """
        overlayed = self.overlay_heatmap(original_image, heatmap)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(overlayed)
        
        # Encode to base64
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        base64_str = base64.b64encode(buffer.read()).decode()
        
        return f"data:image/png;base64,{base64_str}"


def create_gradcam(model, target_layer):
    """Factory function to create GradCAM instance"""
    return GradCAMGenerator(model, target_layer)
