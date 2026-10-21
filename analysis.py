"""Palmer Penguins: what explains body mass variation?

Runs the full analysis end to end and writes the figures plus a short
summary table used in the README.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "penguins.csv"
FIGS = ROOT / "figures"
OUT = ROOT / "results"

for folder in (FIGS, OUT):
    if not folder.is_dir():
        folder.mkdir(parents=True)

SPECIES_COLORS = {
    "Adelie": "#1f77b4",
    "Chinstrap": "#d95f02",
    "Gentoo": "#2ca02c",
}

plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    before = len(df)
    df = df.dropna(subset=["bill_length_mm", "bill_depth_mm",
                           "flipper_length_mm", "body_mass_g", "sex"])
    print(f"Rows loaded: {before}, complete cases kept: {len(df)}")
    return df


def figure_scatter(df: pd.DataFrame) -> float:
    """Body mass vs flipper length, pooled fit plus per-species fits."""
    x = df["flipper_length_mm"].to_numpy()
    y = df["body_mass_g"].to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for species, group in df.groupby("species"):
        ax.scatter(group["flipper_length_mm"], group["body_mass_g"],
                   s=26, alpha=0.75, label=species,
                   color=SPECIES_COLORS[species], edgecolor="white", linewidth=0.4)
        s, i = np.polyfit(group["flipper_length_mm"], group["body_mass_g"], 1)
        xs = np.linspace(group["flipper_length_mm"].min(),
                         group["flipper_length_mm"].max(), 20)
        ax.plot(xs, s * xs + i, color=SPECIES_COLORS[species], linewidth=1.2, alpha=0.9)

    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, slope * xs + intercept, color="#444444", linewidth=2,
            linestyle="--", label=f"All birds (R²={r2:.2f})")

    ax.set_xlabel("Flipper length (mm)")
    ax.set_ylabel("Body mass (g)")
    ax.set_title("Heavier birds have longer flippers, but the slope differs by species")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.grid(alpha=0.2, linewidth=0.5)
    fig.tight_layout()
    fig.savefig(FIGS / "fig1_mass_vs_flipper.png", bbox_inches="tight")
    plt.close(fig)
    return r2


def figure_boxplot(df: pd.DataFrame) -> pd.DataFrame:
    """Body mass by species and sex."""
    order = ["Adelie", "Chinstrap", "Gentoo"]
    data = [df.loc[(df["species"] == s) & (df["sex"] == sex), "body_mass_g"]
            for s in order for sex in ("male", "female")]

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    bp = ax.boxplot(data, patch_artist=True, widths=0.62,
                    medianprops={"color": "#222222", "linewidth": 1.2},
                    flierprops={"markersize": 3, "markerfacecolor": "#999999",
                                "markeredgecolor": "none"})
    for patch, species in zip(bp["boxes"], [s for s in order for _ in (0, 1)]):
        patch.set_facecolor(SPECIES_COLORS[species])
        patch.set_alpha(0.35)
        patch.set_edgecolor(SPECIES_COLORS[species])

    ax.set_xticks(range(1, 7))
    ax.set_xticklabels([f"{s}\n{sex}" for s in order for sex in ("male", "female")],
                       fontsize=8.5)
    ax.set_ylabel("Body mass (g)")
    ax.set_title("Within every species, males are heavier than females")
    ax.grid(axis="y", alpha=0.2, linewidth=0.5)
    fig.tight_layout()
    fig.savefig(FIGS / "fig2_mass_by_sex.png", bbox_inches="tight")
    plt.close(fig)

    return (df.groupby(["species", "sex"])["body_mass_g"]
              .agg(["count", "mean", "std"]).round(1))


def within_species_gap(df: pd.DataFrame, pooled_r2: float) -> pd.DataFrame:
    """Per-species regression of mass on flipper length."""
    rows = []
    for species, group in df.groupby("species"):
        slope, intercept = np.polyfit(group["flipper_length_mm"],
                                      group["body_mass_g"], 1)
        r = np.corrcoef(group["flipper_length_mm"], group["body_mass_g"])[0, 1]
        rows.append({
            "species": species,
            "n": len(group),
            "mean_mass_g": round(group["body_mass_g"].mean(), 1),
            "slope_g_per_mm": round(slope, 1),
            "r2_within": round(r ** 2, 2),
        })
    table = pd.DataFrame(rows)
    table.attrs["pooled_r2"] = pooled_r2
    return table


def main() -> None:
    df = load_data(DATA)

    pooled_r2 = figure_scatter(df)
    by_sex = figure_boxplot(df)
    table = within_species_gap(df, pooled_r2)

    by_sex.to_csv(OUT / "mass_by_species_sex.csv")
    table.to_csv(OUT / "within_species_regression.csv", index=False)

    with open(OUT / "summary.md", "w") as fh:
        fh.write("# Results\n\n")
        fh.write(f"- Complete cases: {len(df)} of 344\n")
        fh.write(f"- Pooled R² (mass ~ flipper length): {pooled_r2:.3f}\n")
        fh.write(f"- Species means (g): "
                 f"{df.groupby('species')['body_mass_g'].mean().round(0).to_dict()}\n")
        fh.write(f"- Male minus female mean mass (g): "
                 f"{(df[df.sex == 'male']['body_mass_g'].mean() - df[df.sex == 'female']['body_mass_g'].mean()):.0f}\n\n")
        fh.write(table.to_string(index=False))

    print(f"Pooled R² = {pooled_r2:.3f}")
    print(table.to_string(index=False))
    print(f"Figures written to {FIGS}")


if __name__ == "__main__":
    main()
