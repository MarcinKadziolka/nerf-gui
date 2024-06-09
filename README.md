# NerfGUI

NeRF is a machine learning model that allows to render new high quality views after training on few dozens images of the scene.

example car gif

But how do we do that? After all we only have pictures of the scene, that we need to somehow used to create representation of the object such that we will be able to query model at any location that we can imagine.

This is done in 3 steps:

1. March rays and sample points
   
   Rays are marched through the scene from the position of the real camera cooridnates which are known beforehand. Each camera also has viewing direction (its imporant to know which direction the camera is facing). Then points are sampled along the ray, which basically means choosing some locations along the ray that'll later be used to render an image.
   
   Each point is represented as a tuple of its x, y, z cooridnates and also camera origin and viewing direction.

2. Get colors and densities
   
   Now we use the NeRF model, which given point representations predicts its color (RGB) and density $\sigma$. $\sigma$ describes whether model thinks something is there or not.
   
   We do that until every point has been assigned its color and density.

3. Render colors and compare
   
   Now we can use classical rendering techniques to accumulate all the samples into one color. Only those colors which density is high will contribute to the final output. It is taken into account that light stops traveling further upon hitting solid object, so the colors predicted "behind" the object won't be taken into account.
   
   Now, we can compare our predicted output with real value and measure the error.
   
   Because every step of the process is differntiable gradient descent methods can be used to minimize error (improve reconstruction of the image)

But how we do get the representation?

This process repeats thousand of times (usually we have 40-70 (400x400) pictures, and rays are shot through every pixel), therefore model has ability to distinguish different points from each other. Simplifying: if it has seen a point from one angle, and its yellow, then it made a prediction of the same point from a different angle, and its still yellow, how probable it is that this point is still yellow viewed from the middle of two angles?

After successful training every possible view can be render at will.

## Medical

### Use Case

### Medical vs Synthetic data

Compared to synthetic data which is usually used to evaluate model performance, medical datasets are based off of CT scans, which sample data only in one axis.
![Medical_vs_synthetic_data!](assets/images/mednerf/Sampling_diff.jpg) 

### MedNeRF

MedNeRF utilizes GRAF based model to produce accurate 3D projections from few or single view x-ray. GRAF uses SIREN to generate
shape and appearance vectors used to describe predicted NeRF patch for a given view angle. Due to training GAN on medical datasets which, due to their nature are usually quite small, a number of issues,
such as mode collapse can occur. The authors solve that by combining GRAF with DAG and using multiple discriminator heads.
![MedNERF!](assets/images/mednerf/MEDNERF.jpg) 

### Hyper NeRFGAN

HyperNeRFGAN builds from INR GAN model by replacing INR model with NeRF.
![nerfgan!](assets/images/mednerf/Nerfgan.jpg)

Generator takes the sample from Gaussian distribution and returns the set of parameters Θ.These parameters are further used inside the NeRF model
FΘ to transform the spatial location x = (x, y, z) to emitted color c = (r, g, b) and volume density σ. Θ is split into two parts Θ which is generated for each representation and Θs which is share by all of them.

#### Adapting model to use medical case

![Nerf_sample_changes!](assets/images/mednerf/Untitled.jpg) 
To evaluate a model for the medical application and ensure comparability with existing methodologies, we use a dataset employed in the MedNeRF containing digitally reconstructed radiographs (DRR) with 20 examples for chest and 5 examples for knee, each consisting of 72 128×128 images taken every 5 degrees, covering full 360-degree vertical rotation per patient. To account
for differences between synthetic and medical datasets we change the sampling angle to only cover one axis as the MedNeRF authors did, and change the model configuration to not assume a white background for the training data. We train the model on a single example for each experiment.

### Experiments

We performed ablation study investigating ways to improve model results. We've experimented with implementing stylegan2 augmentations, changed the number of feature maps and implememted nerf viewing directions
[TABLE]
[CONCLUSIONS]

### Results

Compared to other models, HyperNeRFGAN achieves significantly better results, leading to higher quality projections from single view x-ray.
![results!](assets/images/mednerf/results.jpg) 
[IMAGES AND GIFS]
