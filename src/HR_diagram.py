import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter # for 1e4 to 10^4 formatting
import numpy as np


# read csv file 
df = pd.read_csv(r"C:\Users\user\Downloads\hyg_v42.csv.gz")


# Selecting the necessary columns and removing missing values
df = df[['ci', 'absmag', 'spect']].dropna() #ci: B–V color index (related to surface temperature)
                                            #absmag: absolute magnitude
                                            #spect: spectral classification

# filter out unrealistic color index values
df = df[(df['ci'] > -0.5) & (df['ci'] < 3)] # The HYG catalog combines multiple observational sources and includes measurement uncertainties and estimated values; 
                                            # therefore, physically unrealistic color indices may appear. To ensure a meaningful Hertzsprung–Russell diagram,
                                            #stars with extreme and non-physical B–V values were excluded using a quality cut.


# Converting Color Index to Surface Temperature
df['Teff'] = 4600 * (
    1 / (0.92 * df['ci'] + 1.7) +
    1 / (0.92 * df['ci'] + 0.62)
)                                  
#This empirical relation (Ballesteros, 2012)


# Converting Absolute Magnitude to Luminosity
M_sun = 4.83
df['luminosity'] = 10 ** (0.4 * (M_sun - df['absmag']))


# Extracting Spectral Classes
df['spec_class'] = df['spect'].str[0] #The first letter of strings like G2V, K1III is taken

valid_classes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
df = df[df['spec_class'].isin(valid_classes)] # only keep valid spectral classes


# Color mapping for spectral classes for readability
spec_colors = {
    'O': '#9bb0ff',
    'B': '#aabfff',
    'A': '#cad7ff',
    'F': '#f8f7ff',
    'G': '#fff4cc',
    'K': '#ffd2a1',
    'M': '#ff9b7a'
}


# HR Diagram Plotting left y-axis: Luminosity
fig, ax_L = plt.subplots(figsize=(9, 7)) #

for sp in valid_classes:
    subset = df[df['spec_class'] == sp]
    ax_L.scatter( 
        subset['Teff'],
        subset['luminosity'],
        s=3,
        color=spec_colors[sp], 
        alpha=0.7,
        label=sp
    )

#Logarithmic Scaling and Axis Orientation
ax_L.set_xscale('log')
ax_L.set_yscale('log')
ax_L.invert_xaxis() # HR diagrams temperature decreasing to the right

# Temperature ticks (standard HR diagram values)
temp_ticks = [40000, 20000, 10000, 5000, 3000] # Define temperature ticks for the bottom x-axis
                                               # These are standard reference temperatures used in
                                               # Hertzsprung–Russell diagrams.

ax_L.set_xticks(temp_ticks)
ax_L.set_xticklabels([r"$4\times10^4$", r"$2\times10^4$", r"$10^4$", r"$5\times10^3$", r"$3\times10^3$"])


ax_L.set_xlabel("Surface Temperature (K)")
ax_L.set_ylabel(r"Luminosity ($L/L_\odot$)")


# Right y-axis: Absolute Magnitude
ax_M = ax_L.twinx()
ax_M.set_yscale('log')
ax_M.set_ylim(ax_L.get_ylim())

#This converts luminosity back into absolute magnitude.
def mag_from_lum(L):
    return M_sun - 2.5 * np.log10(L)

ax_M.set_ylabel("Absolute Magnitude")
ax_M.set_yticks(ax_L.get_yticks())
ax_M.set_yticklabels([f"{mag_from_lum(l):.1f}" for l in ax_L.get_yticks()])


# Upper x-axis: Spectral Class
ax_spec = ax_L.twiny()

spectral_T = [40000, 20000, 10000, 7500, 5800, 4500, 3000]
spectral_labels = ['O', 'B', 'A', 'F', 'G', 'K', 'M']

ax_spec.set_xscale('log')
ax_spec.invert_xaxis()
ax_spec.set_xlim(ax_L.get_xlim())
ax_spec.set_xticks(spectral_T)
ax_spec.set_xticklabels(spectral_labels)
ax_spec.set_xlabel("Spectral Class")

# Logarithmic Tick Formatting
def log_format(x, pos):
    exponent = int(np.log10(x))
    return rf"$10^{{{exponent}}}$"

formatter = FuncFormatter(log_format)
ax_L.yaxis.set_major_formatter(formatter)

#Final Visual Enhancements
ax_L.set_title("Hertzsprung–Russell Diagram (HYG v42)")
ax_L.legend(title="Spectral Class", frameon=False, markerscale=4)
ax_L.grid(True, which='both', alpha=0.3)

ax_L.set_facecolor('#f9f9f9')
fig.patch.set_facecolor('white')

# Annotating Key Regions
ax_L.text(7000, 1, "Main Sequence", fontsize=12)
ax_L.text(4500, 1e3, "Red Giants", fontsize=12)
ax_L.text(10000, 1e6, "Supergiants", fontsize=12)


plt.tight_layout()
fig.savefig(
    r"C:\Users\user\Downloads\HR_diagram_HYG_v42.pdf",
    format="pdf"
)
plt.show()



