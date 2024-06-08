# NerfGUI
## About
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum
## Medical 
### Medical vs Synthetic data
Compared to synthetic data which is usually used to evaluate model performance, medical datasets are based off of CT scans, which sample data only in one axis.
![Test image!](assets/images/mednerf/Sampling_diff.jpg)
![Test image!](assets/images/mednerf/Untitled.jpg) 

To evaluate a model for the medical application and ensure comparability with existing methodologies, we use a dataset employed in the MedNeRF containing digitally reconstructed radiographs (DRR) with 20 examples for chest and 5 examples for knee, each consisting of 72 128×128 images taken every 5 degrees, covering full 360-degree vertical rotation per patient. To account
for differences between synthetic and medical datasets we change the sampling angle to only cover one axis as the MedNeRF authors did, and change the model configuration to not assume a white background for the training data. We train the model on a single example for each experiment.
<div class="test-componenent">
    <p>Test component</p>
<ul>
    <li>List item</li>
<button>button</button>
</ul>
</div>