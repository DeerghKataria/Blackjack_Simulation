from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

class bankrollPlot:
    def __init__(self):
        self.handBankrolls = []
        self.roundBankrolls = []
        
    def recordHandBankroll(self, player):
        self.handBankrolls.append(player.rollingBankroll)
        
    def recordRoundBankroll(self):
        bankrolls = self.handBankrolls
        self.handBankrolls = []
        self.roundBankrolls.append(bankrolls)
        
    def plotBankrollDist(self):
        """Plot the density distribution of final bankroll figures from Monte Carlo simulation"""
        # Extract final bankroll from each round (last value in each round's bankroll list)
        final_bankrolls = [round_bankrolls[-1] for round_bankrolls in self.roundBankrolls if round_bankrolls]
        
        if not final_bankrolls:
            print("No bankroll data available to plot")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create density plot using histogram with density=True and fill
        n, bins, patches = ax.hist(final_bankrolls, bins=50, density=True, alpha=0.6, 
                                  color='skyblue', edgecolor='black', linewidth=0.5)
        
        # Add smooth density curve using gaussian kernel density estimation
        kde = gaussian_kde(final_bankrolls)
        x_range = np.linspace(min(final_bankrolls), max(final_bankrolls), 300)
        density_curve = kde(x_range)
        ax.plot(x_range, density_curve, color='darkblue', linewidth=2, 
                label='Density Curve')
        
        # Add statistical lines
        mean_bankroll = np.mean(final_bankrolls)
        median_bankroll = np.median(final_bankrolls)
        
        ax.axvline(mean_bankroll, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: ${mean_bankroll:.2f}')
        ax.axvline(median_bankroll, color='green', linestyle='--', linewidth=2, 
                   label=f'Median: ${median_bankroll:.2f}')
        
        # Formatting
        ax.set_title("Density Distribution of Final Bankroll Values (Monte Carlo Simulation)")
        ax.set_xlabel("Final Bankroll ($)")
        ax.set_ylabel("Density")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add statistics text
        stats_text = f"""Simulations: {len(final_bankrolls)}
Mean: ${mean_bankroll:.2f}
Std Dev: ${np.std(final_bankrolls):.2f}
Min: ${min(final_bankrolls):.2f}
Max: ${max(final_bankrolls):.2f}"""
        
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
    def plotBankrollOverTime(self):
        """Plot bankroll progression over time for each simulation round (original functionality)"""
        fig, ax = plt.subplots()
        ax.set_title("Plot of Player Bankroll over each Round")
        ax.set_xlabel("Hand Number")
        ax.set_ylabel("Bankroll")
        
        for bankroll in self.roundBankrolls:
            ax.plot([i for i in range(1, len(bankroll)+1)], bankroll, alpha=0.6)
            
        plt.show()
        
    def plotMCResults(self, houseEdge):
        """Plot bankroll progression with rotated density distribution (like the photo)"""
        # Extract final bankroll from each round
        final_bankrolls = [round_bankrolls[-1] for round_bankrolls in self.roundBankrolls if round_bankrolls]
        
        # Create figure with custom layout - main plot on left, rotated density on right
        fig = plt.figure(figsize=(12, 6))
        
        # Main plot (left side) - progression lines
        ax_main = plt.subplot2grid((1, 4), (0, 0), colspan=3)
        
        # Plot bankroll progression over time
        for bankroll in self.roundBankrolls:
            ax_main.plot([i for i in range(1, len(bankroll)+1)], bankroll, alpha=0.3)
        
        ax_main.set_xlabel("Hand Number")
        ax_main.set_ylabel("Bankroll ($)")
        ax_main.set_title("Bankroll Progression")
        ax_main.grid(True, alpha=0.3)
        
        # Density plot (right side) - rotated 90 degrees clockwise
        ax_density = plt.subplot2grid((1, 4), (0, 3))
        
        # Calculate density using KDE
        kde = gaussian_kde(final_bankrolls)
        y_range = np.linspace(min(final_bankrolls), max(final_bankrolls), 300)
        density_values = kde(y_range)
        
        # Plot density horizontally (rotated 90 degrees clockwise)
        ax_density.plot(density_values, y_range, color='darkblue', linewidth=2)
        ax_density.fill_betweenx(y_range, 0, density_values, alpha=0.6, color='skyblue')
        
        # Add statistical lines on the density plot
        mean_bankroll = np.mean(final_bankrolls)
        
        ax_density.axhline(mean_bankroll, color='red', linestyle='--', linewidth=2, 
                          label=f'Mean: ${mean_bankroll:.2f}')
        
        # Format density plot
        ax_density.set_ylabel("")
        ax_density.set_title("Distribution", rotation=0, pad=20)
        ax_density.yaxis.set_label_position("right")
        ax_density.yaxis.tick_right()
        ax_density.grid(True, alpha=0.3)
        # ax_density.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        
        # Match y-axis limits between main plot and density plot
        y_min = min(min(final_bankrolls), ax_main.get_ylim()[0])
        y_max = max(max(final_bankrolls), ax_main.get_ylim()[1])
        ax_main.set_ylim(y_min, y_max)
        ax_density.set_ylim(y_min, y_max)
        
        # Add statistics text to main plot
        stats_text = f"""Simulations: {len(final_bankrolls)}
Mean: ${mean_bankroll:.2f}
Std Dev: ${np.std(final_bankrolls):.2f}
Min: ${min(final_bankrolls):.2f}
Max: ${max(final_bankrolls):.2f}
House Edge: {houseEdge:.2f}%"""
        
        ax_main.text(0.02, 0.98, stats_text, transform=ax_main.transAxes, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
