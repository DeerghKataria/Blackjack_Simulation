# Blackjack Simulation and Analysis Project

![Python](https://img.shields.io/badge/Python-v3.8%2B-blue)
![NumPy](https://img.shields.io/badge/NumPy-Latest-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Latest-blue)
![Pandas](https://img.shields.io/badge/Pandas-Latest-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)

A comprehensive Blackjack simulation system that implements advanced card counting strategies, betting systems, and statistical analysis. This project provides tools for analyzing optimal play strategies, detecting card counting patterns, and understanding the mathematical foundations of Blackjack.

<!-- Add main project image here -->
![Blackjack Simulation Overview](images/main_simulation.png)

## 🎯 Quick Start

```python
from Simulation import Simulation
from HouseRules import HouseRules
from Strategy import BasicStrategy

# Set up a quick simulation
rules = HouseRules()
strategy = BasicStrategy()
sim = Simulation(rules=rules, strategy=strategy)
results = sim.run(num_hands=1000)

print(f"Win Rate: {results.win_rate:.2%}")
print(f"House Edge: {results.house_edge:.2%}")
```

## Table of Contents

1. [Abstract](#abstract)
2. [Project Overview](#project-overview)
3. [Key Features](#key-features)
4. [Installation](#installation)
5. [Usage Examples](#usage-examples)
6. [Game Components](#game-components)
7. [Analysis & Visualization](#analysis--visualization)
8. [Research Results](#research-results)
9. [Project Structure](#project-structure)
10. [Contributing](#contributing)
11. [Academic Reference](#academic-reference)
12. [License](#license)

## Abstract

Blackjack is one of the most mathematically interesting casino games, offering players the opportunity to use skill and strategy to influence outcomes. This project implements a comprehensive simulation environment that models real casino conditions, incorporates various card counting systems, and analyzes the effectiveness of different playing and betting strategies.

The simulation provides detailed statistical analysis and visualization tools to understand the mathematical foundations of optimal Blackjack play, making it valuable for both educational purposes and serious strategy research.

## Project Overview

This Blackjack simulation project provides a complete framework for analyzing the game from multiple perspectives. It implements accurate casino rules, various player strategies including basic strategy and card counting systems, and comprehensive statistical analysis tools.

### Why This Project?

- **Educational Value**: Understand the mathematics behind Blackjack without risking real money
- **Strategy Testing**: Validate theoretical strategies with large-scale simulations
- **Research Tool**: Analyze card counting effectiveness and detection methods
- **Customizable Environment**: Model different casino conditions and house rules

![Strategy Comparison](images/strategy_comparison.png)

## Key Features

### 🎲 Game Simulation
- **Accurate Casino Modeling**: Implements real casino rules and procedures
- **Configurable House Rules**: Customize game parameters to match different casinos
- **Multiple Deck Support**: Simulate single-deck through 8-deck shoes
- **Realistic Shuffling**: Various shuffling algorithms and cut card positions

### 🧮 Card Counting Systems
- **Hi-Lo System**: The most popular balanced counting system
- **KO (Knock-Out)**: Unbalanced system for easier mental calculation
- **Custom Systems**: Framework for implementing your own counting methods
- **True Count Conversion**: Automatic conversion for multi-deck games

![Card Counting Analysis](images/card_counting_effectiveness.png)

### 📊 Statistical Analysis
- **Performance Metrics**: Win rates, house edge, standard deviation
- **Confidence Intervals**: Statistical significance testing
- **Variance Analysis**: Risk assessment and bankroll requirements
- **Detection Analysis**: Patterns that might reveal card counting

### 💰 Betting Systems
- **Flat Betting**: Consistent bet sizing
- **Progressive Systems**: Martingale, D'Alembert, and custom progressions
- **Count-Based Betting**: Adjust bet size based on card count
- **Kelly Criterion**: Optimal bet sizing for maximum growth

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
git clone https://github.com/DeerghKataria/Blackjack_Simulation.git
cd Blackjack_Simulation

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

### Basic Simulation

```python
from Simulation import Simulation
from HouseRules import HouseRules
from Strategy import BasicStrategy

# Configure standard Vegas rules
rules = HouseRules(
    num_decks=6,
    dealer_hits_soft_17=True,
    double_after_split=True,
    surrender_allowed=True,
    blackjack_payout=1.5
)

# Run simulation with basic strategy
strategy = BasicStrategy()
sim = Simulation(rules=rules, strategy=strategy)
results = sim.run(num_hands=100000)

print(f"Expected Loss per Hand: ${results.expected_loss:.2f}")
print(f"Standard Deviation: ${results.std_dev:.2f}")
```

### Card Counting Simulation

```python
from Count import HiLoCount
from Strategy import CardCountingStrategy
from Betting import CountBasedBetting

# Set up Hi-Lo counting system
count_system = HiLoCount()
strategy = CardCountingStrategy(count_system=count_system)
betting = CountBasedBetting(base_bet=10, spread=1-12)

# Run counting simulation
sim = Simulation(rules=rules, strategy=strategy, betting=betting)
results = sim.run(num_hands=50000)

print(f"Advantage: {results.player_advantage:.3%}")
print(f"Hourly Expected Value: ${results.hourly_ev:.2f}")
```

![Betting Spread Analysis](images/betting_spread.png)

### Jupyter Notebook Analysis

For detailed analysis, open the Jupyter notebook:

```bash
jupyter notebook "Card Counting Detection.ipynb"
```

The notebook includes:
- **Interactive Simulations**: Run simulations with different parameters
- **Strategy Comparisons**: Side-by-side analysis of different approaches
- **Detection Methods**: How casinos identify card counters
- **Risk Assessment**: Bankroll requirements and risk of ruin calculations

## Game Components

### House Rules Configuration

```python
# Conservative casino rules
conservative_rules = HouseRules(
    num_decks=8,
    dealer_hits_soft_17=True,
    double_after_split=False,
    surrender_allowed=False,
    blackjack_payout=1.2  # 6:5 payout
)

# Player-friendly rules
friendly_rules = HouseRules(
    num_decks=1,
    dealer_hits_soft_17=False,
    double_after_split=True,
    surrender_allowed=True,
    blackjack_payout=1.5  # 3:2 payout
)
```

### Strategy Implementation

The project includes several strategy types:

- **Basic Strategy**: Mathematically optimal decisions for each hand combination
- **Card Counting Strategies**: Adjust play based on remaining cards
- **Conservative Strategy**: Minimize risk with conservative play
- **Aggressive Strategy**: Maximize advantage in favorable situations

### Dealer Behavior

Dealer follows standard casino protocols:
- Automatic blackjack checking
- Consistent hitting/standing rules
- Proper payout procedures
- Insurance offering when appropriate

## Analysis & Visualization

### Performance Tracking

![Performance Over Time](images/performance_tracking.png)

```python
from Plotting import (
    plot_performance, 
    plot_count_distribution, 
    plot_strategy_comparison,
    plot_betting_analysis
)

# Visualize simulation results
plot_performance(results, title="10,000 Hand Simulation")
plot_count_distribution(count_data)
plot_strategy_comparison([basic_results, counting_results])
```

### Statistical Metrics

The simulation tracks comprehensive statistics:
- **Win/Loss/Push Rates**: Percentage breakdown of outcomes
- **Expected Value**: Mathematical expectation per hand
- **Variance**: Measure of result volatility
- **Sharpe Ratio**: Risk-adjusted performance metric
- **Maximum Drawdown**: Largest peak-to-trough decline

## Research Results

### Basic Strategy Performance

Our simulations confirm theoretical expectations:
- **House Edge**: 0.5% with optimal basic strategy
- **Standard Deviation**: Approximately 1.1 betting units per hand
- **Win Rate**: ~43% (excluding pushes)

![Basic Strategy Results](images/basic_strategy_results.png)

### Card Counting Effectiveness

Hi-Lo counting system results:
- **Player Advantage**: 0.5-1.5% with proper bet spreading
- **Detection Risk**: Analysis of betting patterns that trigger suspicion
- **Bankroll Requirements**: Minimum 200 betting units for low risk of ruin

![Counting System Comparison](images/counting_comparison.png)

### Betting System Analysis

Comparison of different betting approaches:
- **Flat Betting**: Lowest variance, steady losses
- **Progressive Systems**: Higher variance, increased risk
- **Count-Based Betting**: Optimal when combined with card counting

## Project Structure

```
Blackjack_Simulation/
│
├── src/                              # Source code
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
│
├── notebooks/                        # Jupyter notebooks
│   └── Card Counting Detection.ipynb # Detailed analysis notebook
│
├── images/                           # Visualization outputs
│   ├── strategy_comparison.png
│   ├── card_counting_effectiveness.png
│   ├── betting_spread.png
│   ├── performance_tracking.png
│   ├── basic_strategy_results.png
│   └── counting_comparison.png
│
├── datasets/                         # Analysis datasets
│   ├── simulation_results.csv
│   └── strategy_performance.csv
│
├── poster/                           # Academic poster
│   └── blackjack_research_poster.pdf
│
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # This file
```

## Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution

- **New Counting Systems**: Implement additional card counting methods
- **Advanced Strategies**: Develop more sophisticated playing strategies
- **Performance Optimization**: Improve simulation speed
- **Documentation**: Enhance code documentation and examples
- **Testing**: Add unit tests and validation procedures

### Contribution Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-counting-system`)
3. Make your changes with clear, documented code
4. Add tests for new functionality
5. Update documentation as needed
6. Submit a pull request with a clear description

### Code Style

- Follow PEP 8 Python style guidelines
- Include docstrings for all classes and methods
- Add type hints where appropriate
- Write clear, self-documenting code

## Academic Reference

### Research Poster

For a comprehensive overview of the research methodology and findings, see our academic poster:

📄 **[View Research Poster](poster/blackjack_research_poster.pdf)**

The poster covers:
- Mathematical foundations of Blackjack
- Simulation methodology
- Statistical analysis results
- Practical implications for players

### Citation

If you use this project in academic work, please cite:

```bibtex
@software{kataria2024blackjack,
  title={Blackjack Simulation and Analysis Project},
  author={Kataria, Deergh},
  year={2024},
  url={https://github.com/DeerghKataria/Blackjack_Simulation},
  note={Educational simulation for Blackjack strategy analysis}
}
```

## Example Output

### Simulation Summary
```
=== Blackjack Simulation Results ===
Hands Played: 100,000
Strategy: Hi-Lo Card Counting + Basic Strategy
Betting: Count-based (1-12 spread)

Results:
├── Win Rate: 43.2%
├── Loss Rate: 48.1%
├── Push Rate: 8.7%
├── Player Advantage: +0.8%
├── Expected Hourly: +$24.50
├── Standard Deviation: $180.25
└── Risk of Ruin (200 units): 2.3%
```

## Advanced Features

### Multi-Threading Support

```python
from Simulation import ParallelSimulation

# Run multiple simulations in parallel
parallel_sim = ParallelSimulation(
    num_threads=4,
    hands_per_thread=25000
)
results = parallel_sim.run()
```

### Custom Strategy Development

```python
from Strategy import Strategy

class CustomStrategy(Strategy):
    def decision(self, hand, dealer_up_card, count=0):
        # Implement your custom logic
        if count > 2:
            return self.aggressive_play(hand, dealer_up_card)
        else:
            return self.basic_strategy(hand, dealer_up_card)
```

## Performance Benchmarks

| Strategy Type | House Edge | Std Dev | Hands/Hour | Expected $/Hour |
|---------------|------------|---------|------------|-----------------|
| Random Play | -2.5% | 1.3 | 80 | -$20.00 |
| Basic Strategy | -0.5% | 1.1 | 80 | -$4.00 |
| Hi-Lo Counting | +0.8% | 1.8 | 60 | +$24.00 |
| Advanced Count | +1.2% | 2.1 | 50 | +$30.00 |

## Troubleshooting

### Common Issues

**Issue**: Simulation runs slowly
**Solution**: Reduce number of hands or use parallel simulation

**Issue**: Memory usage is high
**Solution**: Process results in batches or increase system RAM

**Issue**: Plots not displaying
**Solution**: Ensure matplotlib backend is properly configured

### Performance Tips

- Use numpy arrays for large datasets
- Implement batch processing for memory efficiency
- Consider using multiprocessing for CPU-intensive simulations

## Educational Applications

This project serves as an excellent educational tool for:

- **Probability Theory**: Understanding conditional probability and expectation
- **Statistics**: Hypothesis testing and confidence intervals
- **Game Theory**: Optimal decision making under uncertainty
- **Computer Science**: Object-oriented programming and simulation design

## Legal Disclaimer

⚠️ **Important Notice**: This project is designed for educational and research purposes only. 

- This software is not intended for actual gambling
- Please gamble responsibly and within your means
- Be aware of local laws regarding gambling simulations
- The authors are not responsible for any gambling-related losses

## Support

If you find this project helpful:
- ⭐ Star the repository
- 🐛 Report bugs or suggest features via issues
- 🔄 Share with others interested in probability and game theory
- 📧 Contact for collaboration opportunities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Repository**: [https://github.com/DeerghKataria/Blackjack_Simulation](https://github.com/DeerghKataria/Blackjack_Simulation)

**Maintained by**: Seán Houraghan (24209056) and Deergh Kataria (24218299)

*"The house edge is just the cost of entertainment... unless you know how to count cards."* 🃏