# NLP Urdu Poetry Generation

This project explores the generation of Urdu poetry using Deep Learning techniques. It implements and compares various neural network architectures, including Recurrent Neural Networks (RNN), Long Short-Term Memory (LSTM) networks, and Transformers, to generate coherent and stylistically appropriate Urdu verses.

## Project Overview

The goal of this project is to build a text generation model capable of composing Urdu poetry. The project covers the entire machine learning pipeline, from data acquisition and preprocessing to model training, evaluation, and generation. It investigates the impact of different model architectures and optimizers on the quality of the generated text.

## Key Features

-   **Data Processing Pipeline:** Comprehensive cleaning, normalization, and tokenization of Urdu text.
-   **Multiple Architectures:** Implementation of Simple RNN, LSTM, and Transformer models from scratch using TensorFlow/Keras.
-   **Experimentation:** Systematic comparison of models with different optimizers (Adam, RMSprop, SGD).
-   **Poetry Generation:** Text generation capabilities with temperature control for diversity.
-   **Evaluation & Visualization:** Detailed analysis of training metrics (Accuracy, Loss, Perplexity) and visualization of results.

## Project Structure

The project is organized as follows:

-   **`data/`**: Stores the dataset.
    -   `processed/`: Contains the cleaned and tokenized data ready for training.
-   **`models/`**: Directory for saving trained model files (`.keras`) and the tokenizer (`tokenizer.pickle`).
-   **`notebooks/`**: Jupyter notebooks containing the code for each step:
    -   `data_exploration.ipynb`: Exploratory Data Analysis (EDA) of the dataset.
    -   `preprocessing.ipynb`: Data cleaning, tokenization, and sequence generation.
    -   `models_experiments.ipynb`: Training and comparing baseline models (RNN, LSTM, Transformer).
    -   `hyper_parameter_training.ipynb`: Hyperparameter tuning experiments.
    -   `text_gen.ipynb`: Generating poetry using the trained models.
    -   `show_generations.ipynb`: Displaying and analyzing generated samples.
    -   `visualization.ipynb`: Visualizing training history and model comparisons.
-   **`results/`**: Stores output files.
    -   `generated_text/`: CSV files containing generated poetry samples.
    -   `training_logs/`: CSV logs of model training history.
    -   `tables/`: Comparison tables of model performance.
-   **`requirements.txt`**: List of Python dependencies required for the project.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd NLP_UrduPoetryGeneration
    ```

2.  **Install dependencies:**
    Ensure you have Python installed. It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the project, execute the notebooks in the following order:

1.  **Data Preparation:**
    Open and run `notebooks/preprocessing.ipynb`. This will clean the raw data, create the tokenizer, and save the processed data to `data/processed/`.

2.  **Model Training:**
    Run `notebooks/models_experiments.ipynb` to train the baseline RNN, LSTM, and Transformer models. This notebook will save the trained models to the `models/` directory and training logs to `results/`.

3.  **Text Generation:**
    Run `notebooks/text_gen.ipynb`. This notebook loads the trained models and generates poetry based on seed text. You can adjust parameters like `temperature` and `seed_text` within the notebook.

4.  **Analysis & Visualization:**
    -   Use `notebooks/show_generations.ipynb` to view the generated poetry in a structured format.
    -   Use `notebooks/visualization.ipynb` to see graphs of loss, accuracy, and perplexity comparisons.

## Dependencies

-   numpy
-   pandas
-   matplotlib
-   seaborn
-   scikit-learn
-   tensorflow
-   datasets
-   urpa

## Results

The project compares the performance of different models based on Perplexity, Accuracy, and Loss. Detailed results and generated samples can be found in the `results/` directory.
