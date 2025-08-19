# Blackjack Simulation 🃏

![Python](https://img.shields.io/badge/Python-v3.8%2B-blue)
![NumPy](https://img.shields.io/badge/NumPy-Latest-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-blue)
![Pandas](https://img.shields.io/badge/Pandas-Latest-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

*"The house edge is just the cost of entertainment... unless you know how to count cards."* 🃏

A Python-based simulation framework for analyzing **Blackjack strategies, betting systems, and card counting detection** using **Monte Carlo simulations** and **machine learning models**.

This project was developed as part of *ACM40960 — Projects in Maths Modelling* at University College Dublin.

## Repository Structure

```
Blackjack_Simulation/
├── Blackjack/                        # Source code
│   ├── Betting.py                    # Betting strategy implementations
│   ├── Card.py                       # Card class and properties
│   ├── Count.py                      # Card counting logic
│   ├── Dealer.py                     # Dealer behavior and actions
│   ├── Deck.py                       # Deck management and shuffling
│   ├── Hand.py                       # Hand evaluation and status
│   ├── HouseRules.py                 # Configurable game rules
│   ├── Player.py                     # Player decision logic
│   ├── Plotting.py                   # Visualization tools
│   ├── Simulation.py                 # Batch simulation runner
│   └── Strategy.py                   # Player strategies
│   └── SimulationNotebook.ipynb      # Monte Carlo Simulation of BlackJack
├── Images/                           # Visualization outputs
├── Datasets/                         # Analysis datasets
├── Poster/                           # Academic poster
├── Card Counting Detection.ipynb     # Detailed analysis notebook
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## Table of Contents

1. [Abstract](#abstract)
2. [Project Overview](#project-overview)
3. [Key Features](#key-features)
4. [Installation](#installation)
5. [Usage Examples](#usage-examples)
6. [Game Components](#game-components)
7. [Analysis & Visualization](#analysis--visualization)
8. [Monte Carlo Simulation Notebook Explainer](#monte-carlo-simulation-notebook-explainer)
9. [Research Results](#research-results)
10. [Contributing](#contributing)
11. [Academic Reference](#academic-reference)
12. [License](#license)

## Abstract

Blackjack is one of the most mathematically rich casino games, where optimal play and strategy can significantly influence long-term outcomes. This project explores the balance between **player advantage strategies** (e.g., card counting) and **casino countermeasures** through large-scale simulations and statistical modeling.

Our study focuses on:
- Simulating **real casino Blackjack rules**.
- Evaluating the **effectiveness of strategies** like basic play, no-bust, random play, and card counting.
- Analyzing **betting spreads** and **rule variations** (e.g., decks used, payouts, dealer actions).
- Developing **machine learning models** to detect card counters based on gameplay data.

## Project Overview

This simulation framework provides a comprehensive environment for analyzing Blackjack strategies, betting systems, and detection mechanisms. The project combines mathematical modeling with machine learning to understand both player and casino perspectives in the game of Blackjack.

The simulation engine runs millions of hands using Monte Carlo methods to generate statistically significant results across different game configurations and player strategies.

## Key Features

- **Blackjack Simulator**: Implements casino rules with configurable game settings
- **Monte Carlo Engine**: Runs millions of simulated hands to measure statistical outcomes
- **Strategy Comparison**: Evaluates player performance under different strategies
- **Betting Analysis**: Tests flat betting vs. progressive betting spreads
- **Rule Variations**: Examines how changes (deck count, S17/H17, 6:5 payouts, etc.) impact the house edge
- **ML Counter Detection**: Random Forest, Logistic Regression, and SVM models to identify card counters
- **Data Visualization**: Generates plots for bankroll distributions, house edge, and model performance

## Installation

### Prerequisites

```bash
# Check Python version (3.8+ required)
python --version

# Ensure pip is installed
pip --version
```

### Quick Install

```bash
# Clone the repository
git clone https://github.com/ACM40960/project-sean-deergh-blackjack-project
cd Blackjack

# Create virtual environment
python -m venv blackjack_env

# Activate virtual environment
# On macOS/Linux:
source blackjack_env/bin/activate
# On Windows:
blackjack_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
scipy>=1.7.0
```

## Usage Examples

### Counting Card Analysis

```bash
# Launch Jupyter and open the analysis notebook
jupyter notebook
# Navigate to 'Card Counting Detection.ipynb'
```

### Monte Carlo Simulation

```bash
cd Blackjack
# Launch Jupyter and open the analysis notebook
jupyter notebook
# Navigate to 'SimulationNotebook.ipynb'
```

## Game Components

The simulation implements the following core components:

- **Card & Deck Management**: Realistic card dealing and shuffling
- **Player Strategies**: Basic strategy, card counting, random play, and no-bust
- **Dealer Logic**: Standard casino dealer rules and behaviors
- **Betting Systems**: Flat betting and various spread betting strategies
- **House Rules**: Configurable game variations and rule sets

## Analysis & Visualization

The framework provides comprehensive visualization tools for:

- **Bankroll distributions across strategies**
- **House edge by rule variations**  
- **Confusion matrix for card counter detection**
- **Strategy performance metrics**
- **Betting system effectiveness**

## Monte Carlo Simulation Notebook Explainer

`SimulationNotebook.ipynb` runs a Monte Carlo simulation of blackjack games with fully customizable settings. You can adjust **house rules** (e.g., dealer stands on soft 17, blackjack payout, number of decks), choose different **player strategies** (basic strategy, casino play, no-bust, random), enable **card counting**, and apply different **betting spreads** (flat, progressive, or wonging out). Players are configured with an initial bankroll and strategy accuracy, and simulations can be run over many trials and hands to analyze long-term outcomes.  

By modifying the rule parameters, strategy class, betting spread, or simulation settings, you can test how different conditions impact profitability.

After running the notebook, one can expect a similar output:

![BlackJack Monte Carlo](Images/BlackJack_Monte_Carlo_Simulation.jpeg)


## Research Results

### Strategy Performance

![Playing Strategy Analysis](Images/BankrollDist.png)

- **Card counting**: Only profitable strategy → **+0.39% house edge**
- **Basic strategy**: **-0.50% house edge**
- **Random strategy**: **-34.58% house edge** (worst performance)

### Betting Strategies

![Betting Strategy Analysis](Images/HouseEdge.png)

- **Flat betting**: Negative returns even with card counting
- **Spread betting**: Increases profitability; *1-25 Wong Out spread* yields **+1.76% edge** in S17 games

### Rule Impact

- More decks change the house edge
- Favorable rules (e.g., Stand on Soft 17) slightly help players
- Harsh rules (e.g., 6:5 payout) strongly favor the house (-1.18%)

### Variance

- Even with an edge, **short-term variance dominates**
- Simulation of 5M hands: wide confidence intervals show need for bankroll management and long-term play

### Machine Learning Detection

![Model Performance Comparison](Images/Model_Performance_Comparison.png)

- **Random Forest** best at detecting card counters:
  - **F1 score:** 0.76
  - **Accuracy:** 0.80
- **Most predictive features**: Bet size, true count, player value, dealer upcard
- **Random Forest Confusion Matrix**: With high accuracy it can verified, whether a player is counting cards or not.

![Random Forest Confusion Matrix](Images/Random_Forest_Confusion_Matrix.png)

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests to help improve the simulation framework.

If you find this project helpful:
- ⭐ Star the repository
- 🐛 Report bugs or suggest features via issues
- 🔄 Share with others interested in probability and game theory
- 📧 Contact for collaboration opportunities

## Academic Reference

### Research Poster

For a comprehensive overview of the research methodology and findings, see our academic poster:

📄 **[View Research Poster](Poster/Poster_Presentation.pdf)**

The poster covers:
- Mathematical foundations of Blackjack
- Simulation methodology
- Statistical analysis results
- Practical implications for players

### Authors

- **Seán Houraghan** (24209056), *MSc Data and Computational Science (2024-25)*
- **Deergh Kataria** (24218299), *MSc Data and Computational Science (2024-25)*

University College Dublin, School of Mathematics

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---