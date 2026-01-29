# 📜 The Gilded Diwan (AI Urdu Poetry Generator)

[![Python](https://img.shields.io/badge/Python-3.9%2B-FFE873?style=flat-square&logo=python&logoColor=black)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

> *"Where silicon meets the soul of Urdu literature."*

---

## 🕯️ Project Overview

**The Gilded Diwan** is a state-of-the-art Natural Language Processing (NLP) project that generates classical Urdu poetry (Ghazal style) using Deep Learning. 

It explores the creative capabilities of three distinct neural architectures:
-   **RNN** (Recurrent Neural Networks)
-   **LSTM** (Long Short-Term Memory)
-   **Transformer** (Self-Attention Mechanism)

Beyond mere text generation, this project features a **premium "Dark Rustic" Web Application** that acts as a digital poet, allowing users to compose verses and mint them into beautiful digital cards.

---

## ✨ Key Features

### 🧠 The AI Brain
-   **Multi-Model Architecture**: Compare the creative outputs of RNNs, LSTMs, and Transformers.
-   **Creativity Control**: Adjust the "Temperature" to shift between literal and abstract verses.
-   **Roman-to-Urdu Engine**: Type naturally in Roman Urdu (e.g., *"Dil"*), and the engine automatically transliterates it to the correct script (`دل`) before generating poetry.

### 🎨 The Frontend Experience
-   **"Dark Rustic" Aesthetic**: A fully custom-styled user interface featuring deep charcoal textures, antique gold accents, and serif typography.
-   **Instant Transliteration**: Visual feedback shows your Roman input transforming into Urdu script in real-time.
-   **Keepsake Generator**: One-click generation of **Instagram-ready poetry cards** with vintage golden frames and elegant typography.

---

## 🚀 Getting Started

Follow these instructions to set up the digital poet on your local machine.

### Prerequisites
-   Python 3.8 or higher
-   Git

### 1. Clone the Repository
```bash
git clone https://github.com/Shaharyar2442/NLP_UrduPoetryGeneration.git
cd NLP_UrduPoetryGeneration
```

### 2. Install Dependencies
We have a dedicated requirements file for the web application:
```bash
pip install -r app/requirements.txt
```

### 3. Launch the Application
Ignite the engine and open the web interface:
```bash
streamlit run app/main.py
```
*The application should automatically open in your default browser at `http://localhost:8501`.*

---

## 🛠️ Project Structure

```bash
NLP_UrduPoetryGeneration/
├── 📂 app/                  # The "Dark Rustic" Web Application
│   ├── main.py              # Application entry point (Streamlit)
│   ├── utils.py             # core logic (Model loading, Transliteration)
│   ├── card_generator.py    # Image generation engine (Pillow)
│   └── requirements.txt     # App-specific dependencies
├── 📂 data/                 # Dataset and processed files
├── 📂 models/               # Pre-trained Keras models (.h5/.keras)
├── 📂 notebooks/            # Jupyter notebooks for training & research
└── 📂 results/              # Generated text samples and CSVs
```


---

## 🔬 Research & Experimentation

This project served as a rigorous study into the comparative performance of sequential models (RNN, LSTM) versus attention-based models (transformers) for low-resource languages like Urdu.

### 📊 Key Findings

| Model | Optimizer | Perplexity (Lower is Better) | Accuracy | Insight |
| :--- | :--- | :--- | :--- | :--- |
| **RNN** | **RMSprop** | **666.04** | **7.60%** | The most consistent performer for this dataset size. |
| **LSTM** | RMSprop | 708.72 | 7.49% | Comparable to RNN but slightly harder to converge. |
| **Transformer**| RMSprop | 811.21 | 7.20% | Requires more data; struggled with high variance compared to RNNs. |

### 🧠 Critical Insights
1.  **Optimizer Dominance**: `RMSprop` consistently outperformed `Adam` and `SGD` across all architectures. For example, the Transformer's perplexity dropped from **1077 (Adam)** to **811 (RMSprop)** just by switching optimizers.
2.  **Architecture Complexity**:
    *   **Simpler is Better**: Our hyperparameter experiments revealed that a **1-Block Transformer** (Perplexity 658) significantly outperformed a 3-Block Transformer (Perplexity 1047).
    *   **Depth vs. Breadth**: Increasing RNN layers from 1 to 3 actually *increased* perplexity (614 -> 680), suggesting the dataset is best modeled by shallower, wider networks.
3.  **The "Transformer Gap"**: While Transformers are SOTA for large corpora, on this specialized Urdu poetry dataset, **RNNs** proved more data-efficient and stable.

> *For a full deep-dive into the loss curves, attention heatmaps, and hyperparameter logs, please see the `report/` and `results/` directories.*

---

## 📸 Snapshot
![Snapshot](Screenshot%202026-01-27%20172546.png)

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for better model architectures or new UI themes:
1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
