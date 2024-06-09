# NerfGUI

## What is NeRF?
NeRF is a machine learning model that allows to render new high quality views after training on few dozens images of the scene.

The idea begins with having images of the scene that we want to represent.

<img src="https://github.com/MarcinKadziolka/nerf-gui/assets/30349386/d049acc6-26be-497b-b109-2f1a69664684" width="400">

Then we want to be able to create new previously unseen image of the scene.

<img src="https://github.com/MarcinKadziolka/nerf-gui/assets/30349386/91513a6e-178c-4534-bbfe-fcfab5f23949" width="400">

But how do we do that? After all we only have pictures of the scene, that we need to somehow use to create representation of the object such that we will be able to query model at any location that we can imagine.

<img src="https://github.com/MarcinKadziolka/nerf-gui/assets/30349386/297c3a0d-714f-4172-99c2-f24be27f0c50" width="400">

This is the problem that NeRF solves in 3 steps.

### 1. March rays and sample points

Rays are marched through the scene from the position of the real camera cooridnates which are known beforehand. Each camera also has viewing direction (its imporant to know which direction the camera is facing). Then points are sampled along the ray, which basically means choosing some locations along the ray that'll later be used to render an image. Each point is represented as a tuple of its x, y, z cooridnates and also camera origin and viewing direction.

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDZtb3RiaHVxZWYwYnMzYnFyNWhnMmJlenUyMjZsNHpoOXI5ZW83ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Xg9OsvGchuBV8pD5l9/giphy.gif)

### 2. Get colors and densities

Now we use the NeRF model, which given point representations predicts its color (RGB) and density $\sigma$. $\sigma$ describes whether model thinks something is there or not.
We do that until every point has been assigned its color and density.

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnB5NjQzemJ6b3E0OWoyamU4bmw3bXNnMXl5cWFrYnNkOHF2ZjdvcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6TeTwFqyoMsXSlt3h6/giphy.gif)

### 3. Render colors and compare

Now we can use classical rendering techniques to accumulate all the samples into one color. Only those colors which density is high will contribute to the final output. It is taken into account that light stops traveling further upon hitting solid object, so the colors predicted "behind" the object won't be taken into account.
Now, we can compare our predicted output with real value and measure the error.
Because every step of the process is differntiable gradient descent methods can be used to minimize error (improve reconstruction of the image)

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTRzNHIzbGlyc2duYTFmamtheW11ZW01NG1nODY3ZDNjYTR5cjEwYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6ldmvwjbJS9WchYeIo/giphy.gif)

### But how we do get the representation?

This process repeats thousand of times (usually we have 40-70 (400x400) pictures, and rays are shot through every pixel), therefore model has ability to distinguish different points from each other. Simplifying: if it has seen a point from one angle, and its yellow, then it made a prediction of the same point from a different angle, and its still yellow, how probable it is that this point is still yellow viewed from the middle of two angles?

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzZmMGpnanE3dTNta3hycnFpcmtrcHM5YzdzbGVrZzlrNXpkMjdwYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/jXqwRj5eXtbOfxF9yd/giphy.gif)

### Rendering

After successful training every possible view can be render at will.

![](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXdjOTRnMnhsdWNwbWJ3Z2UzMG5wcHA5NXMyc2lqNXM4eHBhZWE4YSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O11QQczTPt3rjTLzHW/giphy.gif)

## Sampling in NeRF

Let's take a closer look at the way points are sampled in the original NeRF and why one would like to improve it.

Original sampling process is done in two stages: first, to get the initial information about densities and second, to resample in the areas of the highest density (highest probability that something is there)

### First stage: Initial uniform sampling

Firstly, ray is divided into N equal bins along the ray. Then for each bin we sample once with the uniform probability between the ends. Why? We want to make sure that we sample throughout the whole scene, but also let the model explore the space, which fixed sampling would prevent.

![](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGY4b3o4dWFtcjlxOHVwMDNqZjJpNTFxbHJ2OHh3bjUxdm03ejBkaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/m7kilMWnQNq5VsB4V9/giphy.gif)

### Second stage: Resampling in dense areas

Secondly, initial samples are sent to NeRF model (referred to as "coarse", because it takes in coarsly sampled points), which outputs RGB and $\sigma$ for each point. We don't care about the color, but the information about density is very usuful. Then more points are sampled accordingly to retrieved piecewise-constant probability function. In that way we make sure to cover all the imporant parts of the scene.

![](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWdkd3UyZGVldWR5YWJoZ3BtM2FkMHUwOGdrMWxsZTRnNHFheWE3MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8Cqeh5RSiSMplgSfbH/giphy.gif)

### The issue with sampling

Unfortunetly whole process is very slow, because NeRF model has to evaluate thousand of samples before it can become useful (trained) and able to render new views. And even then the rendering process is slow making real-time rendering not feasible.

Wouldn't it be nice to sample exactly on the edge of the beggining of matter? Then only one point would be needed to get the color for the pixel. If that's not really possible, then sampling directly in the close proximity of dense area would still be a grand improvment.

![](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZnZtazNpYXI4c20xY29kMDUwMjZieWhwNWZvNnM5ZDB0YmVtYzZ6ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JFPMUsHZRHzlkHnKIo/giphy.gif)

### Solution

That's exactly the problem that our work is trying to solve. With long lasting project, various ideas and experiments we still haven't arrived at the desired effect, but for now  we present our best results so far in the form of this application.





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
